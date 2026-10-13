# TaniAdapt Research Dossier — Phase 6: Exploratory Data Analysis (EDA) Master Architecture

**Status**: COMPLETED  
**Ruang Lingkup**: Arsitektur 10 Jupyter Notebooks Mandiri & Katalog 68 Figur Kanonik  
**Prinsip Desain**: Single-Dataset Analysis (Notebook 01–09) dan Multi-Dataset Synthesis (Notebook 10)

---

## 1. Struktur Arsitektur 10 Jupyter Notebooks
Sesuai arahan arsitektur proyek, eksplorasi data dibagi secara modular:

```text
notebook/
├── 01_AgERA5.ipynb                          <- EDA Cuaca AgERA5 (1991–2024), ET0 FAO-56, & Baseline 30 Tahun
├── 02_CHIRPS.ipynb                          <- EDA Satelit Hujan CHIRPS (2015–2024) & Validasi Bias Hujan
├── 03_west_java_rice.ipynb                  <- EDA Panel Padi BPS 27 Kabupaten (2015–2017)
├── 04_rice_harvest_production_area.ipynb    <- EDA Padi KSA BPS (2018–2024) & Dinamika Musim Tanam
├── 05_subang_maize.ipynb                    <- EDA Panel Jagung 18 Sentra (2015–2021) & Eliminasi Imputasi 2022
├── 06_west_java_horticulture.ipynb          <- EDA Hortikultura Cabai & Tomat SBS Jawa Barat (2017–2024)
├── 07_soybean_and_spatial_geoboundaries.ipynb <- EDA Geospasial ADM2, Centroid, Sel Grid Cuaca, & DEM SRTM
├── 08_production_and_harvest_area.ipynb     <- EDA Struktur Luas Baku Lahan & Pangsa Sentra Pangan
├── 09_climate_covariates_and_chirps.ipynb   <- EDA Respons Iklim Makro El Niño (ONI) & IOD (DMI)
└── 10_phase6_exploratory_data_analysis.ipynb <- NOTEBOOK INDUK SINTESIS: Fusi Multi-Dataset, Phase 7–12
```

---

## 2. Rangkuman Temuan Inti Lintas Notebook EDA

### A. EDA 01 & 02: Cuaca dan Presipitasi Reanalysis vs Satelit
* AgERA5 merekam suhu rata-rata tahunan Jawa Barat berkisar $21.2^\circ	ext{C}$ di dataran tinggi hingga $28.4^\circ	ext{C}$ di pesisir utara.
* Evapotranspirasi acuan ($ET_0$) Penman-Monteith memiliki rata-rata harian $3.88	ext{ mm/hari}$ (berkisar antara $2.8	ext{ mm/hari}$ saat puncak musim hujan hingga $5.2	ext{ mm/hari}$ saat kemarau terik berangin).
* Validasi CHIRPS vs AgERA5 pada 936 unit-bulan menunjukkan korelasi tinggi ($r = 0.727$), namun AgERA5 cenderung sedikit basah (*wet bias*) di lereng pegunungan orografis.

### B. EDA 07: Geospasial, Centroid, dan Resolusi Elevasi SRTM
* Sebanyak 27 Kabupaten/Kota Jawa Barat berhasil dipetakan ke 22 sel cuaca unik $0.1^\circ$. Jarak pergeseran rata-rata (*haversine offset*) adalah **5.80 km (formula Haversine)**.
* Profil elevasi menunjukkan gradien curam: dari 7 mdpl (Indramayu) hingga 1.341 mdpl (Lembang/Bandung Barat), memvalidasi perlunya koreksi tekanan udara barometrik lokal pada formula Penman-Monteith.

### C. EDA 10: Sintesis Multi-Dataset di Notebook 10
Notebook 10 menjadi pusat integrasi seluruh hasil penelitian, memuat:
* Pengujian 11 hipotesis fenologi (Phase 7, Cell 44–49).
* Feature store 65.754 baris dan pengujian multikolinearitas VIF (Phase 8, Cell 50–55).
* Benchmarking 6 model machine learning LOYO cross-validation (Phase 9, Cell 56–61).
* Kalibrasi model risiko fisis FAO-56 dan mikroklimat fajar $P_{10}$ (Phase 10, Cell 62–67).
* Logika keputusan operasional 5 tindakan agronomi jam 06.00–18.00 WIB (Phase 11, Cell 68–73).
* Validasi hindcast non-yield 3 peristiwa BMKG dan stress-testing (Phase 12, Cell 74–79).
