# TaniAdapt — West Java Climate–Agronomic Resilience Architecture

> **Evidence-Based Agricultural Decision Support System for Indonesian Smallholders**  
> *Translating Microclimate, Phenology, and Agrometeorological Dynamics into Calibrated Agronomic Actions.*

> **Phase 4 canonical record:** see [`docs/phase4_final_dataset_evidence_registry.md`](docs/phase4_final_dataset_evidence_registry.md) for the authoritative dataset status and [`docs/reproducibility.md`](docs/reproducibility.md) for the refresh workflow.

[![Phase](https://img.shields.io/badge/Research%20Phase-Phase%204%20Closure%20%26%20Phase%206%20EDA-success)](file:///c:/CODING/research_taniAdapt/reports/audit_closure_report.md)
[![Audit Status](https://img.shields.io/badge/Audit%20Blockers-A1--A11%20CLOSED-blue)](file:///c:/CODING/research_taniAdapt/reports/audit_closure_report.md)
[![Notebooks](https://img.shields.io/badge/Executable%20Notebooks-10%20Verified%20(0%20Errors)-brightgreen)](file:///c:/CODING/research_taniAdapt/notebook/)

---

## 🧭 Master Navigation & Notebook Index

Seluruh alur riset, audit integritas, dan visualisasi *Exploratory Data Analysis* (EDA) telah dikonsolidasikan langsung ke dalam **10 Jupyter Notebooks mandiri**. Anda **cukup membuka notebook yang relevan** tanpa perlu menelusuri puluhan berkas mentah.

### 1. Single-Dataset EDA (Analisis Mandiri per Dataset)
Setiap notebook `01` s/d `09` mengeksekusi audit kualitas internal dan visualisasi statistik murni yang hanya bersumber dari dataset itu sendiri:

| Notebook | Komoditas / Sumber Data | Cakupan Wilayah & Waktu | Fokus Audit & Visualisasi EDA Mandiri |
| :--- | :--- | :--- | :--- |
| [**`01_AgERA5.ipynb`**](file:///c:/CODING/research_taniAdapt/notebook/01_AgERA5.ipynb) | Cuaca Harian AgERA5 (ECMWF CDS) | 27 Kab/Kota (2015–2024, 10 thn) | **Dependensi Spasial Presipitasi & $N_{\text{eff}}$**: Matriks korelasi 27 unit ($r > 0.75$) & PCA Scree Plot membuktikan derajat bebas iklim independen efektif Jabar hanya ~3–4 klaster. |
| [**`02_bangladesh_rice_panel.ipynb`**](file:///c:/CODING/research_taniAdapt/notebook/02_bangladesh_rice_panel.ipynb) | Benchmark Padi BRRI (Mendeley Data) | 64 Distrik (2015–2024, 3 musim) | **Dekomposisi Varians Two-Way Fixed Effects**: Disparitas yield per musim (Boro > Aman > Aus) & bukti benchmark bahwa residual sinyal cuaca menyumbang ~25% variasi. |
| [**`03_west_java_rice_productivity.ipynb`**](file:///c:/CODING/research_taniAdapt/notebook/03_west_java_rice_productivity.ipynb) | Padi Sawah/Total (Distanhor & BPS) | 27 Kab/Kota (2015–2020) | **Rekonsiliasi B1 & Isolasi Artefak**: Rata-rata berbobot luas panen cocok 100.0% dengan BPS resmi pre-KSA (2015–2017); isolasi lonjakan semu 2019 (+21.8%) akibat konversi GKP Galura. |
| [**`04_indonesia_agroclimatic.ipynb`**](file:///c:/CODING/research_taniAdapt/notebook/04_indonesia_agroclimatic.ipynb) | Indikator Ekstrem Nasional (ERA5) | 12 Titik Poligon Jabar (2016–2025) | **Distribusi CDD Persentil Empiris**: Hapus ambang kaku 30/60 hari; gunakan persentil lokal (P50, P75, P90), neraca air ($P - ET_0$), dan evaluasi sirkularitas internal ERA5. |
| [**`05_subang_maize_productivity.ipynb`**](file:///c:/CODING/research_taniAdapt/notebook/05_subang_maize_productivity.ipynb) | Jagung Jabar & Subang (Distanhor) | 27 Kab/Kota (2015–2022) | **Deteksi Imputasi 2022 & Detrending Subang**: Deteksi 13 unit identik 75.70 ku/ha (imputasi); tren linear Subang (+4.93 ku/ha/thn) dengan CV residu menyusut ke 5.49% (ex-2022). |
| [**`06_west_java_horticulture_productivity.ipynb`**](file:///c:/CODING/research_taniAdapt/notebook/06_west_java_horticulture_productivity.ipynb) | SBS Cabai Besar & Rawit (Distanhor) | Provinsi (2017–2024) | **Koreksi CV Sejati & Isolasi Tier B**: CV empiris Cabai Besar 4.49% & Cabai Rawit 5.71%; bukti *zero overlap* data kabupaten `od_18096` (2013–2014) membatasi hortikultura ke aturan IFWC non-regresi. |
| [**`07_soybean_and_spatial_geoboundaries.ipynb`**](file:///c:/CODING/research_taniAdapt/notebook/07_soybean_and_spatial_geoboundaries.ipynb) | Kedelai & Centroid geoBoundaries | 27 Kab/Kota (2015–2022) | **Deteksi Imputasi Kedelai 2022 & Filter 17 Sentra**: SD spasial kolaps ke 0.19 ku/ha pada 2022 (imputasi provinsi); filter ex-ante kabupaten aktif minimal 6 tahun menghasilkan panel 17 sentra. |
| [**`08_production_and_harvest_area.ipynb`**](file:///c:/CODING/research_taniAdapt/notebook/08_production_and_harvest_area.ipynb) | Produksi & Luas Panen (Distanhor) | 27 Kab/Kota (2015–2021) | **Dekomposisi Log Produksi & Funnel Plot**: $\Delta \ln(\text{Prod}) = \Delta \ln(\text{Area}) + \Delta \ln(\text{Yield})$ membuktikan 98.4% lonjakan Subang disumbang luas panen; Funnel plot skala luas vs CV yield. |
| [**`09_climate_covariates_and_chirps.ipynb`**](file:///c:/CODING/research_taniAdapt/notebook/09_climate_covariates_and_chirps.ipynb) | Indeks Iklim Makro (NOAA CPC/PSL) | Pasifik & Samudra Hindia (2015–2024)| **Dinamika Kovariat Makro ENSO & IOD**: Runtun waktu NOAA ONI (El Niño 2015/16, La Niña 2020–22, Super El Niño 2023/24) dan NOAA PSL DMI (fase IOD positif ekstrem 2019). |

---

### 2. Cross-Dataset Merged EDA (Sintesis Gabungan Antar-Dataset)
Khusus untuk analisis yang **memerlukan perpaduan 2 atau lebih dataset**, seluruh evaluasinya disatukan dalam 1 notebook sintesis:

| Notebook | Dataset yang Digabungkan | Analisis & Visualisasi Multimodal |
| :--- | :--- | :--- |
| [**`10_phase6_exploratory_data_analysis.ipynb`**](file:///c:/CODING/research_taniAdapt/notebook/10_phase6_exploratory_data_analysis.ipynb) | **DS01 + DS03 + DS05 + DS06 + DS07 + DS09 + CHIRPS + DEM** | **Sintesis Ekonometrika & Weather Coupling**:<br>1. **AgERA5 + CHIRPS v2 + DEM**: Regresi signed bias spasial vs elevasi topografi ($r = +0.631$, overestimasi Bandung Raya $+33\%\text{ s.d. }+61\%$) & korelasi anomali bulanan deseasonalized ($r = 0.50\text{--}0.80$).<br>2. **AgERA5 + Jagung Subang/Jabar**: Added-Variable Plot Hipotesis `H_CORN_01` (presipitasi vegetatif Feb–Apr setelah partial out FE Kabupaten & Tahun) disandingkan dengan MDE ($\pm 0.2296$).<br>3. **AgERA5 + Padi Sawah**: Panel coupling presipitasi MH/MK terhadap dinamika yield 18 sentra & evaluasi MDE (2.35%).<br>4. **AgERA5 + Hortikultura**: Mikroklimat depresi titik embun harian ($T_{\min} - T_d$) per sel/bulan untuk pre-registrasi ambang $P_{10}$ IFWC.<br>5. **AgERA5 + geoBoundaries**: Matriks dependensi spasial (27 adm2 ke 25 sel grid AgERA5 unik; $N_{\text{eff}} = 18$).<br>6. **AgERA5 + Makro ONI**: Telekoneksi anomali presipitasi tahunan terhadap siklus ENSO. |

---

## 🏛️ Matriks Resolusi Audit (Item Blocker A1–A11 & B1–B4)

Semua inkonsistensi yang ditemukan oleh audit independen telah ditutup secara permanen:

| ID | Topik Audit | Temuan Empiris | Resolusi Ilmiah & Status | Dokumen / Notebook Pembuktian |
| :--- | :--- | :--- | :--- | :--- |
| **A1** | Rekonsiliasi Padi 2015–2017 | Rata-rata berbobot luas panen DS03 cocok **100.0% (selisih 0.00%)** dengan publikasi BPS resmi (61.22, 60.49, 58.87 ku/ha). | Terpecahkan. Lonjakan 2019 (+21.8%) diisolasi sebagai artefak konversi GKP Galura. Periode 2018–2020 dieksklusikan dari panel utama. | [`b1_rice_reconciliation_v2.csv`](file:///c:/CODING/research_taniAdapt/reports/dataset_audit/b1_rice_reconciliation_v2.csv)<br>[`03_west_java_rice_productivity.ipynb`](file:///c:/CODING/research_taniAdapt/notebook/03_west_java_rice_productivity.ipynb) |
| **A2** | AgERA5 vs CHIRPS 27 Unit | Korelasi deseasonalized bulanan $r = 0.50\text{--}0.80$ (median 0.73). Signed bias berkorelasi positif dengan elevasi ($r = +0.631$). | Terpecahkan. Angka Tasikmalaya dikoreksi ke rata-rata 3 tahun benchmark (4.465,7 mm). Overestimasi orografis Bandung Raya (+33% s.d. +61%) dicatat sebagai limitasi model. | [`b3_rainfall_bias_chirps_audit_v2.csv`](file:///c:/CODING/research_taniAdapt/reports/dataset_audit/b3_rainfall_bias_chirps_audit_v2.csv)<br>[`10_phase6_exploratory_data_analysis.ipynb`](file:///c:/CODING/research_taniAdapt/notebook/10_phase6_exploratory_data_analysis.ipynb) |
| **A3** | Anomali Jagung & Kedelai 2022 | 13 unit jagung identik 75.70 ku/ha. Standar deviasi kedelai kolaps ke 0.19 ku/ha. | Terpecahkan. Tahun 2022 ditandai `SUSPECT` dan dieksklusikan dari panel utama model regresi. | [`05_subang_maize_productivity.ipynb`](file:///c:/CODING/research_taniAdapt/notebook/05_subang_maize_productivity.ipynb)<br>[`07_soybean_and_spatial_geoboundaries.ipynb`](file:///c:/CODING/research_taniAdapt/notebook/07_soybean_and_spatial_geoboundaries.ipynb) |
| **A4** | CV Produktivitas Subang | CV sampel mentah = 12.21%. Titik 2022 menyumbang 49.8% sum of squared errors tren linear. | Terpecahkan. Tanpa titik 2022, CV residu detrended menyusut ke **5.49%** (linear) dan **2.65%** (piecewise). | [`05_subang_maize_productivity.ipynb`](file:///c:/CODING/research_taniAdapt/notebook/05_subang_maize_productivity.ipynb) |
| **A5** | Dekomposisi Log Produksi Subang | $\Delta \ln(\text{Prod}) = \Delta \ln(\text{Area}) + \Delta \ln(\text{Yield})$. | Terpecahkan. 98.4%–98.7% lonjakan produksi jagung Subang 2018 & 2020 disumbang oleh ekspansi luas panen, bukan produktivitas. | [`08_production_and_harvest_area.ipynb`](file:///c:/CODING/research_taniAdapt/notebook/08_production_and_harvest_area.ipynb) |
| **A6** | Hipotesis Embun & CV Cabai | Ambang kaku 2.0°C diganti persentil lokal $P_{10}$ per sel/bulan. CV empiris Cabai Besar 4.49% & Rawit 5.71%. | Terpecahkan. Data kabupaten `od_18096` hanya ada di 2013–2014 (*zero overlap*). Hortikultura diisolasi ke modul aturan IFWC non-regresi. | [`06_west_java_horticulture_productivity.ipynb`](file:///c:/CODING/research_taniAdapt/notebook/06_west_java_horticulture_productivity.ipynb)<br>[`10_phase6_exploratory_data_analysis.ipynb`](file:///c:/CODING/research_taniAdapt/notebook/10_phase6_exploratory_data_analysis.ipynb) |
| **A7** | Titik Grid DS04 & Sirkularitas | Tepat 12 titik grid berada di dalam poligon batas resmi Jabar (14 titik pada bbox kasar). Ambang absolut CDD >30/>60 hari dihapus. | Terpecahkan. Sirkularitas internal ERA5 diakui sebagai *internal consistency check*, bukan validasi independen. | [`04_indonesia_agroclimatic.ipynb`](file:///c:/CODING/research_taniAdapt/notebook/04_indonesia_agroclimatic.ipynb) |
| **A8** | Sel Grid AgERA5 27 Wilayah | 27 wilayah administratif memetakan ke 25 sel grid AgERA5 0.1° unik. Seluruh 18 kabupaten sentra pertanian Tier A memiliki sel grid 100% independen. | Terpecahkan. Derajat bebas spasial efektif 18 sentra $N_{\text{eff}} = 18$. Titik koordinat Subang disinkronkan ke lintang -6.56°S, bujur 107.76°E. | [`a8_spatial_grid_cells_audit.csv`](file:///c:/CODING/research_taniAdapt/reports/dataset_audit/a8_spatial_grid_cells_audit.csv)<br>[`10_phase6_exploratory_data_analysis.ipynb`](file:///c:/CODING/research_taniAdapt/notebook/10_phase6_exploratory_data_analysis.ipynb) |
| **A9** | Filter Sentra Kedelai Ex-Ante | Kriteria ex-ante: kabupaten aktif minimal 6 tahun dengan hasil panen $> 0$. | Terpecahkan. Panel seimbang ketat $N=8$ menghasilkan 14 sentra (termasuk kota); panel kabupaten pertanian $N \ge 6$ menghasilkan tepat **17 sentra kabupaten**. | [`07_soybean_and_spatial_geoboundaries.ipynb`](file:///c:/CODING/research_taniAdapt/notebook/07_soybean_and_spatial_geoboundaries.ipynb) |
| **A10** | Multiple Testing & Cluster Power | Koreksi multiple testing menggunakan Holm-Bonferroni (primer) dan Benjamini-Hochberg (sekunder). Kluster $G \approx 18$ kabupaten. | Terpecahkan. MDE final panel dengan wild cluster bootstrap Webb: Padi 2.35%, Jagung 25.81%, Kedelai 10.33%. | [`a10_panel_mde_audit.csv`](file:///c:/CODING/research_taniAdapt/reports/dataset_audit/a10_panel_mde_audit.csv)<br>[`10_phase6_exploratory_data_analysis.ipynb`](file:///c:/CODING/research_taniAdapt/notebook/10_phase6_exploratory_data_analysis.ipynb) |
| **A11** | Audit File Terhapus | 45 file yang sempat terhapus diverifikasi dalam riwayat git (semuanya berkas duplikat/sintetik; nol skrip reproduksi hilang). | Terpecahkan. Seluruh repositori dapat direproduksi penuh secara deterministik dari awal. | [`audit_closure_report.md`](file:///c:/CODING/research_taniAdapt/reports/audit_closure_report.md) |

---

## 📁 Struktur Repositori Bersih (Zero-Clutter Layout)

Repositori ini telah dirapikan agar efisien, tidak membingungkan, dan memenuhi standar riset akademik tingkat lanjut:

```text
research_taniAdapt/
├── README.md                                 # Peta Navigasi & Master Index (Dokumen ini)
├── notebook/                                 # 10 Notebook Eksekusi Utama (Live Inline Visuals)
│   ├── 01_AgERA5.ipynb                       # [DS01] AgERA5 Spasial & Klimatologi (Single Dataset)
│   ├── 02_bangladesh_rice_panel.ipynb        # [DS02] Benchmark Panel Ekonometrika (Single Dataset)
│   ├── 03_west_java_rice_productivity.ipynb  # [DS03] Padi Sawah Rekonsiliasi & Heatmap (Single Dataset)
│   ├── 04_indonesia_agroclimatic.ipynb       # [DS04] Ekstrem Grid Persentil Empiris (Single Dataset)
│   ├── 05_subang_maize_productivity.ipynb    # [DS05] Jagung Subang & Imputasi 2022 (Single Dataset)
│   ├── 06_west_java_horticulture_productivity.ipynb # [DS06] Cabai CV Sejati & Tier B (Single Dataset)
│   ├── 07_soybean_and_spatial_geoboundaries.ipynb   # [DS07] Kedelai 17 Sentra Ex-Ante (Single Dataset)
│   ├── 08_production_and_harvest_area.ipynb  # [DS08] Dekomposisi Log Produksi & Funnel (Single Dataset)
│   ├── 09_climate_covariates_and_chirps.ipynb# [DS09] Kovariat Makro ENSO & IOD (Single Dataset)
│   └── 10_phase6_exploratory_data_analysis.ipynb # [SINTESIS] Cross-Dataset Coupling & Multimodal Regresi
├── reports/                                  # Laporan Resmi & Berkas Referensi Final
│   ├── audit_closure_report.md               # Laporan Penutupan Audit Komprehensif (A1–A11 & B1–B4)
│   ├── source_log.md                         # Log Sumber Resmi BPS, CDS, BMKG (Verified URLs & Tanggal)
│   ├── citation_audit_matrix.csv             # Matriks Sitasi Agronomi (Jagadish, Prasad, dll.)
│   ├── dataset_audit/                        # Berkas Referensi CSV Terverifikasi
│   │   ├── b1_rice_reconciliation_v2.csv     # Hasil Rekonsiliasi Padi 2015-2020 vs BPS
│   │   ├── b3_rainfall_bias_chirps_audit_v2.csv # Audit Signed Bias AgERA5 vs CHIRPS 27 Unit
│   │   ├── a8_spatial_grid_cells_audit.csv   # Pemetaan 27 ADM2 ke 25 Sel Grid AgERA5
│   │   ├── a10_panel_mde_audit.csv           # Matriks Perhitungan Minimum Detectable Effect (MDE)
│   │   ├── jabar_27_kabkota_centroids.csv    # Koordinat Centroid Resmi ADM2 Jawa Barat
│   │   ├── cross_dataset_linking_matrix_revised.csv # Matriks Kelayakan Integrasi Data
│   │   ├── dataset_audit_summary.csv         # Ringkasan Audit Kualitas per Dataset
│   │   └── archive/                          # [ARSIP] Berkas CSV draf & kerja intermediat
│   ├── figures/                              # Gambar PNG Berkualitas Tinggi Hasil Eksekusi Notebook
│   ├── logs/                                 # [LOGS] Log Inkonsistensi & Riwayat Eksplorasi
│   └── archive/                              # [ARSIP] Draf laporan historis
├── scripts/                                  # Skrip Inti Pipeline
│   ├── build_modular_eda_notebooks.py        # Master Runner: Bangun & Eksekusi Semua 10 Notebook
│   ├── acquire_agera5_all_27_kabkota.py      # Pengunduh Data Cuaca AgERA5 27 Unit
│   ├── fetch_chirps_remaining.py             # Pengunduh Satelit CHIRPS v2
│   ├── fetch_padi_variants.py                # Pengunduh Varian Padi Galura/Distanhor
│   ├── fetch_area_production_datasets.py     # Pengunduh Luas Panen & Produksi
│   ├── run_quality_audit.py                  # Audit Kualitas Terotomatisasi
│   └── archive/                              # [ARSIP] 43 skrip temporer, patch, & scratch
└── data/                                     # Raw Data Storage (Diabaikan oleh Git)
```

---

## ⚡ Cara Menjalankan & Mereproduksi (1-Click Pipeline)

Untuk mereproduksi seluruh hasil audit dan merender ulang semua visualisasi pada 10 notebook secara otomatis dari awal hingga akhir:

```powershell
python scripts/build_modular_eda_notebooks.py
```

*Skrip ini akan mengonfigurasi sel EDA single-dataset pada Notebook `01` s/d `09`, menyelaraskan Notebook `10` untuk cross-dataset synthesis, lalu mengeksekusi ke-10 notebook menggunakan `NotebookClient` hingga seluruh grafik PNG ter-render inline.*
