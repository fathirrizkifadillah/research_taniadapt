# TaniAdapt Research Dossier — Phase 3: Dataset Discovery & Multi-Source Fusion

**Status**: COMPLETED / RATIFIED  
**Ruang Lingkup**: Evaluasi 20 Kandidat Dataset dan Integrasi 9 Dataset Terpilih (DS01 s/d DS09)  
**Tujuan**: Membangun Fondasi Data Geospasial, Iklim Reanalysis, dan Statistik Produksi Jawa Barat yang Konsisten

---

## 1. Inventaris dan Spesifikasi 9 Dataset Terpilih (Data Fusion)

| ID Dataset | Nama & Penyedia Data | Cakupan Wilayah | Resolusi Temporal | Resolusi Spasial | Format Data & Skema Kunci |
|---|---|---|:---:|:---:|---|
| **DS01** | **Copernicus AgERA5 (ECMWF)** | Jawa Barat (22 Grid Cells) | Harian (1991–2024) | Grid $0.1^\circ$ (~10 km) | CSV: Suhu 2m (min/mean/max), Titik Embun, Presipitasi, Radiasi Surya, Kecepatan Angin 10m, dan $ET_0$ Penman-Monteith. |
| **DS02** | **CHIRPS (UCSB CHC)** | Jawa Barat (27 Kab/Kota) | Harian & Bulanan (2015–2024) | Grid $0.05^\circ$ (~5 km) | NetCDF/CSV: Estimasi curah hujan satelit inframerah terkalibrasi stasiun bumi untuk audit bias hujan AgERA5. |
| **DS03** | **BPS Jabar — Padi Sawah Tradisional** | 27 Kabupaten/Kota | Tahunan (2015–2017) | Tingkat Kabupaten (ADM2) | CSV/PDF: Luas Panen (ha), Produksi (ton), dan Produktivitas (ku/ha) pra-metode KSA (N=54 valid). |
| **DS04** | **BPS Jabar — Padi KSA Modern** | 27 Kabupaten/Kota | Bulanan/Subround (2018–2024) | Tingkat Kabupaten (ADM2) | CSV: Luas panen berbasis Kerangka Sampel Area citra satelit dan amatan fase vegetatif bulanan. |
| **DS05** | **Open Data Jabar — Jagung** | 27 Kabupaten/Kota | Tahunan (2015–2021) | Tingkat Kabupaten (ADM2) | CSV: Luas panen, produksi, produktivitas jagung pipil (18 sentra utama aktif, N=124 valid). |
| **DS06** | **Open Data Jabar & SBS — Cabai & Tomat** | Agregat Jawa Barat | Bulanan/Tahunan (2017–2024) | Tingkat Provinsi (SBS) | CSV: Produksi dan luas panen hortikultura cabai besar, cabai rawit, dan tomat sayur (N=8 per komoditas). |
| **DS07** | **Open Data Jabar — Kedelai & GeoJSON** | 27 Kabupaten/Kota | Tahunan (2015–2021) | Spasial Poligon ADM2 | CSV & GeoJSON: Data produksi kedelai 17 sentra dan batas poligon wilayah batas administrasi Jawa Barat. |
| **DS08** | **BPS Statistik Pertanian Jawa Barat** | 27 Kabupaten/Kota | Tahunan (2015–2021) | Tingkat Kabupaten (ADM2) | CSV: Buku statistik kompilasi dinas pertanian, luas baku sawah, irigasi teknis/tadah hujan, dan komoditas palawija. |
| **DS09** | **Indeks Iklim Global & BMKG History** | Samudera Pasifik & Hindia | Bulanan (1991–2024) | Indeks Global / Lokal | CSV: Oceanic Niño Index (ONI / ENSO), Dipole Mode Index (DMI / IOD), dan kronik kejadian bencana iklim BMKG Jabar. |

---

## 2. Matriks Penautan Silang Antar-Dataset (Cross-Dataset Linking Matrix)
Tantangan terbesar fusi data multi-sumber di Indonesia adalah ketidakselarasan penamaan administratif dan resolusi grid:
1. **Penyelarasan Kode Administratif ADM2**:
   * Nama kabupaten BPS (mis. "BOGOR", "BANDUNG", "GARUT") diselaraskan menggunakan standar penamaan kanonik uppercase bebas spasi dan prefiks (`KABUPATEN_` / `KOTA_`).
2. **Penetapan Koordinat Centroid Wilayah**:
   * Centroid dihitung dari poligon batas resmi Jawa Barat (`data/raw/DS07_spatial/jabar_kabupaten_boundary.geojson`).
3. **Pencocokan Titik Grid AgERA5 Terdekat (Nearest Weather Grid)**:
   * Menggunakan algoritma jarak Haversine bola bumi pada koordinat grid $0.1^\circ$ Copernicus.
   * Ditemukan total **22 sel AgERA5 unik** yang mewakili seluruh 27 Kabupaten/Kota di Jawa Barat.
4. **Koreksi Elevasi Topografi SRTM DEM**:
   * Ketinggian stasiun cuaca reanalysis dicocokkan dengan elevasi rata-rata lahan pertanian menggunakan raster elevasi SRTM 90m DEM.
   * Disimpan sebagai tabel lookup kanonik: `data/processed/lookup_kab_cell_elev.csv`.
