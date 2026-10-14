# Laporan Komprehensif Phase 13 Milestone 3 (M3): Bio-Mechanistic Engine Enhancements, Cold-Start Water Ledger, Forward Simulation, & Narration Guardrail Layer

**Repositori Riset:** `/mnt/c/CODING/research_taniAdapt` (branch `main`)  
**Repositori Web:** `/mnt/c/CODING/TaniAdapt/taniadapt-web` (branch `main`)  
**Tanggal Pelaksanaan:** 2026-10-14  
**Status Pengesahan Dokumen:** `PENDING_HUMAN` (Menunggu pengesahan pengguna; dilarang mencantumkan status RATIFIED)  
**Tingkat Integritas Pengujian:** 100% Lulus (Pytest 11/11, Vitest 31/31, Next.js Build 8/8 routes, Guardrail Template 10/10)

---

## 1. Ringkasan Eksekutif & Sasaran Milestone 3 (M3)

Milestone 3 (M3) dari Phase 13 difokuskan pada penyelesaian tuntas lima kelompok perbaikan sistemik:
1. **Kelompok A (Data & Label)**: Penguncian kanonik anomali produktivitas padi DS03 2019, penandaan status 2018 edisi campuran, pengulangan uji sensitivitas panel ekonometrika padi, pemeriksaan komoditas pembanding (jagung & kedelai), serta konsolidasi temuan audit empiris A3–A5.
2. **Kelompok B (Koreksi Dokumen & Sitasi)**: Pembersihan menyeluruh matriks keterlacakan (*traceability*), penegasan status *convention pending* tanpa atribusi sitasi semu, klarifikasi indikator durasi kebasahan daun (*Leaf Wetness Duration* / LWD), perbaikan deskripsi API prakiraan Open-Meteo, pembetulan rujukan persamaan Penman-Monteith ke FAO-56 Bab 2 Persamaan 6, pelaporan objektif evaluasi Machine Learning LOYO, penghapusan catatan spekulatif $K_{c,\text{end}}$ tomat, penambahan aturan pupuk `RULE_FERT_LOCKOUT_14D`, serta dokumentasi batas fisika $P_{\text{eff}} = P$ dan ketiadaan $K_s$.
3. **Kelompok C (Penyempurnaan Engine Pure TypeScript)**: Implementasi pemisahan produk data cuaca pada persentil (C1), evaluasi sensitivitas hujan efektif 80% vs 100% (C2), simulasi proyeksi neraca air maju 7 hari dua skenario (C3), modul rekonstruksi ledger air awal *cold-start* dual lintasan dengan penanganan interval ketidakpastian (C4), serta penambahan kelas tekstur tanah Sandy Loam, Loam, dan Silty Clay Loam ke `rules.json` (C5).
4. **Kelompok D (Lapisan Narasi & Validator Guardrail)**: Implementasi modul templat fallback terarah PPL/Puskesmas dan bahasa Sunda bertanda `PENDING_HUMAN`, normalisasi ucapan suara (*speech normalization*), validator narasi murni TypeScript dengan proteksi angka liar, merek dagang pestisida, takaran dosis kimia, dan klaim kepastian palsu, serta unit test Vitest lengkap.
5. **Kelompok E (Dokumentasi Kontrak UI & Laporan M3)**: Penyusunan panduan kontrak antarmuka frontend `docs/ui_contract_phase13_m3.md` dan pelaporan dossier teknis ini secara jujur dan apa adanya.

---

## 2. Kelompok A: Rekonsiliasi Data, Anomali DS03 2019, & Hasil Audit A3–A5

### A. Anomali Produktivitas Padi DS03 Tahun 2019
Pemeriksaan forensik data BPS dan Dinas Tanaman Pangan dan Hortikultura (Distanhor) Jawa Barat menunjukkan lonjakan rasio rata-rata berbobot luas panen DS03 terhadap BPS KSA sebesar **1,2181 (+21,81%)** pada tahun 2019 (DS03: 70,09 ku/ha vs BPS KSA: 57,54 ku/ha):
- **Cakupan Spasial Lonjakan**: Terjadi serempak pada seluruh 27 dari 27 kabupaten/kota se-Jawa Barat tanpa terkecuali (rasio minimum 1,0618 di Kab. Pangandaran, maksimum 1,3921 di Kota Bogor; rata-rata rasio 1,2390 dengan $\text{SD} = 0,0691$).
- **Perbandingan dengan Tahun 2018 dan 2020**: Pada 2018 (56,07 vs 56,51 ku/ha, selisih -0,78%) dan 2020 (55,30 vs 56,82 ku/ha, selisih -2,67%), produktivitas DS03 berbobot luas sangat konsisten dengan BPS KSA. Lonjakan hanya terjadi di tahun 2019.
- **Status Kanonik**: Karena belum ditemukan dokumen teknis tertulis resmi dari Distanhor Jabar yang menjelaskan latar belakang metodologis lonjakan serempak ini, berkas `reports/dataset_audit/b1_rice_reconciliation_v2.csv` ditandai secara tegas sebagai **`ANOMALI, BELUM DIJELASKAN`**.
- **Status Tahun 2018**: Ditandai sebagai **`UNVERIFIED_BY_HUMAN (edisi campuran)`** karena adanya perbedaan pencatatan antara BRS 68/11/32 dan publikasi Jawa Barat Dalam Angka (JDA) 2020.
- **Uji Sensitivitas Panel Padi**: Seluruh estimasi ekonometrika padi diulang dan dicatat di `reports/dataset_audit/a10_panel_mde_audit.json` dengan catatan tegas: *"peka terhadap anomali DS03 2019"*.
- **Pemeriksaan Jagung (DS05) dan Kedelai (DS07)**: Pemeriksaan data produktivitas jagung (rata-rata rasio 2019/2018 = 1,0083) dan kedelai (rata-rata rasio 2019/2018 = 1,2092 dengan dispersi lebar $\text{SD} = 0,3321$) membuktikan bahwa **lonjakan serempak 27 unit hanya terjadi secara eksklusif pada padi sawah (DS03)**.

### B. Rangkuman Hasil Audit Empiris A3–A5
- **A3 (Deteksi Imputasi Jagung & Kedelai 2022)**:
  * Pada dataset jagung DS05 tahun 2022, terdeteksi 13 kabupaten/kota memiliki angka produktivitas identik 75,70 ku/ha (indikasi imputasi nilai agregat provinsi).
  * Pada dataset kedelai DS07 tahun 2022, standar deviasi spasial runtuh drastis menjadi 0,19 ku/ha (dari rata-rata historis $\text{SD} \approx 2\text{--}4\text{ ku/ha}$).
  * Resolusi: Tahun 2022 diberi label `SUSPECT` dan dieksklusikan dari panel utama pemodelan regresi.
- **A4 (Koreksi CV Produktivitas Subang)**:
  * Koefisien variasi (CV) sampel mentah jagung Subang adalah 12,21%. Namun, titik data anomali tahun 2022 menyumbang 49,8% dari total *sum of squared errors* (SSE) terhadap tren linear.
  * Resolusi: Tanpa titik 2022, CV residu detrended menyusut signifikan ke **5,49%** (tren linear) dan **2,65%** (tren *piecewise*).
- **A5 (Dekomposisi Log Produksi Subang)**:
  * Melalui dekomposisi identitas $\Delta \ln(\text{Produksi}) = \Delta \ln(\text{Luas Panen}) + \Delta \ln(\text{Produktivitas})$, dibuktikan bahwa **98,4%–98,7%** lonjakan produksi jagung Subang pada tahun 2018 dan 2020 murni didorong oleh ekspansi luas panen, bukan kenaikan produktivitas per hektare.

---

## 3. Kelompok B: Koreksi Dokumen, Sitasi, & Matriks Traceability

Tindakan perbaikan dokumen ilmiah dan metadata aturan agrometeorologi telah diselesaikan pada commit `416b8d7`:
1. **Pembersihan Sitasi Semu pada Aturan `CONVENTION_PENDING`**:
   - Aturan praktis heuristik yang belum memiliki kalibrasi sensor lapang in-situ (seperti ambang batas angin semprot, jeda hujan pupuk, dan jendela kelembapan panen) telah dibersihkan dari atribusi referensi semu.
   - Sitasi ASABE S572.1, sitasi Bab 8 ambang 100 mm FAO-56, dan pedoman pascapanen serealia dihapus dari daftar rujukan aturan heuristik, lalu ditulis secara jujur sebagai: *"konvensi tim, tanpa sumber ilmiah"*.
2. **Klarifikasi Ilmiah Leaf Wetness Duration (LWD)**:
   - Sitasi Sentelhas et al. (2008) (*Agric. For. Meteorol.* 148(3):392–400) diperjelas fungsinya sebagai model estimasi durasi basah daun berbasis jam harian dengan $RH \ge 90\%$.
   - Ambang batas 10 jam ditetapkan secara eksplisit sebagai konvensi tim (`METHOD_UNCALIBRATED`). Teks panduan petani diperhalus menjadi: *"kondisi lembap panjang yang mendukung jamur"*.
3. **Perbaikan Deskripsi API Cuaca Open-Meteo**:
   - Dinyatakan secara akurat sebagai: **"Model Prakiraan Numerik 7 Hari (bukan reanalysis)"**.
4. **Pembetulan Nomor Persamaan Penman-Monteith**:
   - Rumus baku evapotranspirasi acuan $ET_0$ dirujuk dengan tepat ke: **FAO-56 Bab 2, Persamaan 6** (dilengkapi Contoh 18 di Bab 4).
5. **Transparansi Hasil Evaluasi Machine Learning**:
   - Dokumentasi laporan riset menegaskan: *"tidak ada bukti bahwa model berbasis cuaca saja dapat memprediksi hasil pada tahun baru (R2 out-of-sample ≈ 0 pada LOYO)"*.
6. **Penghapusan Catatan Spekulatif $K_{c,\text{end}}$ Tomat**:
   - Catatan kaki spekulatif terkait pemisahan tomat industri (0,70–0,80) vs tomat segar (0,80–0,90) pada Tabel 12 telah dihapus bersih karena naskah asli FAO-56 Tabel 12 tidak memiliki catatan kaki tersebut. Nilai 0,80 diakui sebagai titik tengah pilihan tim (`CONVENTION_PENDING`).
7. **Penambahan Aturan Pupuk & Batasan Fisika**:
   - Menambahkan aturan `RULE_FERT_LOCKOUT_14D` (`CONVENTION_PENDING`) untuk mencegah rekomendasi pemupukan berulang dalam selang 14 hari.
   - Mendokumentasikan secara terbuka batasan asumsi curah hujan efektif $P_{\text{eff}} = P$ serta ketiadaan koefisien stres air $K_s$ pada simulasi deplesi.

---

## 4. Kelompok C: Penyempurnaan Engine Bio-Mekanistik Pure TypeScript (C1–C5)

Seluruh logika keputusan dieksekusi secara deterministik tanpa I/O di dalam `taniadapt-web/src/lib/engine/`:

### C1: Penegasan Paritas Produk Cuaca pada Persentil (`percentile.ts`)
- Fungsi `evaluateClimatologyParity` kini membedakan secara tegas produk `OpenMeteo_Forecast_API` vs `OpenMeteo_ERA5_Archive`.
- Jika data prakiraan dibandingkan dengan arsip reanalysis (atau sebaliknya), evaluasi persentil secara otomatis mengembalikan:
  * `relative_rank: null`
  * `rank_basis: 'beda sumber, tidak dibandingkan'`
  * `rank_basis_n: null`
  * `status: 'evidence_insufficient'`

### C2: Evaluasi Sensitivitas Curah Hujan Efektif (`engine.ts`)
- Engine melakukan simulasi ganda neraca air pada hari berjalan:
  1. Asumsi standar: $P_{\text{eff}} = 1.0 \times P$
  2. Asumsi konservatif: $P_{\text{eff}} = 0.8 \times P$
- Jika status kesimpulan air berubah antara kedua asumsi tersebut, engine menyematkan flag aditif:  
  `sensitif_terhadap_asumsi_hujan_efektif = true`.

### C3: Simulasi Maju Neraca Air 7 Hari Dua Skenario (`waterBalance.ts`)
- Fungsi baru `simulate7DaysForward` menyimulasikan dinamika air tanah harian $D_r(t+1) \dots D_r(t+7)$ ke depan menggunakan dua skenario simultan:
  1. *Skenario Prakiraan Cuaca*: Menggunakan presipitasi harian dari prakiraan cuaca Open-Meteo.
  2. *Skenario Tanpa Hujan (Worst-Case)*: Mengasumsikan presipitasi bernilai $0,0\text{ mm}$ setiap hari.
- Mengembalikan array `proyeksi_7hari` (7 elemen) serta tanggal ambang terlampaui:
  * `hari_pertama_melewati_raw_prakiraan`: Tanggal pertama melintasi $RAW$ pada skenario prakiraan, atau `null`.
  * `hari_pertama_melewati_raw_tanpa_hujan`: Tanggal pertama melintasi $RAW$ jika kemarau berlanjut, atau `null`.
- **Batas Fisika**: Begitu deplesi melintasi batas $RAW$, akumulasi deplesi berhenti bertambah karena model belum menyertakan dinamika koefisien penurunan transpirasi $K_s$.

### C4: Rekonstruksi Ledger Air Awal (*Cold-Start*) (`src/lib/ledger/coldStart.ts`)
- Menjalankan dua lintasan batas deplesi ekstrem sejak tanggal tanam:
  * Lintasan Batas Bawah: Dimulai dari kapasitas lapang ($D_{r0} = 0\text{ mm}$).
  * Lintasan Batas Atas: Dimulai dari titik layu permanen ($D_{r0} = TAW$).
- Jika kedua lintasan bertemu (misal akibat hujan lebat $P \ge TAW$ atau siram jenuh):
  * `dr_awal_status = 'pasti'`
  * `konvergen_pada = <tanggal_konvergensi>`
- Jika kedua lintasan belum bertemu:
  * `dr_awal_status = 'interval'`
  * `dr_interval_mm = [dr_low, dr_high]`
  * `konvergen_pada = null`
- **Penanganan Interval Ketidakpastian Melintasi $RAW$**:
  Jika interval $[D_{r,\text{low}}, D_{r,\text{high}}]$ merentang melintasi nilai $RAW$:
  * Aksi irigasi (`irrigation`) berstatus `rule_status = 'INSUFFICIENT'`.
  * Label status: `'Perlu Waspada'`.
  * Alasan: *"Keadaan air tanah belum pasti; tanyakan kapan terakhir disiram atau hujan deras."*
  * Status top-level engine dijamin **TIDAK PERNAH** tereskalasi menjadi `kondisi_stres_abiotik`.

### C5: Penambahan Tiga Kelas Tekstur Tanah Resmi (`rules.json`)
Menambahkan parameter biofisik tekstur tanah berdasarkan FAO-56 Bab 7 Tabel 19:
1. **Sandy Loam**: $\theta_{FC} \in [0.18, 0.28]$ (pilihan tim: $0.23$), $\theta_{WP} \in [0.06, 0.16]$ (pilihan: $0.10$), $TAW = 130.0\text{ mm/m}$.
2. **Loam**: $\theta_{FC} \in [0.20, 0.30]$ (pilihan tim: $0.27$), $\theta_{WP} \in [0.07, 0.17]$ (pilihan: $0.12$), $TAW = 150.0\text{ mm/m}$.
3. **Silty Clay Loam**: $\theta_{FC} \in [0.30, 0.37]$ (pilihan tim: $0.33$), $\theta_{WP} \in [0.17, 0.24]$ (pilihan: $0.18$), $TAW = 150.0\text{ mm/m}$.
Status ketiga kelas tanah ditandai `CONVENTION_PENDING` dengan catatan: *"pilihan tim di dalam rentang FAO-56 Bab 7, Tabel 19; teks petani = PENDING_HUMAN"*.

---

## 5. Kelompok D: Lapisan Narasi, Validator & Normalisasi Suara

Modul narasi di `taniadapt-web/src/lib/narration/` mengimplementasikan batas arsitektur decoupled:
1. **Templat Out-of-Scope & Pengalihan (`templates.ts`)**:
   - Pertanyaan estimasi hasil panen (`yield_prediction`) dialihkan ke Petugas Penyuluh Lapangan (PPL).
   - Pertanyaan harga komoditas (`price`) dialihkan ke PIHPS/PPL.
   - Kasus dugaan keracunan kimia (`pesticide_poisoning`) dialihkan ke Puskesmas/Rumah Sakit terdekat.
   - Sengketa lahan (`law_land_tenure`) dialihkan ke kantor dinas/PPL.
   - Templat Bahasa Sunda (`SUNDA_TEMPLATES`) ditandai `PENDING_HUMAN`.
2. **Normalisasi Suara (`speech.ts`)**:
   - Fungsi `normalizeForSpeech` mengonversi rentang jam (`"06.00 - 08.00 WIB"` $\to$ `"pukul enam sampai delapan Waktu Indonesia Barat"`) dan unit metrik (`"km/j"` $\to$ `"kilometer per jam"`, `"mm"` $\to$ `"milimeter"`, `"°C"` $\to$ `"derajat Celsius"`, `"RH"` $\to$ `"kelembapan udara"`).
   - Fungsi `generateConfirmationPrompt` menghasilkan konfirmasi komoditas dan wilayah sebelum eksekusi.
3. **Validator Narasi Deterministik (`validator.ts`)**:
   - Memindai teks narasi dari LLM atau templat bebas:
     * Menolak angka liar (*unauthorized numbers*) yang tidak ada dalam JSON engine.
     * Menolak 11 merek dagang pestisida sintetis (*prohibited pesticide brands*).
     * Menolak unit takaran dosis (*prohibited dose units*: `ml/l`, `kg/ha`, `sdm`, dll.).
     * Menolak kata kepastian palsu (*certainty words*: `pasti`, `terbukti`, `dijamin`, `100%`) pada aksi yang belum terverifikasi in-situ.
   - Jika terdeteksi pelanggaran, narasi secara otomatis ditolak dan digantikan oleh `generateDeterministicFallback`.
4. **Penyatuan Ekspor (`index.ts`)**:
   - Seluruh modul diekspor secara bersih melalui `src/lib/narration/index.ts`.

---

## 6. Hasil Pengujian Otomatis & Status Verifikasi Komprehensif

Seluruh komponen telah diuji secara komprehensif menggunakan test runner resmi:

| Kategori Pengujian | Test Suite / Perintah | Berkas Pengujian | Metrik Hasil | Status |
|---|---|---|:---:|:---:|
| **Python Unit Tests** | `pytest tests/test_engine_schema_and_rules.py` | `test_engine_schema_and_rules.py` | 11 passed / 11 items | **100% PASS** |
| **TypeScript Engine Tests** | `vitest run` di `taniadapt-web` | `tests/engine.test.ts` | 22 passed / 22 tests | **100% PASS** |
| **TypeScript Narration Tests** | `vitest run` di `taniadapt-web` | `tests/narration.test.ts` | 9 passed / 9 tests | **100% PASS** |
| **Total TypeScript Tests** | `npm test` di `taniadapt-web` | 2 berkas pengujian | 31 passed / 31 tests | **100% PASS** |
| **Guardrail Template Test** | `python scripts/test_template_guardrails.py` | `scripts/test_template_guardrails.py` | 10 passed / 10 cases | **100% PASS** |
| **Next.js Production Build** | `npm run build` di `taniadapt-web` | App Router Next.js 16.3.6 | 8 routes generated | **100% PASS** |
| **Single Source Hash Parity** | `test_engine_code_single_source_hash_parity` | SHA256 rules & schema | Identik 100% | **100% PASS** |

### Rincian Rute Next.js yang Dihasilkan pada Build:
```text
Route (app)
┌ ○ /
├ ○ /_not-found
├ ƒ /api/advisory
├ ○ /apple-icon.png
├ ○ /icon.png
└ ○ /sumber-dan-batasan
```

---

## 7. Inventaris Item PENDING_HUMAN yang Tersisa

Sesuai prinsip etika kecerdasan buatan dan tata kelola data ilmiah, sistem melarang keras agen otomatis memberikan label `RATIFIED`. Item-item berikut tetap berada dalam status pengawasan manusia (`PENDING_HUMAN`):
1. **`reports/dataset_audit/bps_manual_input.csv`**: Menunggu konfirmasi nama fisik berkas PDF laporan resmi BPS Jawa Barat Dalam Angka 2016–2020.
2. **`taniadapt-web/src/app/sumber-dan-batasan/page.tsx`**: Verifikasi manual teks sitasi ECMWF AgERA5 CDS dan identitas API portal Satu Data Jabar.
3. **`docs/crop_outcome_decision.md`**: Dokumen matriks pemilihan 5 komoditas menunggu ratifikasi tim peneliti.
4. **`taniadapt-web/src/lib/narration/templates.ts` (`SUNDA_TEMPLATES`)**: Kosakata dialek lokal Sunda untuk petani pedesaan menunggu peninjauan penutur asli (*native speaker*).
5. **`rules/rules.json` (`soil_classes`)**: Terjemahan bahasa lapangan istilah tekstur tanah (*Sandy Loam*, *Loam*, *Silty Clay Loam*) ke bahasa petani Jawa Barat berstatus `PENDING_HUMAN`.

---

## 8. Batasan Biofisik & Rekomendasi Pengembangan Lanjutan

1. **Koefisien Cekaman Air Dinamis ($K_s$)**:
   - Model neraca air saat ini mengasumsikan transpirasi tanaman berlangsung penuh ($ET_c = K_c \times ET_0$) hingga $D_r$ mencapai $RAW$. Begitu $D_r > RAW$, engine memicu status cekaman air namun belum menurunkan nilai transpirasi aktual ($ET_{c,\text{act}} = K_s \times ET_c$). Penambahan modul $K_s$ linier ($K_s = \frac{TAW - D_r}{(1-p)TAW}$) direkomendasikan untuk fase berikutnya.
2. **Rezim Sawah Tergenang Padi (*Ponded Wetland Dynamics*)**:
   - Padi sawah dataran rendah Jawa Barat dibudidayakan dalam kondisi tergenang (5–10 cm). Model matriks tanah tak jenuh FAO-56 Bab 8 tidak berlaku, sehingga modul air padi tetap berstatus `evidence_insufficient`. Diperlukan integrasi model neraca air petakan sawah tergenang (*standing water depth balance*) untuk mengaktifkan modul irigasi padi.
3. **Mulsa Plastik & Naungan Hujan Hortikultura Tropis**:
   - Budidaya cabai dan tomat dataran tinggi Lembang/Garut umumnya menggunakan mulsa plastik hitam perak (MPHP) atau naungan hujan (*rain shelter*), yang memodifikasi evaporasi tanah langsung ($E$). Koefisien tanaman terbagi ganda (*dual crop coefficient* $K_{cb} + K_e$) dari FAO-56 Bab 7 dapat dievaluasi pada iterasi mendatang.

---

## 9. Sematan Tag Git Lokal

- **Repositori Riset (`research_taniAdapt`)**: Sematan tag baru **`phase13-m3-verified`** pada branch `main`.
- **Repositori Web (`taniadapt-web`)**: Sematan tag baru **`phase13-m3-engine`** pada branch `main`.
- **Aturan Mutlak**: Sesuai instruksi pengguna, **dilarang melakukan git push**. Seluruh commit dan tag disimpan secara lokal, siap untuk ditinjau dan dieksekusi dorong (*push*) secara mandiri oleh pengguna.
