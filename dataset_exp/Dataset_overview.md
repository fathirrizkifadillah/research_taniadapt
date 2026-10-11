# 📚 Master Katalog & Kamus Data Terpadu — Proyek TaniAdapt

Repositori ini memuat **9 Dataset Utama (DS01 s.d. DS09)** yang terverifikasi secara empiris untuk membangun Decision Engine dan Advisory Pertanian Presisi di Jawa Barat.

---

## 1. Matriks Ringkasan Seluruh 9 Dataset

| ID | Nama Dataset | Penerbit / Portal Sumber Resmi | Cakupan Spasial | Cakupan Waktu & N_eff | Total Kolom | Status Disposisi Audit |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: |
| **DS01** | **AgERA5 Agrometeorological Indicators** | Copernicus CDS (ECMWF / EU) | **27 Kab/Kota Se-Jawa Barat** | 2015–2024 (Harian, $98.631$ baris) | **27 kolom** | **PASS** (Backbone Cuaca) |
| **DS02** | **Bangladesh Rice Climate-Yield Panel** | Mendeley Data / BRRI | 64 Distrik Bangladesh | 2015–2024 (3 Musim, $1.728$ baris) | **36 kolom** | **BENCHMARK** (Replikasi Panel) |
| **DS03** | **Produktivitas Padi Jawa Barat** | Distanhor / Open Data Jabar | **27 Kab/Kota Se-Jawa Barat** | 2015–2020 (Tahunan, 162 baris) | **8 kolom** | **PASS** (Artefak 2019 Terisolasi) |
| **DS04** | **Indonesia Nationwide Agroclimatic** | Elsevier / Mendeley Data | 612 Titik Grid (14 di Jabar) | 2016–2025 (Harian) | **23 kolom** | **PASS** (Validasi Silang Grid) |
| **DS05** | **Produktivitas Jagung Jawa Barat** | Distanhor / Open Data Jabar | **27 Kab/Kota Se-Jawa Barat** | 2015–2022 (Tahunan, 216 baris) | **8 kolom** | **PASS** (Target Jagung Regional) |
| **DS06** | **Hortikultura Cabai & Tomat** | Distanhor / Open Data Jabar | Provinsi (SBS) & Kab/Kota (Prod) | 2016–2024 (Tahunan) | **7 & 9 kolom** | **PASS** (Target Panen Makro) |
| **DS07** | **Kedelai & Geospasial ADM2 Centroids**| Distanhor & geoBoundaries | **27 Kab/Kota Se-Jawa Barat** | 2015–2022 (Tahunan, 216 baris) | **8 kolom** | **PASS** (Target Kedelai + Batas GIS) |
| **DS08** | **Volume Produksi & Luas Panen** | Distanhor / Open Data Jabar | **27 Kab/Kota Se-Jawa Barat** | 2015–2022 (Tahunan) | **8 kolom** | **PASS** (Identitas Matematika Valid) |
| **DS09** | **Kovariat Iklim Makro (ONI, DMI, CHIRPS)**| NOAA CPC, PSL & UCSB ERDDAP | Pasifik, Samudera Hindia, Jabar | 2015–2024 (Bulanan & Harian) | **4 & 4 kolom** | **PASS** (Validasi Orografis Nyata) |

---

## 2. Navigasi Dokumentasi Spesifik Dataset
* [01_DS01_agera5_weather.md](file:///c:/CODING/research_taniAdapt/dataset_exp/01_DS01_agera5_weather.md) — 27 Parameter Agrometeorologi AgERA5
* [02_DS02_bangladesh_rice_panel.md](file:///c:/CODING/research_taniAdapt/dataset_exp/02_DS02_bangladesh_rice_panel.md) — 36 Variabel Replikasi Padi Bangladesh
* [03_DS03_west_java_rice.md](file:///c:/CODING/research_taniAdapt/dataset_exp/03_DS03_west_java_rice.md) — Produktivitas Padi Sawah, Ladang & Total
* [04_DS04_indonesia_agroclimatic.md](file:///c:/CODING/research_taniAdapt/dataset_exp/04_DS04_indonesia_agroclimatic.md) — 23 Indikator Ekstrem Agroklimat Parquet
* [05_DS05_subang_maize.md](file:///c:/CODING/research_taniAdapt/dataset_exp/05_DS05_subang_maize.md) — Produktivitas Jagung 27 Kab/Kota Jawa Barat
* [06_DS06_west_java_horticulture_chili_tomato.md](file:///c:/CODING/research_taniAdapt/dataset_exp/06_DS06_west_java_horticulture_chili_tomato.md) — Hortikultura Cabai Rawit, Cabai Besar & Tomat
* [07_soybean_and_spatial_geoboundaries.md](file:///c:/CODING/research_taniAdapt/dataset_exp/07_soybean_and_spatial_geoboundaries.md) — Kedelai Jawa Barat & Geospasial Poligon
* [08_production_and_harvest_area.md](file:///c:/CODING/research_taniAdapt/dataset_exp/08_production_and_harvest_area.md) — Uji Identitas Matematika Yield = Produksi / Luas Panen
* [09_climate_covariates_and_chirps.md](file:///c:/CODING/research_taniAdapt/dataset_exp/09_climate_covariates_and_chirps.md) — NOAA ONI, DMI, dan Satelit CHIRPS v2
