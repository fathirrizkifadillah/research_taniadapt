# Laporan Milestone Phase 13 (M2): Rekonsiliasi Anomali DS03 2019, Standarisasi Sitasi FAO-56, Pengetatan Kontrak Skema, & Uji Paritas Independen

**Repositori Riset:** `/mnt/c/CODING/research_taniAdapt`  
**Repositori Web:** `/mnt/c/CODING/TaniAdapt/taniadapt-web`  
**Tanggal Pelaksanaan:** 2026-10-13  
**Status Pengesahan Dokumen:** PENDING_HUMAN (Menunggu ratifikasi pengguna manusia; dilarang mencantumkan status RATIFIED)  

---

## 1. Diagnosis Anomali Produktivitas Padi DS03 Tahun 2019

Rasio rata-rata berbobot luas panen DS03 terhadap BPS KSA Jawa Barat tahun 2019 adalah **1,2181 (+21,81%)** (DS03: 70,09 ku/ha vs BPS KSA: 57,54 ku/ha). Pemeriksaan forensik empiris dilakukan secara objektif tanpa menyimpulkan penyebab sebelum ada bukti primer:

### A. Perbandingan Luas Panen, Produksi, dan Produktivitas Provinsi (DS03 vs BPS)

| Tahun | Metrik | Nilai Agregat DS03 | Nilai Resmi BPS (JDA 2020 / BRS) | Rasio (DS03 / BPS) | Selisih (%) | Status & Catatan |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **2018** | **Produksi (ton)** | 11.494.099 | 9.647.359 | 1,1914 | +19,14% | BPS KSA (BRS 68/11/32) |
| | **Luas Panen (ha)** | 2.050.066 | 1.691.725 | 1,2118 | +21,18% | BPS KSA (BRS 68/11/32) |
| | **Produktivitas (ku/ha)** | **56,07** (berbobot) | **56,51** | **0,9922** | **-0,78%** | **Konsisten Paritas Yield (< 1% diff)** |
| **2019** | **Produksi (ton)** | 13.892.899 | 9.084.957 | 1,5292 | +52,92% | BPS KSA (JDA 2020 Tabel 5.1.1) |
| | **Luas Panen (ha)** | 1.982.170 | 1.578.836 | 1,2555 | +25,55% | BPS KSA (JDA 2020 Tabel 5.1.1) |
| | **Produktivitas (ku/ha)** | **70,09** (berbobot) | **57,54** | **1,2181** | **+21,81%** | **ANOMALI BESAR (+21,81%)** |
| **2020** | **Produksi (ton)** | 10.615.119 | 9.016.773 | 1,1773 | +17,73% | BPS KSA (BRS 67/10/32 / JDA 2021) |
| | **Luas Panen (ha)** | 1.919.561 | 1.586.889 | 1,2097 | +20,97% | BPS KSA (BRS 67/10/32) |
| | **Produktivitas (ku/ha)** | **55,30** (berbobot) | **56,82** | **0,9733** | **-2,67%** | **Konsisten Paritas Yield (< 3% diff)** |

*Temuan Kritis*: Pada tahun 2018 dan 2020, luas panen dan produksi DS03 keduanya ~20% lebih besar daripada BPS KSA (mencerminkan perbedaan cakupan metode ubinan konvensional dinas vs survei KSA citra satelit), namun **rasio produktivitasnya hampir identik** (56,07 vs 56,51 pada 2018; 55,30 vs 56,82 pada 2020). Sebaliknya, pada tahun 2019, produksi DS03 melonjak menjadi 13,89 juta ton sementara BPS KSA mencatat 9,08 juta ton, menghasilkan selisih produktivitas +21,81%.

### B. Distribusi Produktivitas per Kabupaten/Kota 2019 vs 2018 & 2020 (DS03)
- **Baris Duplikat**: 0 baris duplikat (tepat 27 kabupaten/kota).
- **Nilai Kosong / Null**: 0 nilai kosong.
- **Karakteristik Lonjakan**: Lonjakan terjadi **secara serempak pada 27 dari 27 kabupaten/kota se-Jawa Barat**:
  * Rasio Produktivitas 2019 / 2018: Rerata = 1,2390, Median = 1,2196, Rentang = [1,0618, 1,3921], Standar Deviasi = 0,0691.
  * Rasio Produktivitas 2019 / 2020: Rerata = 1,2669, Median = 1,2773, Rentang = [1,0854, 1,3904], Standar Deviasi = 0,0789.
  * Nilai minimum 2019 adalah 58,89 ku/ha (Kab. Sukabumi) dan maksimum 77,01 ku/ha (Kab. Bandung). Tidak ada pencilan tunggal (outlier terisolasi); seluruh kurva distribusi bergeser ke kanan sebesar +22% sampai +27%.
- **Kemungkinan Kesalahan Satuan / Definisi**: Pola pergeseran serentak berskala $\approx 1,22$ konsisten dengan dugaan perbedaan kadar air gabah atau pencatatan GKP mentah sebelum konversi GKG, namun karena belum ada bukti dokumen teknis tertulis dari Dinas Pertanian Jawa Barat, status resmi pada `reports/dataset_audit/b1_rice_reconciliation_v2.csv` ditandai tegas sebagai: **`ANOMALI, BELUM DIJELASKAN`**.

### C. Pemeriksaan Serupa pada Jagung (DS05) dan Kedelai (DS07) Tahun 2019
- **Jagung (DS05)**:
  * Rata-rata produktivitas: 2018 = 45,52 ku/ha; 2019 = 42,83 ku/ha; 2020 = 53,58 ku/ha.
  * Rasio 2019 / 2018: Rerata = 1,0083, Median = 0,9870, Standar Deviasi = 0,2854.
  * *Temuan*: **TIDAK ada lonjakan serempak pada jagung di tahun 2019** (sebagian kabupaten naik, sebagian turun wajar).
- **Kedelai (DS07)**:
  * Rata-rata produktivitas: 2018 = 9,08 ku/ha; 2019 = 10,13 ku/ha; 2020 = 10,44 ku/ha.
  * Rasio 2019 / 2018: Rerata = 1,2092, Median = 1,2143, Standar Deviasi = 0,3321.
  * *Temuan*: Fluktuasi kedelai memiliki dispersi spasial lebar ($\text{SD} = 0,33$), tidak menunjukkan lonjakan artifisial seragam.
- **Kesimpulan**: Anomali seragam tahun 2019 **hanya terjadi secara eksklusif pada komoditas padi (DS03)**.

---

## 2. Pembaruan Sitasi Standar FAO-56 & Penyesuaian Rumus $p$

1. **Penghapusan Nomor Halaman Buku**:
   * Seluruh nomor halaman fisik FAO-56 pada `rules/rules.json`, `docs/rules_register.md`, `evidence_registry.csv`, dan berkas antarmuka UI telah dihapus.
   * Format diseragamkan menjadi: **"FAO-56 Bab N, Tabel M (URL: https://www.fao.org/4/x0490e)"**.
2. **Status Rumus Penyesuaian $p$ terhadap $ET_c$**:
   * Pada naskah web resmi FAO-56 Bab 8 (`https://www.fao.org/4/x0490e/x0490e0e.htm`), rumus $p = p_{\text{Table 22}} + 0.04(5 - ET_c)$ tercantum sebagai aproksimasi numerik teks dan catatan kaki Tabel 22 tanpa nomor persamaan resmi (tidak berlabel Eq.).
   * Ditandai secara jujur pada konfigurasi limitations: **"rumus belum diverifikasi manusia (nomor persamaan belum dikonfirmasi)"**.
3. **Konfirmasi Nomor Persamaan Example 36**:
   * Dari naskah resmi FAO-56 Example 36 terkonfirmasi definitif:
     - Total Available Water: **$TAW = \text{Eq. } 82$**
     - Readily Available Water: **$RAW = \text{Eq. } 83$**

---

## 3. Pengetatan Kontrak Skema JSON (Draft 2020-12)

1. **Klausa Kondisional `if/then` yang Ketat**:
   * Diperbarui pada `schemas/engine_output.schema.json`:
     ```json
     "if": {
       "properties": {
         "status": { "const": "kondisi_stres_abiotik" }
       }
     },
     "then": {
       "properties": {
         "evidence_refs": {
           "minItems": 1,
           "contains": { "const": "RULE_WATER_FAO56_DEPLETION" }
         }
       }
     }
     ```
   * Jika status bernilai `kondisi_stres_abiotik`, array `evidence_refs` **wajib memuat ID aturan pemicunya yaitu `RULE_WATER_FAO56_DEPLETION`**.
   * Kombinasi ID FAO lain (seperti hanya mencantumkan `["FAO56_RAW_DEPLETION", "FAO56_KC_MAIZE"]` tanpa aturan pemicu) secara otomatis **DITOLAK** oleh validator schema (teruji di Pytest & Vitest).
2. **Status `kondisi_mendukung_OPT`**:
   * Dihapus dari enum `status` level atas (karena belum ada aturan OPT berstatus `VERIFIED_METHOD`).
   * Didokumentasikan sebagai status tak terjangkau di level atas; peringatan OPT dialihkan murni ke kartu tindakan `scouting_opt` berstatus `METHOD_UNCALIBRATED`.

---

## 4. Penyelarasan Aturan LWD & Transisi Kelembapan Panen

1. **`RULE_OPT_LWD_HOURLY_RH90`**:
   * Metrik diselaraskan dengan deskripsi menjadi: `daily_rh90_hours_sum` (jumlah jam per hari dengan kelembapan relatif $RH \ge 90\%$, bukan jam berturut-turut).
   * Jam-RH90 dijadikan indikator durasi kebasahan daun (`METHOD_UNCALIBRATED`).
   * Ambang batas 10 jam dipisahkan dan diberi label tegas `CONVENTION_PENDING` (*"ambang ditetapkan tim, tanpa sumber"*).
2. **Zona Transisi Kelembapan Panen 75%–85%**:
   * Menambahkan aturan baru **`RULE_HARVEST_RH_WARN`** di `rules.json` untuk menutup celah kelembapan panen:
     - $RH \le 75\% \to$ `SAFE` (`RULE_HARVEST_RH_SAFE`)
     - $75\% < RH \le 85\% \to$ `WARN` (`RULE_HARVEST_RH_WARN`, perlunya pengeringan segera pasca panen)
     - $RH > 85\% \to$ `DANGER` (`RULE_HARVEST_RH_DANGER`)

---

## 5. Uji Independen Benchmark FAO-56 Example 36 & RH Panen

Pengujian independen perhitungan $TAW = 1000 \times (\theta_{FC} - \theta_{WP}) \times Z_r$ dan $RAW = p \times TAW$ dilakukan pada 3 tekstur tanah terhadap Example 36 FAO-56 (toleransi $\le 1\text{ mm}$):

1. **Loamy Sand** ($\theta_{FC} = 0,15; \theta_{WP} = 0,06 \implies 90\text{ mm/m}$):
   - Tomat ($Z_r = 0,8\text{ m}, p = 0,40$): Target TAW = 72 mm, RAW = 29 mm $\implies$ Terhitung TAW = 72,0 mm, RAW = 28,8 mm $\to$ **PASS**.
   - Jagung ($Z_r = 1,2\text{ m}, p = 0,55$): Target TAW = 108 mm, RAW = 59 mm $\implies$ Terhitung TAW = 108,0 mm, RAW = 59,4 mm $\to$ **PASS**.
2. **Silt** ($\theta_{FC} = 0,32; \theta_{WP} = 0,15 \implies 170\text{ mm/m}$):
   - Tomat: Target TAW = 136 mm, RAW = 54 mm $\implies$ Terhitung TAW = 136,0 mm, RAW = 54,4 mm $\to$ **PASS**.
   - Jagung: Target TAW = 204 mm, RAW = 112 mm $\implies$ Terhitung TAW = 204,0 mm, RAW = 112,2 mm $\to$ **PASS**.
3. **Silty Clay** ($\theta_{FC} = 0,35; \theta_{WP} = 0,23 \implies 120\text{ mm/m}$):
   - Tomat: Target TAW = 96 mm, RAW = 38 mm $\implies$ Terhitung TAW = 96,0 mm, RAW = 38,4 mm $\to$ **PASS**.
   - Jagung: Target TAW = 144 mm, RAW = 79 mm $\implies$ Terhitung TAW = 144,0 mm, RAW = 79,2 mm $\to$ **PASS**.
4. **Uji RH Panen 80% (Zona 75–85%)**:
   - Teruji menghasilkan status `Perlu Waspada` (WARN) dan memicu `RULE_HARVEST_RH_WARN` $\to$ **PASS**.

---

## 6. Transparansi Evaluasi LLM (Guardrail Templat)

- **Pernyataan Kejujuran Metodologi**: Skrip pengujian `scripts/test_template_guardrails.py` **BUKAN pemanggilan API model LLM sungguhan** (tidak memanggil endpoint OpenAI/Anthropic langsung). Skrip ini adalah simulasi aturan guardrail templat deterministik untuk menguji apakah respons templat mampu mematuhi batas larangan sistem prompt.
- Frasa *"zero-tolerance terhadap halusinasi"* dan *"100% patuh"* telah **dihapus bersih**.
- Hasil pengujian disimpan secara objektif di `reports/phase13_template_guardrail_results.json` (10/10 kasus pengujian batas lulus kriteria aturan).

---

## 7. Kutipan Langsung Nilai $K_c$ FAO-56 Tabel 12 & Koreksi Iklim

Kutipan verbatim langsung dari naskah resmi FAO-56 Bab 6 (`https://www.fao.org/4/x0490e/x0490e0b.htm#tabulated%20kc%20values`):

| Komoditas di Tabel 12 | $K_{c,\text{ini}}$ | $K_{c,\text{mid}}$ | $K_{c,\text{end}}$ | Catatan Kaki Resmi Tabel 12 | Nilai di `rules.json` | Selisih |
| :--- | :---: | :---: | :---: | :--- | :---: | :---: |
| **Maize, Field (grain)** | 0,30 | 1,20 | 0,60–0,35 | Footnote 11: *"First value is for harvest at high moisture; second value is for harvest after drying in field."* | 0,30 / 1,20 / 0,35 (kering) & 0,60 (basah) | **0,00** |
| **Soybeans** | 0,40 | 1,15 | 0,50 | Nilai tunggal panen polong kering standar | 0,40 / 1,15 / 0,50 | **0,00** |
| **Tomato** | 0,60 | 1,15 | 0,70–0,90 | Tabel 12 tidak memiliki catatan kaki untuk Tomato; nilai 0,80 adalah titik tengah pilihan tim (`CONVENTION_PENDING`) | 0,60 / 1,15 / 0,80 (pilihan tim titik tengah) | **0,00** |

*Catatan Batasan Iklim Ditambahkan ke Engine*: Nilai $K_{c,\text{mid}}$ dan $K_{c,\text{end}}$ pada Tabel 12 FAO-56 berlaku secara khusus untuk kondisi iklim sub-humid dengan kelembapan relatif minimum siang hari $RH_{\min} \approx 45\%$ dan kecepatan angin $u_2 \approx 2\text{ m/s}$. Formula koreksi iklim lokal (FAO-56 Eq. 62 & Eq. 65) belum diterapkan ke dalam engine saat ini.

---

## 8. Penyatuan Kode Engine Menjadi Single Source of Truth

- Kode implementasi engine TypeScript murni disatukan secara definitif di repositori web:  
  **`taniadapt-web/src/lib/engine/`** (`fao56.ts`, `kc.ts`, `waterBalance.ts`, `percentile.ts`, `rules.ts`, `engine.ts`, `types.ts`).
- Folder duplikat `src/lib/engine/` di repositori riset telah dihapus bersih.
- Repositori riset menggunakan skrip sinkronisasi kanonik `scripts/sync_engine_to_web.py`.
- Integritas keselarasan diproteksi secara otomatis melalui unit test Pytest `test_engine_code_single_source_hash_parity` yang memverifikasi bahwa hash SHA256 berkas `rules.json` dan `engine_output.schema.json` di kedua direktori identik 100%.

---

## 9. Ringkasan Pengujian Akhir & Status Repositori

| Test Suite | File Pengujian | Jumlah Test | Lulus | Gagal | Status |
|---|---|:---:|:---:|:---:|:---:|
| **Python Pytest** | `tests/test_engine_schema_and_rules.py` | 11 | 11 | 0 | **100% PASS** |
| **TypeScript Vitest** | `taniadapt-web/tests/engine.test.ts` | 17 | 17 | 0 | **100% PASS** |
| **Guardrail Templat** | `scripts/test_template_guardrails.py` | 10 | 10 | 0 | **100% PASS** |
| **Next.js Web Build** | `npm run build` di `taniadapt-web` | 8 routes | 8 | 0 | **100% PASS** |

### Daftar Item PENDING_HUMAN yang Tersisa:
1. **`bps_manual_input.csv`**: Konfirmasi nama fisik berkas PDF publikasi BPS JDA 2016–2020.
2. **`sumber-dan-batasan/page.tsx`**: Verifikasi teks sitasi AgERA5 CDS dan identitas Satu Data Jabar.
3. **Dokumen Keputusan Komoditas**: `docs/crop_outcome_decision.md` berstatus `PENDING_HUMAN`.

---

## 10. Tag Git Resmi
- **Tag Baru:** **`phase13-m2-verified`** (menggantikan milestone sebelumnya tanpa memindahkan tag lama).
- Tag lama tetap utuh: `audit-v3`, `phase4-close-candidate`, `v2-audit-closure`, `phase12-honest-status`, `phase13-gate-ready`, `bps-verified-partial`, `phase13-m1-engine`, `phase13-m1-research`.
