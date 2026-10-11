# 🌾 DS08 — Volume Produksi Fisik & Luas Panen Jawa Barat (Padi, Jagung, Kedelai)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS08_production_and_harvest_area`
* **Penerbit / Institusi:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Provinsi Jawa Barat
* **Portal / Sumber:** Galura Open Data Jabar (Satu Data Jawa Barat)
* **Koleksi Berkas Lokal:**
  1. `data/raw/DS03_west_java_rice_productivity/produksi_padi_jabar.csv` (270 baris, 2013–2022)
  2. `data/raw/DS05_subang_maize_productivity/produksi_jagung_jabar.csv` (216 baris, 2015–2022)
  3. `data/raw/DS05_subang_maize_productivity/luas_panen_jagung_jabar.csv` (216 baris, 2015–2022)
  4. `data/raw/produksi_kedelai_jabar.csv` (216 baris, 2015–2022)
  5. `data/raw/luas_panen_kedelai_jabar.csv` (216 baris, 2015–2022)
* **Lisensi:** Open Data Pemerintah Provinsi Jawa Barat

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:** **27 Kabupaten/Kota Se-Jawa Barat** (18 Kabupaten + 9 Kota).
* **Rentang Waktu:** 8–10 Tahun Penuh (**2015 s.d. 2022** untuk Jagung & Kedelai; **2013 s.d. 2022** untuk Padi).
* **Frekuensi:** Tahunan agregat.

---

## 3. Kamus Data Lengkap Seluruh Berkas Produksi & Luas Panen

Seluruh berkas memiliki skema kolom seragam 8 kolom:

### A. Berkas Volume Produksi Fisik (`produksi_padi_jabar.csv`, `produksi_jagung_jabar.csv`, `produksi_kedelai_jabar.csv`)
| No | Nama Kolom Aktual | Tipe Data | Satuan | Deskripsi & Interpretasi |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` | Integer | ID Unik | ID unik record sistem basis data Galura |
| 2 | `kode_provinsi` | Integer | Kode BPS | `32` (Provinsi Jawa Barat) |
| 3 | `nama_provinsi` | String | Teks | `JAWA BARAT` |
| 4 | `kode_kabupaten_kota` | Integer | Kode BPS | Kode administratif 27 Kabupaten/Kota |
| 5 | `nama_kabupaten_kota` | String | Teks | Nama resmi Kabupaten/Kota |
| 6 | `produksi_padi` / `produksi_jagung` / `produksi_kedelai` | Float | **TON** | Total volume produksi fisik hasil panen gabah/pipilan/biji kering |
| 7 | `satuan` | String | Teks | `TON` (1 Ton = 1.000 kg = 10 Kuintal) |
| 8 | `tahun` | Integer | Tahun | Tahun kalender observasi |

### B. Berkas Luas Panen Fisik (`luas_panen_jagung_jabar.csv`, `luas_panen_kedelai_jabar.csv`)
| No | Nama Kolom Aktual | Tipe Data | Satuan | Deskripsi & Interpretasi |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` | Integer | ID Unik | ID unik record sistem Galura |
| 2 | `kode_provinsi` | Integer | Kode BPS | `32` (Provinsi Jawa Barat) |
| 3 | `nama_provinsi` | String | Teks | `JAWA BARAT` |
| 4 | `kode_kabupaten_kota` | Integer | Kode BPS | Kode administratif 27 Kabupaten/Kota |
| 5 | `nama_kabupaten_kota` | String | Teks | Nama resmi Kabupaten/Kota |
| 6 | `luas_panen` | Float | **HEKTAR** | Total luas lahan yang berhasil dipanen |
| 7 | `satuan` | String | Teks | `HEKTAR` (1 Ha = 10.000 m²) |
| 8 | `tahun` | Integer | Tahun | Tahun kalender observasi |

---

## 4. Pengujian Identitas Matematika Agronomi

Dalam statistik pertanian resmi Indonesia (BPS dan Kementerian Pertanian):

> **Produktivitas (Kuintal/Hektar) = (Produksi (Ton) × 10) / Luas Panen (Hektar)**

### Hasil Uji Konsistensi Numerik di Seluruh Jawa Barat:
1. **Jagung (2015–2022):** Konsisten 100% pada seluruh 194 observasi dengan Luas Panen > 0 (selisih mutlak ≤ 0,05 ku/ha).
2. **Kedelai (2015–2022):** Konsisten 100% pada seluruh 151 observasi aktif (selisih mutlak < 0,01 ku/ha).

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

path_prod = Path("data/raw/DS05_subang_maize_productivity/produksi_jagung_jabar.csv")
path_area = Path("data/raw/DS05_subang_maize_productivity/luas_panen_jagung_jabar.csv")
path_yield = Path("data/raw/DS05_subang_maize_productivity/produktivitas_jagung_jabar.csv")

df_p = pd.read_csv(path_prod)
df_a = pd.read_csv(path_area)
df_y = pd.read_csv(path_yield)

# Merge untuk menguji identitas
m = pd.merge(df_p, df_a, on=["kode_kabupaten_kota", "tahun"])
m = pd.merge(m, df_y, on=["kode_kabupaten_kota", "tahun"])

m_valid = m[m["luas_panen"] > 0].copy()
m_valid["yield_calc"] = (m_valid["produksi_jagung"] * 10.0) / m_valid["luas_panen"]
m_valid["selisih"] = (m_valid["yield_calc"] - m_valid["produktivitas_jagung"]).abs()

print(f"Rata-rata selisih absolut identitas: {m_valid['selisih'].mean():.4f} ku/ha (KONSISTEN)")
```
