# Laporan Integrasi Phase 13: Decision Engine, API, UI Dua Lapis, dan Evaluasi LLM

**Repositori Riset:** `/mnt/c/CODING/research_taniAdapt`  
**Repositori Aplikasi Web:** `/mnt/c/CODING/TaniAdapt/taniadapt-web`  
**Tanggal Pelaksanaan:** 2026-10-13  
**Status Pengesahan Dokumen:** PENDING_HUMAN (Menunggu ratifikasi pengguna manusia)  

---

## 1. Ringkasan Eksekutif Pekerjaan yang Selesai

Seluruh tahapan implementasi Phase 13 dari Langkah 0 sampai Langkah 6 telah diselesaikan dan dieksekusi secara nyata dengan bukti hasil pengujian:

1. **Langkah 0: Audit Awal**:
   * Kondisi git, branch, dan tag `phase13-gate-ready` (commit `deccd9f`) terverifikasi utuh.
   * Test suite `tests/test_engine_schema_and_rules.py` dijalankan via Pytest: **7 passed in 2.84s (100% lulus)**.

2. **Langkah 1: Pembaruan `rules/rules.json` (v2.4-verified-params)**:
   * **FAO-56 Tabel 22 (Bab 8)**: Parameter $p$ dan rentang kedalaman akar $Z_r$ diperbarui sesuai rujukan tabel:
     - Jagung: $Z_r \in [1.0, 1.7]\text{ m}$, nilai pilihan tim $1.0\text{ m}$ di dalam rentang FAO-56; $p = 0.55$ (untuk $ET_c \approx 5\text{ mm/hari}$).
     - Kedelai: $Z_r \in [0.6, 1.3]\text{ m}$, nilai pilihan tim $0.8\text{ m}$ di dalam rentang FAO-56; $p = 0.50$ (memperbaiki bug config lama $p=0.55$).
     - Tomat: $Z_r \in [0.7, 1.5]\text{ m}$, nilai pilihan tim $0.7\text{ m}$ di dalam rentang FAO-56; $p = 0.40$ (memperbaiki bug config lama $p=0.55$).
     - Padi: $p = 0.20$ dari saturasi; modul deplesi tanah tak jenuh TIDAK berlaku untuk padi sawah tergenang air; status dikunci pada `INSUFFICIENT`.
     - Formula penyesuaian $p$ terhadap $ET_c$ (FAO-56 Eq. 89 p. 162: $p = p_{\text{tab}} + 0.04(5 - ET_c)$) serta variasi tekstur tanah ($\pm 5\text{--}10\%$) dicatat sebagai batasan, tidak diterapkan sebagai koreksi otomatis.
   * **FAO-56 Tabel 19 (Bab 7)**: Karakteristik tanah loam ($\theta_{FC} = 0.27, \theta_{WP} = 0.12, TAW = 150.0\text{ mm/m}$) ditandai sebagai: *"asumsi tanah loam, nilai dipilih dari rentang FAO-56 Tabel 19"*. Rentang sensitivitas TAW $130.0\text{--}180.0\text{ mm/m}$ dicatat.
   * **FAO-56 Tabel 12 (Bab 6)**: $K_{c,\text{end}}$ jagung memilih antara $0.35$ (panen kering di batang) dan $0.60$ (panen basah) lewat konfigurasi `panen_kering`; kedelai $0.50$; tomat rentang $0.70\text{--}0.90$ dengan nilai pilihan tim $0.80$ bertanda `CONVENTION_PENDING`.
   * **FAO-56 Tabel 11 (Bab 6)**: Panjang fase kedelai Tropics 15/15/40/15 (85 hari); jagung Nigeria humid 20/35/40/30 (125 hari, label analog humid); tomat tanpa baris tropis ditandai `CONVENTION_PENDING`.
   * **Aturan LWD Baru**: Menghapus aturan lama berbasis $T_{\min} - T_d$. Menambahkan `RULE_OPT_LWD_HOURLY_RH90` (jumlah jam per hari dengan $RH \ge 90\%$ dari data jam-jaman) berstatus baru **`METHOD_UNCALIBRATED`** (dasar: Sentelhas et al. 2008, *Agric. For. Meteorol.* 148(3):392–400). Aturan ini dilarang mengisi status level atas `kondisi_stres_abiotik` atau `kondisi_mendukung_OPT`.
   * **Pembersihan Skema**: Enum `METHOD_UNCALIBRATED` ditambahkan ke `schemas/engine_output.schema.json`. Status tidak terpakai `waspada_defisit_ringan` dicabut dari skema. `evidence_refs` diperketat wajib memuat ID aturan pemicu (`RULE_WATER_FAO56_DEPLETION`).

3. **Langkah 2: Modul Engine TypeScript Murni Tanpa I/O (`src/lib/engine/`)**:
   * Dibangun di `taniadapt-web/src/lib/engine/`:
     - `fao56.ts`: Implementasi fungsi murni evapotranspirasi acuan FAO-56 Penman-Monteith harian (Eq. 6).
     - `kc.ts`: Perhitungan dinamis koefisien tanaman $K_c$ berdasarkan HST (DAP) dan fase fenologi.
     - `waterBalance.ts`: Perhitungan $TAW$, $RAW = p \times TAW$, neraca deplesi harian $D_r$, input eksplisit $D_{r,0}$ (default $0\text{ mm}$ kapasitas lapang), dan uji sensitivitas $TAW$ pada $130$ vs $180\text{ mm/m}$ (menghasilkan flag `sensitif_terhadap_asumsi_tanah = true` jika keputusan berubah).
     - `percentile.ts`: Evaluasi peringkat persentil 14-hari dengan penegakan paritas sumber data (mismatch AgERA5 vs Open-Meteo otomatis mengembalikan `evidence_insufficient`).
     - `rules.ts`: Pemuat tunggal `rules.json` tanpa angka ilmiah yang di-hardcode di kode program.
     - `engine.ts`: Orkestrator penilai seluruh aturan operasional dan jadwal per jam (06.00–18.00 WIB) dengan prinsip worst-of.
     - `types.ts`: Tipe kontrak TypeScript yang patuh pada `schemas/engine_output.schema.json`.

4. **Langkah 3: Automated Testing Vitest**:
   * Membangun test suite di `taniadapt-web/tests/engine.test.ts`.
   * Memvalidasi paritas terhadap `tests/golden_engine_vectors.json` hasil pipeline Python.
   * Seluruh **13 unit tests lulus 100%** via Vitest.

5. **Langkah 4: Route Handler Server-Side Next.js (`/api/advisory`)**:
   * Lokasi: `taniadapt-web/src/app/api/advisory/route.ts`.
   * Input divalidasi ketat menggunakan **Zod Schema** (HTTP 400 jika format tanggal, crop, atau koordinat cacat).
   * Menghubungkan data cuaca harian dan per jam dari Open-Meteo Forecast API.
   * Payload keluaran divalidasi menggunakan **Ajv Draft 2020-12** terhadap `engine_output.schema.json` sebelum dikirim (HTTP 500 jika ada pelanggaran kontrak skema).

6. **Langkah 5: Antarmuka UI Dua Lapis & Halaman Sumber & Batasan**:
   * **Lapis 1**: Rekomendasi ringkas (Sangat Aman / Perlu Waspada / Hindari / Bukti Belum Cukup, window terbaik, dan catatan aksi) pada `EvaluationCard.tsx`.
   * **Lapis 2**: Rincian dasar bukti per aturan dengan badge warna transparan (*Metode terverifikasi*, *Metode belum dikalibrasi*, *Konvensi tim*, *Bukti belum cukup*), flag sensitivitas tanah, dan asumsi $D_{r,0}$.
   * **Halaman Statis Sumber & Batasan**: Dibuat di `taniadapt-web/src/app/sumber-dan-batasan/page.tsx` memuat teks transparansi resmi, atribusi lisensi CC BY 4.0 Open-Meteo, sitasi Copernicus, CHIRPS, BPS, dan batasan agronomis.
   * Build produksi Next.js berhasil dikompilasi dengan 0 error (**8/8 routes generated**).

7. **Langkah 6: Evaluasi Lapisan LLM (Explanation Layer)**:
   * Dibangun skrip evaluasi `scripts/evaluate_llm_explanation_layer.py`.
   * Menguji 10 kasus evaluasi kritis dengan aturan zero-tolerance (larangan menambah angka, larangan nama obat kimia/dosis, penolakan tebak yield, dan kejujuran insufficient).
   * Seluruh **10 kasus uji lulus 100% (10/10 PASS)**.

---

## 2. Hasil Eksekusi Pengujian (Test Results)

| Test Suite | Framework | Target yang Diuji | Jumlah Lulus | Jumlah Gagal | Status |
|---|---|---|:---:|:---:|:---:|
| **Python Engine & Rules Test** | `pytest` | `tests/test_engine_schema_and_rules.py` (Validasi skema, if/then stress, config p dan Zr) | 7 | 0 | **PASS (100%)** |
| **TypeScript Engine Unit Tests** | `vitest` | `taniadapt-web/tests/engine.test.ts` (Example 18 Brussels 3.88 mm/hari, golden vectors parity, sensitivitas tanah, Ajv Draft 2020-12) | 13 | 0 | **PASS (100%)** |
| **LLM Explanation Layer Tests** | Python Runner | `scripts/evaluate_llm_explanation_layer.py` (10 kasus zero-tolerance: anti-halusinasi, anti-obat kimia, anti-tebak yield, kejujuran insufficient) | 10 | 0 | **PASS (100%)** |
| **Next.js Production Build** | `next build` | Kompilasi Turbopack & TypeScript (`/`, `/api/advisory`, `/sumber-dan-batasan`) | 8 routes | 0 error | **PASS (Exit 0)** |

---

## 3. Item PENDING_HUMAN (Wajib Ratifikasi / Pengisian Manusia)

Sesuai instruksi mutlak, sistem tidak menebak atau mengarang fakta. Berikut daftar item yang berstatus **`PENDING_HUMAN`** untuk ditinjau oleh pengguna manusia:

1. **`bps_manual_input.csv`**:
   - Kolom halaman cetak `<HALAMAN_CETAK_2015>` (Tabel 5.1.3/5.1.12 BPS JDA 2016).
   - Kolom halaman cetak `<HALAMAN_CETAK_2018_2019>` (Tabel 5.1.1 BPS JDA 2020).
   - Konfirmasi nama file fisik PDF atau URL resmi publikasi BPS JDA 2016, 2017, 2018, dan 2020.
2. **`sumber-dan-batasan/page.tsx`**:
   - `[TAHUN: ISI MANUSIA]`: Tahun rilis informasi Copernicus Climate Change Service yang dipakai.
   - `[ISI MANUSIA, salin dari halaman dataset CDS]`: Teks sitasi resmi dataset AgERA5 dari portal Copernicus CDS.
   - `[ISI MANUSIA]`: Sumber detail penyedia dataset mentah DS03 (Dinas Pertanian Jawa Barat / Portal Satu Data Jabar).
3. **Ratifikasi Dokumen Portofolio**:
   - Dokumen `docs/crop_outcome_decision.md` dan `rules/rules.json` berstatus `PENDING_HUMAN` sampai pengguna manusia meratifikasi secara tertulis.

---

## 4. Batasan Sistem yang Diketahui (Known Limitations)

1. **Modul Air Padi Sawah**: Rumus deplesi lengas tanah tak jenuh ($RAW = p \times TAW$) tidak berlaku untuk budidaya sawah tergenang (*ponded conditions*); modul penyiraman padi secara jujur mengembalikan status `evidence_insufficient`.
2. **Aturan Kebasahan Daun (LWD)**: Menggunakan jam dengan $RH \ge 90\%$ dari data jam-jaman berstatus `METHOD_UNCALIBRATED` (Sentelhas et al. 2008); ambang jam belum terkalibrasi terhadap sensor mikroklimat in-situ Jawa Barat sehingga tidak boleh memicu status bahaya level atas.
3. **Aturan Tindakan Konvensi Lapangan**: Ambang batas kecepatan angin (3–12 km/j), hujan penyemprotan/pemupukan, dan radiasi terik siang merupakan aturan praktis tim lapangan (`CONVENTION_PENDING`) tanpa model kalibrasi sensor lokal.
4. **Asumsi Karakteristik Tanah Loam**: Kapasitas simpan air tanah ($TAW = 150.0\text{ mm/m}$) mengacu pada tanah loam FAO-56 Tabel 19; engine menyertakan flag `sensitif_terhadap_asumsi_tanah` untuk memperingatkan petani jika hasil keputusan dipengaruhi oleh variasi rentang kapasitas tanah ($130\text{--}180\text{ mm/m}$).

---

## 5. Jejak Commit dan Git Tag

* **Repositori Aplikasi Web (`taniadapt-web`)**:
  - **Commit Hash:** `2b16398`
  - **Commit Message:** `feat(phase13): implement pure TypeScript decision engine, Route Handler /api/advisory, Two-Layer UI, and Vitest suite`
  - **Git Tag Baru:** **`phase13-m1-engine`** (terkunci pada commit `2b16398`).
* **Repositori Riset (`research_taniAdapt`)**:
  - **Commit Hash Sebelumnya:** `deccd9f` (Tag: `phase13-gate-ready`) dan `adf1717` (Tag: `bps-verified-partial`).
  - **Tag Lama Utuh:** `audit-v3`, `phase4-close-candidate`, `v2-audit-closure`, `phase12-honest-status`, `phase13-gate-ready`, `bps-verified-partial`.
