# 🌶️ DS06 — Hortikultura Sayuran Buah Semusim (Cabai & Tomat)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS06_west_java_horticulture`
* **Penerbit / Institusi:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Provinsi Jawa Barat
* **Portal / Sumber:** Galura Open Data Jabar (Satu Data Jawa Barat)
* **Endpoint API Resmi:**
  * Produktivitas SBS: `https://galura.jabarprov.go.id/api/bigdata/od_18100_produktivitas_sayuran_buah_semusim_berdasarkan_komoditas`
  * Volume Produksi Sayuran: `https://galura.jabarprov.go.id/api/bigdata/od_18096_produksi_sayuran_berdasarkan_komoditas`
* **Format File Lokal:** CSV & JSON di `data/raw/DS06_west_java_horticulture/`
* **Ukuran Total:** ~76 KB (kombinasi 2 dataset)

---

## 2. Cakupan Spasial, Komoditas, & Rentang Waktu
* **Cakupan Spasial:**
  * `produktivitas_sbs_jabar.csv`: **Tingkat Agregat Provinsi Jawa Barat** (N = 9 baris observasi per komoditas, 2016–2024).
  * `produksi_sayuran_komoditas_jabar.csv`: **Tingkat Kabupaten/Kota** (volume produksi sayuran, 2016–2024).
* **Rentang Waktu:** 9 Tahun Penuh (**2016 s.d. 2024**).
* **Komoditas Utama yang Dipantau:** Cabai Rawit, Cabai Besar, Tomat, Bawang Merah.
* **Satuan Ukuran Aktual:**
  * Produktivitas SBS: **KUINTAL / HEKTAR** (1 ku = 100 kg = 0,1 ton).
  * Volume Produksi Sayuran: **TON** (bukan Kuintal).

---

## 3. Kamus Data Lengkap Seluruh Kolom Aktual

### A. File `produktivitas_sbs_jabar.csv` (7 Kolom Lengkap)
| No | Nama Kolom Aktual | Tipe Data | Satuan | Deskripsi & Interpretasi |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` | Integer | ID Unik | ID unik record sistem basis data Galura |
| 2 | `kode_provinsi` | Integer | Kode BPS | `32` (Kode resmi Provinsi Jawa Barat) |
| 3 | `nama_provinsi` | String | Teks | `JAWA BARAT` (Tingkat agregat ADM1) |
| 4 | `komoditi` | String | Kategori | Nama komoditas (`CABAI RAWIT`, `CABAI BESAR`, `TOMAT`, `BAWANG MERAH`) |
| 5 | `produktivitas_sayur_buah` | Float | Kuintal / Ha | Rata-rata produktivitas sayuran buah semusim tingkat provinsi |
| 6 | `satuan` | String | Teks | `KUINTAL/HEKTAR` |
| 7 | `tahun` | Integer | Tahun | Tahun kalender observasi (**2016 s.d. 2024**) |

### B. File `produksi_sayuran_komoditas_jabar.csv` (9 Kolom Lengkap)
| No | Nama Kolom Aktual | Tipe Data | Satuan | Deskripsi & Interpretasi |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` | Integer | ID Unik | ID unik record sistem Galura |
| 2 | `kode_provinsi` | Integer | Kode BPS | `32` (Jawa Barat) |
| 3 | `nama_provinsi` | String | Teks | `JAWA BARAT` |
| 4 | `kode_kabupaten_kota` | Integer | Kode BPS | Kode administratif 27 Kabupaten/Kota |
| 5 | `nama_kabupaten_kota` | String | Teks | Nama resmi Kabupaten/Kota (e.g. `KABUPATEN BANDUNG`, `KABUPATEN GARUT`) |
| 6 | `jenis_komoditas` | String | Kategori | Jenis komoditas hortikultura sayuran |
| 7 | `produksi_sayuran` | Float | Ton | Total volume produksi fisik sayuran |
| 8 | `satuan` | String | Teks | `TON` |
| 9 | `tahun` | Integer | Tahun | Tahun observasi (**2016 s.d. 2024**) |

---

## 4. Temuan Audit Metodologi (Yield vs Kejadian Penyakit OPT)

> [!IMPORTANT]
> **Ketiadaan Data Serangan Hama/Penyakit (OPT)**:
> 1. Dataset ini **HANYA BERISI ANGKA HASIL PANEN DAN VOLUME PRODUKSI**.
> 2. Dataset ini **TIDAK MEMILIKI LABEL PENYAKIT / HAMA (OPT)** (tidak ada data antraknosa, layu fusarium, atau hawar daun).
> 3. **Larangan Metodologis**: Dilarang melatih model Machine Learning klasifikasi atau probabilitas penyakit dari data panen tahunan makro.
> 4. **Arsitektur Advisory**: Menggunakan **Indeks Kondisi Cuaca Mendukung (IFWC)** berbasis depresiasi titik embun malam (T_min - T_dew) dan kelembapan diurnal relatif.

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

raw_dir = Path("data/raw/DS06_west_java_horticulture")
df_sbs = pd.read_csv(raw_dir / "produktivitas_sbs_jabar.csv")

print(f"Dimensi SBS Jabar: {df_sbs.shape}")
print(f"Kolom Aktual SBS: {df_sbs.columns.tolist()}")

# Filter komoditas cabai rawit dan cabai besar
chili_df = df_sbs[df_sbs['komoditi'].str.upper().str.contains('CABAI')].copy()
print("\nRingkasan Produktivitas Cabai Jabar (ku/ha):")
print(chili_df[['tahun', 'komoditi', 'produktivitas_sayur_buah', 'satuan']].sort_values(['komoditi', 'tahun']))
```
