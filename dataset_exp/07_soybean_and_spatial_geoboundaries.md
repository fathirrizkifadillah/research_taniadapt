# 🧬 Data Ekstensi — Kedelai Jawa Barat & Geospasial ADM2 Centroids

## 1. Produktivitas Kedelai Jawa Barat (`produktivitas_kedelai_jabar.csv`)

### A. Identitas Dataset & Sumber Resmi
* **Penerbit / Sumber:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Jawa Barat / Galura Open Data Jabar
* **Endpoint API Resmi:** `https://galura.jabarprov.go.id/api/bigdata/od_18105_produktivitas_kedelai_berdasarkan_kabupatenkota`
* **Format File Lokal:** CSV di `data/raw/produktivitas_kedelai_jabar.csv`
* **Ukuran:** ~15 KB (216 baris lengkap, 27 kabupaten/kota $\times$ 8 tahun: 2015 s.d. 2022)

### B. Distribusi Nilai & Fakta Empiris
Audit empiris terhadap dataset kedelai menunjukkan:
* **Total Baris:** 216 baris panel ($27\text{ kab/kota} \times 8\text{ tahun}$).
* **Baris Bernilai Positif ($>0$ Ku/Ha):** **156 baris ($72,2\%$)**.
* **Baris Bernilai Nol ($=0$ Ku/Ha):** **60 baris ($27,8\%$)** — terkonsentrasi pada 9 wilayah perkotaan (KOTA) non-agraris.
* **Missing Value (NaN / Null):** **0 baris ($0,0\%$)**.
* **Kelayakan Spasial Panel:**
  * Sebanyak **18 dari 27 kabupaten/kota** memiliki aktivitas tanam kedelai aktif $\ge 6$ dari 8 tahun.
  * Sebanyak **14 kabupaten sentra utama** memiliki data positif **8 tahun penuh tanpa putus**.
  * Rata-rata produktivitas pada unit positif adalah $15,16\text{ ku/ha}$ dengan CV mentah $23,18\%$ dan CV residual detrended $22,98\%$.

### C. Perbandingan Empiris Sisi-demi-Sisi: Kedelai vs Tomat (Audit 0.4)
Alih-alih mengunci pilihan berdasarkan asumsi kedekatan famili taksonomi, perbandingan objektif berbasis bukti adalah sebagai berikut:

| Dimensi Evaluasi | Kedelai (DS_EXT) | Tomat (DS06) | Implikasi bagi Sistem |
| :--- | :--- | :--- | :--- |
| **Resolusi Spasial** | Tingkat Kabupaten (ADM2) | Tingkat Provinsi (ADM1 agregat) | Kedelai memiliki variasi lokal antar-kabupaten |
| **Total Observasi** | 216 baris (156 positif) | 9 baris ($N=9$ tahun) | Kedelai memiliki sampel 24x lebih besar |
| **Sentra Runtun Penuh** | 14 kabupaten penuh 8 thn | 0 (data kabupaten tidak ada) | Kedelai layak untuk ekonometrika panel |
| **Dukungan Literatur** | Paper 13 & 14 di repo | Tidak ada paper spesifik tomat | Kedelai didukung literatur empiris repo |
| **Arsitektur Advisory** | **Tier A (Panel Regression)** | **Tier B (IFWC Mikroklimat)** | Tomat berbagi modul kelembapan dengan Cabai |

*Usulan Arsitektur*: Padi, Jagung, dan Kedelai dialokasikan sebagai **Tier A** (diuji sinyal cuacanya pada Phase 6 EDA; dieleminasi jika tidak terbukti ada sinyal). Cabai dan Tomat dialokasikan sebagai **Tier B** (advisory mikroklimat berbasis aturan literatur dan kelembapan relatif, tanpa regresi hasil panen).

---

## 2. Batas Geospasial Poligon ADM2 & Centroid Geografis

### A. Sumber Data Geospasial
* **Sumber:** **geoBoundaries (USAID / William & Mary)** — open administrative boundary database (ADM2 Jawa Barat).
* **Koreksi Istilah:** Titik centroid yang dihitung adalah **Centroid Geometris Wilayah Administratif (*Geometric Centroid*)**, **BUKAN titik berat lahan pertanian**. Titik berat lahan pertanian memerlukan data spasial tutupan lahan (*land cover crop mask*) seperti ESA WorldCover.
* **File Output:**
  * `reports/dataset_audit/jabar_27_kabkota_spatial_audit.csv`
  * `reports/dataset_audit/jabar_27_kabkota_centroids.csv`

### B. Distribusi Sel Grid AgERA5 0.1° per Poligon Kabupaten

| Nama Wilayah | Tipe | Centroid Geometris (Lat, Lon) | Luas Approx ($km^2$) | Jumlah Sel AgERA5 (0.1°) |
| :--- | :--- | :--- | :--- | :--- |
| **KABUPATEN SUKABUMI** | Kabupaten | -7.0762, 106.7073 | 4.199 km² | **36 sel grid** |
| **KABUPATEN CIANJUR** | Kabupaten | -7.1337, 107.1578 | 3.623 km² | **30 sel grid** |
| **KABUPATEN GARUT** | Kabupaten | -7.3596, 107.7889 | 3.117 km² | **25 sel grid** |
| **KABUPATEN SUBANG** | Kabupaten | -6.4830, 107.7322 | 2.187 km² | **18 sel grid** |
| **KABUPATEN KARAWANG**| Kabupaten | -6.2520, 107.3542 | 1.927 km² | **16 sel grid** |
| **KABUPATEN INDRAMAYU**| Kabupaten | -6.4488, 108.1686 | 2.098 km² | **17 sel grid** |
| **KOTA BANDUNG** | Kota | -6.9175, 107.6191 | 167 km² | **2 sel grid** |

---

## 3. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

csv_kedelai = Path("data/raw/produktivitas_kedelai_jabar.csv")
df_ked = pd.read_csv(csv_kedelai)

print(f"Dimensi Data Kedelai: {df_ked.shape}")
print(f"Kolom Aktual: {df_ked.columns.tolist()}")

# Hitung jumlah observasi positif dan mean per kabupaten
positive_ked = df_ked[df_ked['produktivitas_kedelai'] > 0]
kab_stats = positive_ked.groupby('nama_kabupaten_kota')['produktivitas_kedelai'].agg(['count', 'mean']).reset_index()
print(f"\nJumlah Kabupaten Aktif Kedelai: {len(kab_stats)}")
print("Contoh 5 Sentra Utama Kedelai:")
print(kab_stats.sort_values('count', ascending=False).head())
```
