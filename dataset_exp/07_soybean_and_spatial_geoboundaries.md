# 🧬 DS07 — Kedelai Jawa Barat & Batas Geospasial ADM2 Centroids

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS07_spatial_geoboundaries` / `produktivitas_kedelai_jabar.csv`
* **Penerbit Data Statistik:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Jawa Barat / Open Data Jabar
* **Penerbit Data Spasial:** **geoBoundaries (USAID / William & Mary)** — open administrative boundary database (ADM2 Jawa Barat)
* **Endpoint API Resmi:** `https://galura.jabarprov.go.id/api/bigdata/od_18105_produktivitas_kedelai_berdasarkan_kabupatenkota`
* **Format File Lokal:**
  * `data/raw/produktivitas_kedelai_jabar.csv` (~15 KB, 216 baris)
  * `reports/dataset_audit/jabar_27_kabkota_centroids.csv` (~3 KB, 27 wilayah)
  * `data/raw/DS07_spatial_geoboundaries/jawa_barat_provinsi.geojson` (~45 KB, MultiPolygon Jawa Barat)
* **Rentang Waktu:** 8 Tahun Penuh (**2015 s.d. 2022**).

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:** **27 Kabupaten/Kota Se-Jawa Barat** (dengan visualisasi poligon batas provinsi dan titik centroid 27 wilayah).
* **Rentang Waktu:** 8 Tahun (**2015 s.d. 2022**).
* **Jumlah Observasi:** 216 baris ($27	ext{ kab/kota} 	imes 8	ext{ tahun}$).
  * 156 baris bernilai positif ($>0	ext{ ku/ha}$), 60 baris bernilai nol (terkonsentrasi pada 9 Kota non-pertanian).

---

## 3. Kamus Data Lengkap Seluruh Kolom Aktual

### A. File `produktivitas_kedelai_jabar.csv` (8 Kolom Lengkap)
| No | Nama Kolom Aktual | Tipe Data | Satuan | Deskripsi & Interpretasi | Catatan Kritis |
| :---: | :--- | :---: | :---: | :--- | :--- |
| 1 | `id` | Integer | ID Unik | ID unik record sistem Galura | Primary key sistem |
| 2 | `kode_provinsi` | Integer | Kode BPS | `32` (Kode resmi Provinsi Jawa Barat) | Standar Kemendagri |
| 3 | `nama_provinsi` | String | Teks | `JAWA BARAT` | Entitas level ADM1 |
| 4 | `kode_kabupaten_kota`| Integer | Kode BPS | Kode administratif 27 Kabupaten/Kota | Kunci relasi ADM2 |
| 5 | `nama_kabupaten_kota`| String | Teks | Nama resmi Kabupaten/Kota | 18 Kab & 9 Kota |
| 6 | `produktivitas_kedelai`| Float | Kuintal / Ha | Rata-rata hasil panen kedelai per hektar | Target luaran pemodelan |
| 7 | `satuan` | String | Teks | `KUINTAL/HEKTAR` | Satuan resmi dinas |
| 8 | `tahun` | Integer | Tahun | Tahun kalender observasi (**2015 s.d. 2022**) | Rentang 8 tahun |

### B. File `jabar_27_kabkota_centroids.csv` & `spatial_audit.csv` (8 Kolom Lengkap)
| No | Nama Kolom Aktual | Tipe Data | Satuan | Deskripsi & Interpretasi |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `nama_kabupaten_kota` | String | Teks | Nama lengkap 27 Kabupaten/Kota |
| 2 | `tipe_wilayah` | String | Kategori | `KABUPATEN` (18 wilayah) atau `KOTA` (9 wilayah) |
| 3 | `true_centroid_lat` | Float | Derajat Desimal | Lintang geografis centroid poligon ADM2 geoBoundaries |
| 4 | `true_centroid_lon` | Float | Derajat Desimal | Bujur geografis centroid poligon ADM2 geoBoundaries |
| 5 | `luas_approx_km2` | Float | $	ext{km}^2$ | Estimasi luas wilayah poligon dalam kilometer persegi |
| 6 | `n_sel_agera5_0_1deg` | Integer | Jumlah Sel | Jumlah sel grid AgERA5 ($0.1^\circ 	imes 0.1^\circ$) yang berada di dalam wilayah |
| 7 | `shape_name_geoboundaries`| String | Teks | Nama wilayah padanan pada database geoBoundaries global |
| 8 | `shape_type` | String | Teks | Tipe entitas administrasi (`Regency`, `City`, `County`) |

### C. File Geospasial `jawa_barat_provinsi.geojson`
* **Format:** GeoJSON RFC 7946 / EPSG:4326.
* **Geometri:** `MultiPolygon` resmi batas daratan dan kepulauan Provinsi Jawa Barat (Bounds: $106.37^\circ - 108.83^\circ	ext{ BT}, -7.82^\circ - -5.92^\circ	ext{ LS}$).
* **Fungsi:** Membentuk siluet visual peta wilayah Provinsi Jawa Barat yang akurat saat diplot di notebook.

---

## 4. Perbandingan Empiris: Kedelai (DS07) vs Tomat (DS06)

| Dimensi Evaluasi | Kedelai (DS07) | Tomat (DS06) | Implikasi bagi Sistem TaniAdapt |
| :--- | :--- | :--- | :--- |
| **Resolusi Spasial** | Tingkat Kabupaten (ADM2) | Tingkat Provinsi (ADM1 agregat) | Kedelai memiliki variasi lokal antar-kabupaten |
| **Total Observasi** | 216 baris (156 positif) | 9 baris ($N=9$ tahun) | Kedelai memiliki sampel 24x lebih besar |
| **Sentra Runtun Penuh**| 14 kabupaten penuh 8 thn | 0 (data kabupaten tidak ada) | Kedelai layak untuk ekonometrika panel |
| **Dukungan Literatur** | Paper 13 & 14 di repo | Tidak ada paper spesifik tomat | Kedelai didukung literatur empiris repo |
| **Arsitektur Advisory** | **Tier A (Panel Regression)**| **Tier B (IFWC Mikroklimat)**| Tomat berbagi modul kelembapan dengan Cabai |

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import geopandas as gpd
import pandas as pd
from pathlib import Path

csv_kedelai = Path("data/raw/produktivitas_kedelai_jabar.csv")
geojson_path = Path("data/raw/DS07_spatial_geoboundaries/jawa_barat_provinsi.geojson")

df_ked = pd.read_csv(csv_kedelai)
gdf_jabar = gpd.read_file(geojson_path)

print(f"Dimensi Data Kedelai: {df_ked.shape}")
print(f"Geometri Batas Provinsi: {gdf_jabar.geometry.iloc[0].geom_type}")
```
