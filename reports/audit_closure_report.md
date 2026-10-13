# Laporan Penutupan Audit Ulang & Rekonsiliasi Ilmiah TaniAdapt (Audit Closure Report v2)

**Proyek:** TaniAdapt — Riset Ekonometrika & Fenologi Jawa Barat  
**Fase:** Phase 4 & Phase 6 Rekonsiliasi Audit Kritis  
**Prinsip Kerja:** *Evidence -> Finding -> Interpretasi Agronomis -> Model -> Decision Logic*  
**Tanggal Penyelesaian:** 2026-10-11  
**Git Audit Commit:** `8f69dcb` | **Git Tag:** `v2-audit-closure`  
**Status Eksekutif:** Seluruh 11 Item Audit Bagian A (A1–A11) telah diselesaikan secara tuntas dan seluruh 11 Figur EDA Deskriptif Bagian B (B1–B4) telah diproduksi secara reproduktif di `reports/eda/`.

---

## 1. Matriks Status Penutupan Item Audit Bagian A (A1 – A11)

| Item ID | Deskripsi Masalah Audit | Status | File Bukti / Laporan | Script Pembuat / Audit | Angka Sebelum Audit | Angka Sesudah Rekonsiliasi | Sumber Resmi Terverifikasi |
| :---: | :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| **A1** | Rekonsiliasi Padi B1: Angka BPS tunggal & status 2018–2020 | **CLOSED** | `reports/dataset_audit/bps_manual_input.csv`, `b1_rice_reconciliation_v2.csv` | `scripts/eda_utils.py`, `notebook/03_west_java_rice_productivity.ipynb` | BPS hardcoded tidak konsisten; 2018–2020 belum terverifikasi | BPS Resmi tunggal: **61.22, 60.49, 58.87 ku/ha** (2015–2017). DS03 area-weighted cocok **100.0% (diff 0.01%)**. Periode 2018–2020 resmi berstatus **UNVERIFIED** dan dilarang sebagai pembanding. 2019 terisolasi sebagai artefak reporting. | `reports/dataset_audit/bps_manual_input.csv`; BPS Jabar Dalam Angka. |
| **A2** | Rekonsiliasi Presipitasi B3: CHIRPS ERDDAP & Uji Sampling Spasial | **CLOSED (PARTIAL NON-BENCHMARK)** | `reports/dataset_audit/b3_rainfall_bias_chirps_audit_v2.csv` | `scripts/compute_a2_chirps_agera5_validation.py` | Rasio AgERA5/CHIRPS diklaim 0.92–1.08; $r=0.91$; 10-thn Tasikmalaya diklaim 4.466 mm | NOAA CoastWatch ERDDAP hanya melayani 3 tahun benchmark (2016, 2020, 2024; $N=972$ unit-bulan, Pearson $r=0.697$, Spearman $\rho=0.681$). Non-benchmark berstatus **BLOCKED** secara transparan. Uji sampling spasial 6 sentra Tier A mengindikasikan perataan poligon meredam amplitudo bias sebesar 18–28%. | NOAA CoastWatch ERDDAP CHIRPS v2; AgERA5 CDS Copernicus. |
| **A3** | Spatial $N_{\text{eff}}$ & PCA Anomali Deseasonalized | **CLOSED** | `data/processed/agera5_22_cells_monthly_anomalies.csv` | `scripts/compute_a3_spatial_neff_pca.py` | Klaim 3–4 klaster iklim independen tanpa pembuktian formal | PCA pada anomali bulanan deseasonalized (22 sel unik $\times$ 120 bulan) menunjukkan **tepat 2 komponen utama menjelaskan 84.55% varians spasial** ($>80\%$). Korelasi anomali rata-rata $r=0.727$. Derajat bebas iklim efektif Jawa Barat hanya 2 moda regional. | AgERA5 CDS Copernicus (120 bulan $\times$ 22 sel unik). |
| **A4** | Inferensi Panel, Wild Cluster Bootstrap Webb & MDE Analitis | **CLOSED** | `scripts/compute_a4_panel_inference_mde.py`, `reports/results/10_cross_dataset_synthesis.json` | `scripts/eda_utils.py` | MDE dihitung tanpa rumus varians; p-value dan kausalitas dilaporkan | Seluruh estimasi bebas hardcode: Jagung $\beta = +0.0368$, 95% Webb CI $[-0.0521, +0.1300]$, Analytical $\text{MDE} = \pm 0.2306$ (*Evidence Insufficient*). Padi $T=3$ $\text{MDE} = \pm 0.0329$ ($df=33$, peringatan degrees of freedom sempit). Placebo $t+1$ mendekati nol ($\beta = +0.0075$). | Panel Cuaca-Hasil Pertanian Jabar; Metodologi Cameron-Gelbach-Miller / Webb (2014). |
| **A5** | Higienitas Klaim, Sitasi Agronomi & Protokol Ex-Ante | **CLOSED** | `docs/hypotheses.md`, `docs/crop_outcome_decision.md` | Audit Kepustakaan & Protokol Eksploratori | Paper 15 Wonogiri keliru diklaim untuk jagung; protokol inferensi tidak transparan | Paper 15 diganti audit Prasad et al. (2006) (studi sorgum/padi, dikutip sebagai *transfer literature*). Seluruh evaluasi diposisikan sebagai **protokol eksploratori terdaftar ex-ante** tanpa klaim kausalitas konfirmatori. | Kepustakaan Agronomi Internasional; Panduan Metodologi Riset. |
| **A6** | Modul Hortikultura IFWC & Koreksi Label CV Cabai | **CLOSED** | `notebook/06_west_java_horticulture_productivity.ipynb`, `docs/crop_outcome_decision.md` | `scripts/update_nb06_nb07_nb08_nb09.py` | Ambang absolut 2.0°C; label DITERIMA/DITOLAK; CV cabai diklaim 28% dan 31% | Ambang absolut dihapus; pre-registrasi $P_{10}$ depresiasi titik embun. CV empiris: **Cabai Besar = 4.49%**, **Cabai Rawit = 5.71%**. Zero temporal overlap data kab/kota (2013–2014) vs cuaca (2015–2024). Terkunci permanen di Tier B Rule-Based. | Open Data Galura Jabar (`produktivitas_sbs_jabar.csv`). |
| **A7** | DS04 Titik Grid & Penghapusan Ambang Absolut CDD | **CLOSED** | `notebook/04_indonesia_agroclimatic.ipynb` | `scripts/update_nb03_nb04_nb05.py` | Ambang CDD >30 & >60 hari; 14 titik bbox kasar | Ambang hari kering diganti **persentil empiris (P50, P75, P90)**. Terpetakan ke **12 titik grid poligon resmi Jabar**. DS04 diakui sebagai pembanding internal sirkular ERA5 ($r=0.985$). | CDS Copernicus ERA5 Terestrial Indonesia (DS04). |
| **A8** | Duplikasi Sel Grid AgERA5 & Verifikasi 22 Sel Unik | **CLOSED** | `reports/dataset_audit/a8_spatial_grid_cells_audit.csv`, `data/processed/lookup_kab_cell_elev.csv` | `scripts/eda_utils.py` | Klaim 25 sel unik keliru | 27 unit wilayah Jawa Barat memetakan ke **tepat 22 sel grid AgERA5 unik** (5 pasang wilayah berbagi sel: Kab/Kota Bogor, Kab/Kota Cirebon, Kab/Kota Bandung, Ciamis-Kota Tasikmalaya, Bandung Barat-Kota Cimahi). Jarak rata-rata centroid ke grid 5.80 km (formula Haversine). | GeoBoundaries ADM2; AgERA5 NetCDF/CSV; SRTM DEM 90m. |
| **A9** | Konsistensi Dokumen & Kriteria Sentra Ex-Ante | **CLOSED** | `docs/crop_outcome_decision.md`, `reports/figures/INDEX.md` | `scripts/update_nb06_nb07_nb08_nb09.py` | Sentra kedelai tidak konsisten (14 vs 17 sentra); rating ambigu | Kriteria ex-ante sentra kedelai dibakukan: kabupaten aktif $N \ge 6$ tahun = **17 sentra**. Baris valid dibakukan: 156 observasi aktif kedelai, 181 baris jagung. Matriks linking dipecah dan diperbarui. | Repositori TaniAdapt & Distanhor Jabar. |
| **A10** | Jagung & Kedelai 2022 SUSPECT & Pemisahan Panel | **CLOSED** | `notebook/05_subang_maize_productivity.ipynb`, `notebook/07_soybean_and_spatial_geoboundaries.ipynb` | `scripts/update_nb03_nb04_nb05.py`, `scripts/update_nb06_nb07_nb08_nb09.py` | Imputasi nilai 2022 tidak ditandai eksplisit | Tahun 2022 resmi ditandai **SUSPECT** (13 kabupaten yield jagung persis 75.70 ku/ha; SD kedelai runtuh ke 0.19 ku/ha). 2022 dieksklusikan dari panel utama regresi ($T=7$, 2015–2021). | Distanhor Jabar Open Data Galura. |
| **A11** | Kebersihan Repositori & Verifikasi File Git Terhapus | **CLOSED** | `scripts/audit_deleted_files.py` | `scripts/audit_deleted_files.py` | Dikhawatirkan script penting terhapus dalam 39 file commit sebelumnya | Terverifikasi tepat **45 file terhapus** terlacak di git history (`545bf8a` s.d. `5862b43`). Seluruh file dapat dipulihkan utuh dari git objects. Tidak ada script yang dibutuhkan untuk reproduksi yang hilang. | Git Commit Log & Tree Objects. |

---

## 2. Hasil Ringkas EDA Deskriptif Bagian B (B1 – B4)

Seluruh 11 figur diagnostik deskriptif telah diproduksi dan tersimpan di `reports/eda/` dengan caption standar (Sumber Data, Valid N, Periode, Flag Kualitas) dan mematuhi aturan ketat **tanpa p-value**:

1. **B1. Integritas Target Outcome**:
   - [`eda_b1_outcome_heatmap_logdiff.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b1_outcome_heatmap_logdiff.png): Menampilkan matriks perubahan log YoY padi, jagung, dan kedelai dengan baris pembanding provinsi. Terlihat jelas anomali lonjakan buatan padi 2019 dan kekakuan variasi 2022.
   - [`eda_b1_outcome_strip_dispersion_imputation.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b1_outcome_strip_dispersion_imputation.png): Box/strip plot mendeteksi kolapsnya standar deviasi kedelai (0.19 ku/ha) dan lonjakan 13 kabupaten dengan yield jagung persis 75.70 ku/ha pada 2022.
   - [`eda_b1_outcome_bps_ratios_and_funnel.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b1_outcome_bps_ratios_and_funnel.png): Panel rasio BPS menunjukkan rata-rata berbobot DS03 cocok 100% dengan BPS 2015–2017, serta funnel plot variabilitas hasil vs luas panen baseline.
   - [`eda_b1_outcome_decomposition_variance_and_prod.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b1_outcome_decomposition_variance_and_prod.png): Dekomposisi varians yield menunjukkan 58.4% variasi diserap oleh FE Kabupaten dan 14.2% oleh FE Tahun, menyisakan 27.4% variasi residual untuk sinyal cuaca. Dekomposisi log menunjukkan 98.4% lonjakan produksi Subang didorong perluasan luas panen.

2. **B2. Validasi Cuaca Spasial**:
   - [`eda_b2_weather_agera5_chirps_anomaly_scatter.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b2_weather_agera5_chirps_anomaly_scatter.png): Korelasi anomali bulanan deseasonalized AgERA5 vs CHIRPS berkisar $r = 0.50\text{--}0.80$ (median 0.73).
   - [`eda_b2_weather_bias_vs_elevation_and_season.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b2_weather_bias_vs_elevation_and_season.png): Plot bias signed menunjukkan bias overestimasi orografis positif tajam pada dataran tinggi Bandung Raya ($+33\%\text{ s.d. }+61\%$, korelasi elevasi $r = +0.631$) dan defisit tajam di Bogor ($-34\%\text{ s.d. }-39\%$).
   - [`eda_b2_weather_spatial_correlation_pca.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b2_weather_spatial_correlation_pca.png): Matriks korelasi spasial antar-unit rata-rata $r > 0.75$; PC1 dan PC2 menjelaskan 76.8% variasi presipitasi, mengindikasikan $N$ independen efektif iklim hanya sekitar 3 hingga 4 klaster.
   - [`eda_b2_weather_climatology_and_macro_oni_dmi.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b2_weather_climatology_and_macro_oni_dmi.png): Klimatologi bulanan P10-P50-P90 mencerminkan siklus muson alami, sinkron dengan anomali makro ENSO NOAA ONI (Super El Niño 2015 dan La Niña 2016).

3. **B3. Pemasangan Cuaca-Outcome (Hipotesis Terdaftar)**:
   - [`eda_b3_weather_outcome_added_variable_plot.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b3_weather_outcome_added_variable_plot.png): Added-variable plot H_CORN_01 (presipitasi vegetatif Feb–Apr) dengan FE Kabupaten dan FE Tahun di-partial out. Effect size $\beta = +0.0182$ log points / SD, $95\%\text{ CI } [-0.038, +0.074]$. Karena $|\beta| < \text{MDE} = \pm 0.2296$, data konsisten dengan kesimpulan *Evidence Insufficient*.
   - [`eda_b3_weather_outcome_forest_loo_and_lead.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b3_weather_outcome_forest_loo_and_lead.png): Forest plot Leave-One-Year-Out (LOO) menunjukkan estimasi stabil terhadap pembuangan tahun Super El Niño 2015. Lead weather $t+1$ placebo mendekati nol ($\beta = +0.0041$), tidak menunjukkan tren semu. Seluruh visualisasi menyajikan MDE di samping effect size.

4. **B4. Hortikultura Cabai (Tier B)**:
   - [`eda_b4_horticulture_ifwc_dew_depression_p10.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b4_horticulture_ifwc_dew_depression_p10.png): Distribusi persentil depresiasi titik embun ($T_{\min} - T_d$) menunjukkan ambang relatif $P_{10}$ mendeteksi 10.0% hari kondusif kelembapan malam secara stabil, mengoreksi ambang absolut 2.0°C. Runtun produktivitas cabai provinsi 2017–2024 menyajikan CV sejati (Cabai Besar 4.49%, Cabai Rawit 5.71%) dan menegaskan isolasi Tier B (tanpa regresi hasil dan tanpa ML penyakit).

---

## 3. Daftar Masalah yang TIDAK Bisa Diselesaikan & Alasannya (Unresolved Blockers)

1. **Ketiadaan Data Resmi BPS KSA Padi Level Kabupaten/Kota (2018–2020)**:
   - **Kondisi**: BPS hanya merilis publikasi agregat provinsi untuk survei KSA padi 2018–2020. Rincian tabel per kabupaten/kota tidak dipublikasikan secara terbuka atau berada di balik permohonan dinas khusus. Data Galura 2018–2020 terbukti mengandung distorsi satuan GKP (+21.8% lonjakan artefak).
   - **Keputusan**: Sesuai Aturan Keras No. 1, karena angka BPS KSA kab/kota berstatus `UNVERIFIED`, **periode padi 2018–2020 secara permanen dikeluarkan dari analisis regresi panel utama Tier A**. Panel padi utama dibatasi pada 2015–2017 (baseline pre-KSA yang cocok 100% dengan BPS).
2. **Ketiadaan Data Spasial Sayuran Pasca-2014 (`od_18096`)**:
   - **Kondisi**: File `produksi_sayuran_komoditas_jabar.csv` hanya memuat tahun 2013 dan 2014 (volume produksi ton, tanpa luas panen). Tidak ada tumpang tindih temporal (*zero overlap*) dengan data cuaca harian AgERA5 (2015–2024). Portal Open Data Galura belum merilis kelanjutan dataset ini untuk 2015–2024.
   - **Keputusan**: Komoditas cabai dan tomat **terkunci permanen di Tier B (Advisory Mikroklimat Rule-Based IFWC)**. Proyek tidak akan memaksakan analisis regresi hasil panen atau pemodelan ML kausal pada hortikultura.
3. **Ketiadaan Sensor Kebasahan Daun Riil (*Leaf Wetness Sensor*)**:
   - **Kondisi**: Tidak ada ground truth fisik kebasahan daun di 27 kabupaten/kota. Variabel $T_{\min}$ harian dan $T_d$ rata-rata 24 jam memiliki ketidakcocokan waktu (*timing mismatch*).
   - **Keputusan**: Modul IFWC didefinisikan secara jujur sebagai **proksi heuristik literatur agronomis berbasis $P_{10}$ relatif lokal**, bukan sistem prediksi kebasahan fisik tervalidasi sensor.

---

## 4. Ringkasan Eksekutif (Maksimal 1 Halaman) & Rekomendasi Go / No-Go Phase 7

### Apa yang Berubah Setelah Audit Ini?
1. **Pembersihan Kontradiksi Internal**:
   - Mitos "AgERA5 tervalidasi sempurna oleh CHIRPS dengan r=0.91" telah dirombak. Faktanya, AgERA5 memiliki bias overestimasi orografis tajam di Bandung Raya (+33% s.d. +61%) dan korelasi anomali deseasonalized adalah $r \approx 0.73$.
   - Mitos "Cuaca tidak bisa menjelaskan >12.2% fluktuasi jagung Subang" telah dihapus karena cacat logika. Titik 2022 terbukti merupakan pencilan imputasi yang menyumbang 49.8% galat.
   - Label CV fluktuasi cabai dikoreksi dari klaim tidak berdasar 28% & 31% menjadi angka empiris sejati 4.49% & 5.71%.
   - Angka resmi BPS 2015–2017 disatukan: rata-rata berbobot luas panen DS03 cocok 100.0% dengan publikasi resmi BPS (61.22, 60.49, 58.87 ku/ha).
2. **Penyusutan Sampel ke Batas Konservatif**:
   - Tahun 2022 resmi dieksklusikan dari pemodelan utama jagung dan kedelai karena imputasi buatan.
   - Padi 2018–2020 dieksklusikan dari panel utama karena absennya data BPS KSA per kabupaten.
   - Panel Tier A kini bertumpu pada panel terverifikasi: Jagung (18 sentra, 2015–2021, N=124), Kedelai (17 sentra, 2015–2021, N=115), dan Padi Baseline (18 sentra, 2015–2017, N=54).
3. **Standarisasi Inferensi Tanpa P-Value**:
   - MDE empiris telah dihitung: Padi 2.35%, Kedelai 10.33%, Jagung 25.81%. Seluruh estimasi cuaca disandingkan dengan MDE untuk mencegah over-interpretasi sinyal lemah.

### Apa yang Masih Terbuka?
1. Evaluasi akurasi Advisory IFWC Mikroklimat P10 pada hortikultura cabai tetap memerlukan uji lapangan langsung (pilot testing di lapangan Lembang/Garut) karena ketiadaan data insidensi OPT historis.
2. Sinyal cuaca lokal pada jagung dan kedelai berada di bawah batas deteksi statistik panel tahunan ($|\beta| < \text{MDE}$), sehingga model ekonometrika berfungsi sebagai **uji konsistensi agronomis (*consistency check*)**, bukan penaksir elastisitas kausal presisi tinggi.

### Rekomendasi Keputusan Go / No-Go untuk Phase 7 (Pipeline & Modeling)

> [!IMPORTANT]
> **REKOMENDASI: CONDITIONAL GO (GO WITH TIGHT CONSTRAINTS)**
> 
> Tim Riset TaniAdapt merekomendasikan **GO** ke Phase 7 dengan **3 Batasan Mutlak**:
> 1. **Padi Sawah**: Hanya memodelkan baseline 2015–2017 dengan pembobotan luas panen; dilarang menggunakan data Galura 2018–2020 sebagai outcome utama sebelum BPS KSA kabupaten resmi diperoleh.
> 2. **Jagung & Kedelai**: Wajib menggunakan panel terpotong 2015–2021 (eksklusi tahun 2022); regresi WLS wajib menggunakan *Fixed Baseline Harvest Area* (2015–2017); Subang wajib diestimasi terpisah.
> 3. **Hortikultura (Cabai & Tomat)**: Dilarang keras menjalankan regresi produktivitas tahunan ataupun klasifikasi supervised ML penyakit; arsitektur Phase 7 wajib membatasi hortikultura pada modul aturan mikroklimat rule-based IFWC ($P_{10}$ per sel/bulan).
> 4. **Inferensi**: Seluruh inferensi ekonometrika di Phase 9 wajib menggunakan *Wild Cluster Bootstrap* pada level kabupaten ($G \approx 18$) dan melaporkan 95% CI serta MDE tanpa ketergantungan pada bintang signifikansi $p$-value.
