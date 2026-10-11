# 📊 TaniAdapt Dataset Landscape & Data Dictionaries (`dataset_exp/`)

> **Tentang Direktori Ini:**  
> Seluruh file data mentah berukuran besar (*raw files* seperti Parquet dan CSV ribuan baris di direktori `data/raw/`) dikecualikan dari Git melalui `.gitignore` demi efisiensi repositori.  
> Direktori `dataset_exp/` ini berfungsi sebagai **dokumentasi data kanonikal** yang dapat dibaca langsung di GitHub maupun oleh asisten AI (seperti Claude), mencakup: asal sumber data, struktur tabel, variabel aktual, rentang waktu, temuan empiris audit, hingga batasan agronomisnya.

---

## 🗺️ Master Dataset Matrix (TaniAdapt Portfolio)

| ID | Nama Dataset | Institusi Sumber & Endpoint | Cakupan Spasial | Frekuensi & Periode | Format & Dimensi | Status Kualitas & Audit | Peran di TaniAdapt |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DS01** | **AgERA5 Agrometeorological Indicators** | Copernicus CDS (ECMWF)<br>`DOI: 10.24381/f9c1f09d` | 27 Kabupaten/Kota Se-Jawa Barat (Full Coverage Centroid) | Harian<br>(2015–2024, 10 thn) | CSV (27 file, ~27 MB)<br>98.631 baris total, 24 var | **PASS & TERVALIDASI INDEPENDEN**<br>(Curah hujan terkonfirmasi satelit CHIRPS v2) | **Backbone Cuaca Mikro**: Suhu, presipitasi (mm/hari), VPD, radiasi, dan depresiasi embun. |
| **DS02** | **Bangladesh Rice Panel** | Mendeley Data / Audited Replication Panel<br>`DOI: 10.17632/h94z4ftts2.1` | 64 Distrik di Bangladesh | Musiman/Tahunan<br>(2015–2024, 10 thn) | CSV (~2.1 MB)<br>Aus, Aman, Boro | **BENCHMARK METODOLOGIS**<br>(Bukan data lokal Jabar) | **Referensi Panel Regression**: Replikasi model *Two-Way Fixed Effects* & dekomposisi musiman. |
| **DS03** | **Produktivitas Padi Jawa Barat** | Distanhor Jabar / Galura API<br>`od_18103_produktivitas_padi...` | 27 Kabupaten/Kota Se-Jawa Barat | Tahunan Agregat<br>(2015–2020, 6 thn) | CSV & JSON (~12 KB)<br>162 baris (Padi Total, Sawah, Ladang) | **ARTEFAK TERBUKTI (BLOCKER B1)**<br>Lonjakan 2019 (+23.7%) adalah artefak GKP vs GKG | **Target Outcome Padi (Tier A)**: Wajib dikoreksi/diganti data BPS KSA sebelum modeling. |
| **DS04** | **Indonesia Nationwide Agroclimate** | Elsevier / Mendeley Data<br>`DOI: 10.17632/3pfbdbzfff.1` | 612 Titik Daratan RI<br>(12–14 titik di Jawa Barat) | Harian<br>(2016–2025, 10 thn) | Parquet (~60 MB)<br>Grid 0.5° & 12 derived indicators | **VALIDASI SILANG (CROSS-VAL ONLY)**<br>Konsistensi internal ERA5 | **Pembanding Eksternal**: Bukan sumber live engine; indikator operasional dihitung via pipeline mandiri. |
| **DS05** | **Produktivitas Jagung Jabar & Subang** | Distanhor Jabar / Galura API<br>`od_18104_produktivitas_jagung...` | 27 Kabupaten/Kota Se-Jawa Barat (Fokus: Subang) | Tahunan Agregat<br>(2015–2022, 8 thn) | CSV & JSON (~14 KB)<br>216 baris lengkap | **OUTLIER LOKAL SUBANG (B2)**<br>Subang naik +4.93 ku/ha/thn; sentra lain datar | **Target Outcome Jagung (Tier A)**: Wajib detrending kabupaten; hipotesis KSA jagung belum terkonfirmasi. |
| **DS06** | **Hortikultura SBS Cabai & Tomat** | Distanhor Jabar / Galura API<br>`od_18100_produktivitas_sayuran...` | Agregat Provinsi Jawa Barat ($N=9$ thn) | Tahunan Agregat<br>(2016–2024, 9 thn) | CSV & JSON (~76 KB)<br>SBS (ku/ha) & Produksi (ton) | **YIELD ONLY (TANPA LABEL OPT)**<br>❌ Ambang tanpa sitasi telah dihapus | **Mikroklimat IFWC (Tier B)**: Advisory berbasis persentil kelembapan relatif & literatur transfer. |
| **DS07** | **Produktivitas Kedelai & Batas ADM2** | Distanhor Jabar (`od_18105`) & GeoBoundaries | 27 Kabupaten/Kota Se-Jawa Barat | Tahunan Agregat<br>(2015–2022, 8 thn) | CSV (~15 KB)<br>216 baris (156 positif, 18 kab aktif) | **PANEL LAYAK (TIER A)**<br>14 sentra penuh 8 tahun | **Kandidat Portofolio Tier A**: Diuji pada Phase 6 EDA berdampingan dengan Padi dan Jagung. |
| **DS08** | **Produksi Fisik & Luas Panen (Padi, Jagung, Kedelai)** | Distanhor Jabar / Galura Open Data | 27 Kabupaten/Kota Se-Jawa Barat | Tahunan Agregat<br>(2013/2015–2022) | CSV (5 file, ~64 KB)<br>Padi, Jagung, Kedelai | **IDENTITAS MATEMATIKA VALID**<br>$\text{Yield} = \frac{\text{Prod}\times 10}{\text{Area}}$ | **Auxiliary Panel Analysis**: Mendekomposisi apakah lonjakan produktivitas berasal dari penyusutan luas panen. |
| **DS09** | **Kovariat Iklim Makro (ONI, DMI) & Validasi CHIRPS** | NOAA CPC, NOAA PSL, NOAA CoastWatch ERDDAP | Pasifik (Niño 3.4), Samudera Hindia, & 9 Kab Jabar | Bulanan & Harian<br>(2015–2024) | ASCII, CSV (~210 KB) | **VALIDASI SILANG LENGKAP**<br>Menuntaskan Blocker B3 | **Variabel Kontrol Makro**: Menangkap guncangan iklim El Niño / IOD dan memvalidasi presipitasi AgERA5. |

---

## 📑 Daftar Dokumen Penjelasan Rinci

1. [01_DS01_agera5_weather.md](01_DS01_agera5_weather.md) — 24 variabel agrometeorologi harian, cakupan lengkap 27 Kabupaten/Kota, satuan presipitasi mm/hari, validasi independen satelit CHIRPS v2 di Tasikmalaya, dan representasi elevasi centroid.
2. [02_DS02_bangladesh_rice_panel.md](02_DS02_bangladesh_rice_panel.md) — DOI resmi terverifikasi, panel 64 distrik, dekomposisi 3 musim (Aus/Aman/Boro), dan peran benchmark metodologis Two-Way FE.
3. [03_DS03_west_java_rice.md](03_DS03_west_java_rice.md) — Nama kolom aktual `produktivitas_padi2`, pembuktian artefak seri 2019 (+23.7% akibat rasio konversi GKP vs GKG ~1.19), dan koreksi klaim $R^2$.
4. [04_DS04_indonesia_agroclimatic.md](04_DS04_indonesia_agroclimatic.md) — DOI resmi terverifikasi, peran terbatas sebagai validasi silang (cross-validation), perbandingan resolusi 0.5° vs 0.1°, dan peringatan konsistensi pipeline mandiri.
5. [05_DS05_subang_maize.md](05_DS05_subang_maize.md) — Subang sebagai outlier lokal (+4.93 ku/ha/thn vs sentra lain yang datar), standardisasi formula CV residual ($\text{ddof}=1 \rightarrow 12.21\%$), dan status hipotesis KSA jagung.
6. [06_DS06_west_java_horticulture_chili_tomato.md](06_DS06_west_java_horticulture_chili_tomato.md) — Nama kolom aktual `komoditi` dan `produktivitas_sayur_buah`, klarifikasi satuan (ku/ha vs ton), penghapusan ambang tanpa sitasi, dan opsi transparan IFWC persentil.
7. [07_soybean_and_spatial_geoboundaries.md](07_soybean_and_spatial_geoboundaries.md) — Perbandingan empiris sisi-demi-sisi kedelai (Tier A) vs tomat (Tier B), dan pemetaan 27 centroid geometris ADM2 GeoBoundaries.
8. [08_production_and_harvest_area.md](08_production_and_harvest_area.md) — Identitas matematika agronomis $\text{Yield} = \frac{\text{Produksi}\times 10}{\text{Luas Panen}}$, dekomposisi lonjakan jagung Subang (penyusutan luas panen), dan implikasi bobot panel.
9. [09_climate_covariates_and_chirps.md](09_climate_covariates_and_chirps.md) — Kovariat iklim makro NOAA ONI (ENSO) dan DMI (IOD), pembuktian curah hujan orografis Tasikmalaya (>4.000 mm/tahun) via satelit-gauge independen CHIRPS v2.
