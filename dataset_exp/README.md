# 📊 TaniAdapt Dataset Landscape & Data Dictionaries (`dataset_exp/`)

> **Tentang Direktori Ini:**  
> Seluruh file data mentah berukuran besar (*raw files* seperti Parquet dan CSV ribuan baris di direktori `data/raw/`) dikecualikan dari Git melalui `.gitignore` demi efisiensi repositori.  
> Direktori `dataset_exp/` ini berfungsi sebagai **dokumentasi data kanonikal** yang dapat dibaca langsung di GitHub maupun oleh asisten AI (seperti Claude), mencakup: asal sumber data, struktur tabel, variabel, rentang waktu, temuan empiris audit, hingga batasan agronomisnya.

---

## 🗺️ Master Dataset Matrix (TaniAdapt Portfolio)

| ID | Nama Dataset | Institusi Sumber & Endpoint | Cakupan Spasial | Frekuensi & Periode | Format & Dimensi | Status Kualitas | Peran di TaniAdapt |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DS01** | **AgERA5 Agrometeorological Indicators** | Copernicus CDS (ECMWF)<br>`sis-agrometeorological-indicators` | 7 Titik Koordinat Jabar (Bandung, Karawang, dll.) | Harian<br>(2015–2024, 10 thn) | CSV (7 file, ~7 MB)<br>25.571 baris total, 24 var | **PASS**<br>(0 null, lolos hukum fisika) | **Backbone Cuaca Mikro**: Suhu, hujan, VPD, radiasi, dan kelembapan. |
| **DS02** | **Bangladesh Rice Panel** | Mendeley Data / BRRI & BMD<br>`DOI: 10.17632/m44r329k8h.1` | 64 Distrik di Bangladesh | Musiman/Tahunan<br>(2015–2024, 10 thn) | CSV (~84 KB)<br>Aus, Aman, Boro | **BENCHMARK ONLY**<br>(Bukan data lokal Jabar) | **Metode Benchmark**: Referensi ekonometrik *Two-Way Fixed Effects*. |
| **DS03** | **Produktivitas Padi Jawa Barat** | Distanhor Jabar / Galura API<br>`od_18103_produktivitas_padi...` | 27 Kabupaten/Kota Se-Jawa Barat | Tahunan Agregat<br>(2015–2020, 6 thn) | CSV & JSON (~12 KB)<br>162 baris per varian (Padi Total, Sawah, Ladang) | **PASS**<br>(0 null, tren stasioner) | **Target Outcome Padi**: Target hasil panen padi lokal tahunan. |
| **DS04** | **Indonesia Nationwide Agroclimate** | Elsevier / Mendeley Data<br>`DOI: 10.17632/3pfbdbdkm3.1` | 612 Titik Daratan RI<br>(14 titik di Jawa Barat) | Harian<br>(2016–2025, 10 thn) | Parquet (~60 MB)<br>12 derived indicators | **PASS**<br>(Konsistensi internal ERA5) | **Backbone Kekeringan/Neraca Air**: CDD, CWD, Water Balance, Rainfall 7d/30d/90d. |
| **DS05** | **Produktivitas Jagung Jabar & Subang** | Distanhor Jabar / Galura API<br>`od_18104_produktivitas_jagung...` | 27 Kabupaten/Kota Se-Jawa Barat (Fokus: Subang) | Tahunan Agregat<br>(2015–2022, 8 thn) | CSV & JSON (~16 KB)<br>216 baris lengkap | **PASS (Detrend Required)**<br>Subang $R^2=0.739$, resid CV $11.42\%$ | **Target Outcome Jagung**: Model regresi cuaca-hasil panen dengan detrending. |
| **DS06** | **Hortikultura SBS Cabai & Tomat** | Distanhor Jabar / Galura API<br>`od_18100_produktivitas_sayuran...` | Agregat Provinsi Jawa Barat | Tahunan Agregat<br>(2017–2024, 8 thn) | CSV & JSON (~17 KB)<br>Cabai Besar, Rawit, Tomat | **PASS (Yield Only)**<br>❌ Tanpa label penyakit OPT | **Target Outcome Hortikultura & IFWC**: Advisory penyakit via proksi mikroklimat. |
| **DS-EXT1** | **Produktivitas Kedelai Jawa Barat** | Distanhor Jabar / Galura API<br>`od_18105_produktivitas_kedelai...` | 27 Kabupaten/Kota Se-Jawa Barat | Tahunan Agregat<br>(2015–2022, 8 thn) | CSV (~15 KB)<br>216 baris (156 positif, 60 nol) | **PASS**<br>(18 kab aktif $\ge 6$ thn) | **Kandidat Portofolio Tanaman Pangan**: Komparasi kelayakan kedelai vs tomat. |
| **DS-EXT2** | **Batas Geospasial ADM2 & Centroid** | GeoBoundaries (USAID / William & Mary) | 27 Poligon Kabupaten/Kota Jawa Barat | Statis | GeoJSON & CSV (~2 KB)<br>Centroid sejati + sel grid | **VERIFIED**<br>Koordinat titik berat poligon | **Penghubung Spasial**: Ekstraksi cuaca presisi ke poligon kabupaten non-pilot. |

---

## 📑 Daftar Dokumen Penjelasan Rinci

Silakan buka masing-masing file markdown di direktori ini untuk melihat kamus data lengkap per dataset:

1. [01_DS01_agera5_weather.md](01_DS01_agera5_weather.md) — 24 variabel agrometeorologi harian, 7 titik koordinat, uji hukum fisika atmosfer, dan fenomena orografis Tasikmalaya.
2. [02_DS02_bangladesh_rice_panel.md](02_DS02_bangladesh_rice_panel.md) — Struktur panel 64 distrik, dekomposisi musiman Aus/Aman/Boro, dan fungsi sebagai benchmark ekonometrik.
3. [03_DS03_west_java_rice.md](03_DS03_west_java_rice.md) — Data panel 27 kab/kota padi Jawa Barat, bukti tren stasioner, dan analisis shock makro seragam 2019–2020.
4. [04_DS04_indonesia_agroclimatic.md](04_DS04_indonesia_agroclimatic.md) — Indikator kekeringan Consecutive Dry Days (CDD), CWD, rolling rainfall, dan neraca air 14 grid Jawa Barat.
5. [05_DS05_subang_maize.md](05_DS05_subang_maize.md) — Analisis lonjakan produktivitas Subang (+56.4%), resolusi bug formula $R^2=0.739$, transisi BPS KSA Jagung, dan evaluasi 3 metode detrending.
6. [06_DS06_west_java_horticulture_chili_tomato.md](06_DS06_west_java_horticulture_chili_tomato.md) — Data statistik hasil panen cabai/tomat, pembuktian ketiadaan label OPT lapangan, dan perumusan Index of Favorable Weather Condition (IFWC).
7. [07_soybean_and_spatial_geoboundaries.md](07_soybean_and_spatial_geoboundaries.md) — Pembuktian data kedelai (156 baris positif), pemilihan Tomat sebagai tanaman ke-4, dan pemetaan 27 centroid poligon GeoBoundaries.

---

## ⚙️ Cara Mereplikasi & Menjalankan Ulang Data
Seluruh data dapat diunduh ulang atau diaudit kapan saja menggunakan script di folder `scripts/`:
- **Audit Kualitas Menyeluruh:** `python scripts/run_quality_audit.py`
- **Analisis Regresi Tren & Lonjakan Subang:** `python scripts/analyze_trends_and_breaks.py`
- **Audit Literatur Riset:** `python scripts/audit_paper_citations.py`
- **Ekstraksi Spasial Centroid:** `python scripts/compute_true_centroids_and_cells.py`
- **Jupyter Notebooks Interaktif:** Buka folder `notebook/` dan jalankan `Run All` pada masing-masing file `.ipynb`.
