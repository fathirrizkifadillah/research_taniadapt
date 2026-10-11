# Laporan Penutupan Audit Ulang & Rekonsiliasi Ilmiah TaniAdapt (Audit Closure Report v2)

**Proyek:** TaniAdapt — Riset Ekonometrika & Fenologi Jawa Barat  
**Fase:** Phase 4 & Phase 6 Rekonsiliasi Audit Kritis  
**Prinsip Kerja:** *Evidence -> Finding -> Interpretasi Agronomis -> Model -> Decision Logic*  
**Tanggal Penyelesaian:** 2026-10-11  
**Status Eksekutif:** Seluruh 11 Item Audit Bagian A (A1–A11) telah diselesaikan secara tuntas dan seluruh 11 Figur EDA Deskriptif Bagian B (B1–B4) telah diproduksi secara reproduktif di `reports/eda/`.

---

## 1. Matriks Status Penutupan Item Audit Bagian A (A1 – A11)

| Item ID | Deskripsi Masalah Audit | Status | File Bukti / Laporan | Script Pembuat / Audit | Angka Sebelum Audit | Angka Sesudah Rekonsiliasi | Sumber Resmi Terverifikasi |
| :---: | :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| **A1** | Rekonsiliasi Padi B1: Dua versi angka BPS 2015–2017 & artefak 2019 | **CLOSED** | `reports/dataset_audit/b1_rice_reconciliation_v2.csv` | `scripts/audit_b1_rice_reconciliation_v2.py` | BPS: 56.2/56.4/56.6 (nb03); 60.19/59.58/57.47 (unweighted DS03) | BPS Resmi: **61.22, 60.49, 58.87 ku/ha**. Area-weighted DS03 cocok **100.0% (diff 0.00%)**. 2019 rasio loncat ke 1.2181 (+21.8% artefak GKP). Padi ladang 2019 melonjak +55.1%. | *Provinsi Jawa Barat Dalam Angka 2016–2018* (Tabel 5.1.1); BPS KSA Nasional 2019. Padi 2018–2020 dikeluarkan dari panel utama. |
| **A2** | Rekonsiliasi Presipitasi B3: Narasi AgERA5 vs CHIRPS bertentangan | **CLOSED** | `reports/dataset_audit/b3_rainfall_bias_chirps_audit_v2.csv` | `scripts/audit_b3_rainfall_bias_chirps_v2.py`, `scripts/clean_notebook_09.py` | Rasio AgERA5/CHIRPS diklaim 0.92–1.08; $r=0.91$; Tasikmalaya diklaim mean 10-thn 4.466 mm | Mean Tasikmalaya 4.465,7 mm adalah **mean 3 tahun benchmark (2016, 2020, 2024)**. Deseasonalized Pearson $r = 0.50\text{--}0.80$ (median 0.73). Bandung Raya overestimasi $+33\%\text{ s.d. }+61\%$. Bogor underestimasi $-34\%\text{ s.d. }-39\%$. Elevasi vs bias $r=+0.631$. Kolom dibakukan: `lokasi`. | NOAA CPC ONI; NOAA CoastWatch ERDDAP CHIRPS v2 Daily 0.05°; AgERA5 CDS Copernicus. |
| **A3** | Jagung & Kedelai 2022: Dugaan imputasi nilai seragam | **CLOSED** | `reports/source_log.md`, `log_inkonsistensi.md` | `scripts/generate_eda_figures.py` (Fig B1.2) | Jagung 2022 6 unit identik; kedelai SD 0.19 ku/ha | Terbukti **13 kabupaten/kota** memiliki yield jagung persis **75.70 ku/ha**. Kedelai SD 0.19 ku/ha. Tahun 2022 ditandai **SUSPECT** dan dieksklusikan dari panel utama. Subang CV residu turun dari 12.21% ke 5.49% tanpa 2022. | Distanhor Jabar Open Data Galura. Belum diverifikasi publikasi BPS KSA Kabupaten. |
| **A4** | Subang Jagung: Definisi CV Residu & Evaluasi Detrending | **CLOSED** | `reports/dataset_audit/a4_subang_detrending_sensitivity.csv` | `scripts/audit_a4_subang_detrending_sensitivity.py` | Dua angka beredar 11.42% vs 12.21%; klaim cuaca tak bisa jelaskan >12.2% | Dibakukan: $\text{CV}_{\text{ddof}=0}=11.42\%$, $\text{CV}_{\text{ddof}=1}=12.21\%$, $\text{CV}_{\text{OLS}}=13.19\%$. Outlier 2022 menyumbang 49.8% SSE. Tanpa 2022, CV residu = **5.49%** (linear) dan **2.65%** (piecewise 2020/2021). Klaim keliru dihapus; diganti "residu detrended, bukan batas atas cuaca". | DS05 Distanhor Jabar (2015–2022). |
| **A5** | Hubungan DS08 vs DS05: Dekomposisi Multiplikatif Log Produksi | **CLOSED** | `reports/eda/eda_b1_outcome_decomposition_variance_and_prod.png` | `scripts/generate_eda_figures.py` (Fig B1.4) | DS08 sebut yield stagnan & 98.4% luas; DS05 sebut yield melonjak 45.7 -> 89.5 | Dekomposisi log $\Delta \ln(\text{Prod}) = \Delta \ln(\text{Area}) + \Delta \ln(\text{Yield})$ membuktikan **98.4%–98.7%** lonjakan 2018 & 2020 didorong luas panen. Hubungan produksi/luas/yield terkonfirmasi sebagai **tautologi akuntansi**. | DS05 & DS08 Distanhor Jabar. Bobot baseline luas panen 2015–2017 tersedia. |
| **A6** | Modul Hortikultura IFWC & Koreksi Label CV Cabai | **CLOSED** | `notebook/06_west_java_horticulture_productivity.ipynb`, `docs/hypotheses.md` | `scripts/clean_notebook_06.py`, `scripts/generate_eda_figures.py` (Fig B4.1) | Ambang absolut 2.0°C; label DITERIMA/DITOLAK; CV cabai diklaim 28% dan 31%; periode 2016/2017/2025 | Ambang 2.0°C & label DITERIMA/DITOLAK dihapus. Pre-registrasi **P10 depresiasi titik embun** per sel/bulan. CV sejati: **Cabai Besar = 4.49%**, **Cabai Rawit = 5.71%**. Periode provinsi dibakukan: 2017–2024 ($N=8$). Sayuran kab/kota `od_18096` hanya 2013–2014 (zero overlap AgERA5). Terkunci Tier B. | `produktivitas_sbs_jabar.csv` & `produksi_sayuran_komoditas_jabar.csv`. |
| **A7** | DS04 Titik Grid & Penghapusan Ambang Absolut CDD | **CLOSED** | `notebook/04_indonesia_agroclimatic.ipynb` | `scripts/clean_notebook_04.py` | Ambang CDD >30 & >60 hari; titik Jabar 14 vs 12; sirkularitas belum diakui | Ambang hari kering absolut diganti **persentil empiris (P50, P75, P90)**. Dibakukan: **12 titik poligon resmi Jabar** (14 titik dalam bbox kasar, 2 di Jateng). DS04 diakui sebagai pembanding internal (sirkular ERA5). | CDS Copernicus ERA5 Terestrial Indonesia (DS04). |
| **A8** | Duplikasi Sel Grid AgERA5 & Unifikasi Koordinat Subang | **CLOSED** | `reports/dataset_audit/a8_spatial_grid_cells_audit.csv` | `scripts/audit_a8_spatial_grid_cells.py` | Duplikasi sel di beberapa kab/kota; koordinat Subang berbeda antar dokumen | 27 unit memetakan ke **25 sel AgERA5 unik**. Duplikasi HANYA pada Kab/Kota Bogor dan Kab/Kota Cirebon. Seluruh 18 kabupaten sentra Tier A memiliki sel 100% independen ($N_{\text{eff}}=18$). Subang dibakukan: Centroid $(-6.4830, 107.7322)$, Sel $(-6.50, 107.70)$, Elevasi DEM $49.0\text{ m}$. | GeoBoundaries ADM2; AgERA5 NetCDF/CSV; USGS SRTM DEM 90m. |
| **A9** | Konsistensi Dokumen & Pemecahan Kolom Matriks Linking | **CLOSED** | `reports/dataset_audit/cross_dataset_linking_matrix_revised.csv`, `dataset_audit_summary.csv` | `scripts/update_audit_matrices_a9.py` | Sentra kedelai 14 vs 17; 216 baris tanpa filter valid; kolom rating tunggal; cabai MODERATE; LINK_04 "7 titik" | Kriteria sentra kedelai ex ante: kabupaten aktif $N \ge 6$ tahun = **17 sentra** (panel seimbang $N=8$ = 14 sentra). Baris valid: 156 baris kedelai, 181 baris jagung. Kolom dipecah: `join_feasibility`, `effective_n_independent`, `expected_signal_power`. Cabai diubah ke `LOW/RULE_BASED_ONLY`. LINK_04 diubah ke 12 titik. DS07–DS09 ditambahkan. "Terbukti" diubah "konsisten dengan". | Repositori TaniAdapt & Distanhor. |
| **A10** | Hipotesis Terdaftar, Koreksi Uji, & Rekalkulasi MDE | **CLOSED** | `docs/hypotheses.md`, `reports/dataset_audit/a10_panel_mde_audit.csv` | `scripts/update_hypotheses_a10.py`, `scripts/compute_mde_final_panel.py` | Sitasi minim; Paper 15 Wonogiri keliru dipakai anthesis sterility; MDE 27 unit; cluster tahun tidak konsisten | Sitasi lengkap dengan label `[Transfer Literatur]`; Paper 15 diganti Prasad et al. (2006) / Jagadish et al. (2007). Koreksi primer: **Holm-Bonferroni**, sekunder: BH. Jendela tumpang tindih = sensitivitas. Placebo p > 0.10 diberi catatan daya rendah. Cluster per kabupaten ($G \approx 18$) + wild cluster bootstrap Webb. MDE 18 sentra final: **Padi = 2.35%**, **Jagung = 25.81%**, **Kedelai = 10.33%**. | Literatur Agronomi Resmi; Panel 18 Sentra Jabar. |
| **A11** | Kebersihan Repositori & Verifikasi File Git Terhapus | **CLOSED** | `scripts/audit_deleted_files.py` | `scripts/audit_deleted_files.py` | Dikhawatirkan script penting terhapus dalam 39 file commit sebelumnya | Terverifikasi tepat **45 file terhapus** terlacak di git history (`545bf8a` s.d. `5862b43`). Seluruh file dapat dipulihkan utuh dari git objects. Tidak ada script yang dibutuhkan untuk reproduksi yang hilang. | Git Commit Log & Tree Objects. |

---

## 2. Hasil Ringkas EDA Deskriptif Bagian B (B1 – B4)

Seluruh 11 figur diagnostik deskriptif telah diproduksi dan tersimpan di `reports/eda/` dengan caption standar (Sumber Data, Valid N, Periode, Flag Kualitas) dan mematuhi aturan ketat **tanpa p-value**:

1. **B1. Integritas Target Outcome**:
   - [`eda_b1_outcome_heatmap_logdiff.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b1_outcome_heatmap_logdiff.png): Menampilkan matriks perubahan log YoY padi, jagung, dan kedelai dengan baris pembanding provinsi. Terlihat jelas anomali lonjakan buatan padi 2019 dan kekakuan variasi 2022.
   - [`eda_b1_outcome_strip_dispersion_imputation.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b1_outcome_strip_dispersion_imputation.png): Box/strip plot mendeteksi kolapsnya standar deviasi kedelai (0.19 ku/ha) dan lonjakan 13 kabupaten dengan yield jagung persis 75.70 ku/ha pada 2022.
   - [`eda_b1_outcome_bps_ratios_and_funnel.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b1_outcome_bps_ratios_and_funnel.png): Panel rasio BPS membuktikan rata-rata berbobot DS03 cocok 100% dengan BPS 2015–2017, serta funnel plot variabilitas hasil vs luas panen baseline.
   - [`eda_b1_outcome_decomposition_variance_and_prod.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b1_outcome_decomposition_variance_and_prod.png): Dekomposisi varians yield menunjukkan 58.4% variasi diserap oleh FE Kabupaten dan 14.2% oleh FE Tahun, menyisakan 27.4% variasi residual untuk sinyal cuaca. Dekomposisi log membuktikan 98.4% lonjakan produksi Subang didorong perluasan luas panen.

2. **B2. Validasi Cuaca Spasial**:
   - [`eda_b2_weather_agera5_chirps_anomaly_scatter.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b2_weather_agera5_chirps_anomaly_scatter.png): Korelasi anomali bulanan deseasonalized AgERA5 vs CHIRPS berkisar $r = 0.50\text{--}0.80$ (median 0.73).
   - [`eda_b2_weather_bias_vs_elevation_and_season.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b2_weather_bias_vs_elevation_and_season.png): Plot bias signed membuktikan bias overestimasi orografis positif tajam pada dataran tinggi Bandung Raya ($+33\%\text{ s.d. }+61\%$, korelasi elevasi $r = +0.631$) dan defisit tajam di Bogor ($-34\%\text{ s.d. }-39\%$).
   - [`eda_b2_weather_spatial_correlation_pca.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b2_weather_spatial_correlation_pca.png): Matriks korelasi spasial antar-unit rata-rata $r > 0.75$; PC1 dan PC2 menjelaskan 76.8% variasi presipitasi, membuktikan $N$ independen efektif iklim hanya sekitar 3 hingga 4 klaster.
   - [`eda_b2_weather_climatology_and_macro_oni_dmi.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b2_weather_climatology_and_macro_oni_dmi.png): Klimatologi bulanan P10-P50-P90 mencerminkan siklus muson alami, sinkron dengan anomali makro ENSO NOAA ONI (Super El Niño 2015 dan La Niña 2016).

3. **B3. Pemasangan Cuaca-Outcome (Hipotesis Terdaftar)**:
   - [`eda_b3_weather_outcome_added_variable_plot.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b3_weather_outcome_added_variable_plot.png): Added-variable plot H_CORN_01 (presipitasi vegetatif Feb–Apr) dengan FE Kabupaten dan FE Tahun di-partial out. Effect size $\beta = +0.0182$ log points / SD, $95\%\text{ CI } [-0.038, +0.074]$. Karena $|\beta| < \text{MDE} = \pm 0.2296$, data konsisten dengan kesimpulan *Evidence Insufficient*.
   - [`eda_b3_weather_outcome_forest_loo_and_lead.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b3_weather_outcome_forest_loo_and_lead.png): Forest plot Leave-One-Year-Out (LOO) menunjukkan estimasi stabil terhadap pembuangan tahun Super El Niño 2015. Lead weather $t+1$ placebo mendekati nol ($\beta = +0.0041$), tidak menunjukkan tren semu. Seluruh visualisasi menyajikan MDE di samping effect size.

4. **B4. Hortikultura Cabai (Tier B)**:
   - [`eda_b4_horticulture_ifwc_dew_depression_p10.png`](file:///c:/CODING/research_taniAdapt/reports/eda/eda_b4_horticulture_ifwc_dew_depression_p10.png): Distribusi persentil depresiasi titik embun ($T_{\min} - T_d$) membuktikan ambang relatif $P_{10}$ mendeteksi 10.0% hari kondusif kelembapan malam secara stabil, mengoreksi ambang absolut 2.0°C. Runtun produktivitas cabai provinsi 2017–2024 menyajikan CV sejati (Cabai Besar 4.49%, Cabai Rawit 5.71%) dan menegaskan isolasi Tier B (tanpa regresi hasil dan tanpa ML penyakit).

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
