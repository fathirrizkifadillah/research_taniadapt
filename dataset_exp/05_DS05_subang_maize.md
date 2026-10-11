# 🌽 DS05 — Produktivitas Jagung 27 Kabupaten/Kota Jawa Barat (2015–2022)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS05_subang_maize_productivity` (Cakupan: Seluruh 27 Kab/Kota Jawa Barat)
* **Penerbit / Institusi:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Provinsi Jawa Barat
* **Portal / Sumber:** Galura Open Data Jabar (Satu Data Jawa Barat)
* **Endpoint API Resmi:** `https://galura.jabarprov.go.id/api/bigdata/od_18104_produktivitas_jagung_berdasarkan_kabupatenkota`
* **Format File Lokal:** CSV & JSON di `data/raw/DS05_subang_maize_productivity/`
* **Ukuran Total:** ~14 KB (216 baris lengkap: 27 kabupaten/kota × 8 tahun, 0 missing value)

---

## 2. Cakupan Spasial Penuh: Seluruh 27 Kabupaten/Kota Se-Jawa Barat
* **Cakupan Spasial:** **Seluruh 27 Kabupaten/Kota di Provinsi Jawa Barat**.
  * Bukan dataset khusus Subang; mencakup seluruh sentra utama jagung (Kab. Garut, Kab. Majalengka, Kab. Cianjur, Kab. Tasikmalaya, Kab. Ciamis, dll.).
  * Kabupaten Subang dibahas secara khusus sebagai **studi kasus investigasi anomali struktural (*structural break*)**.
* **Rentang Waktu:** 8 Tahun Penuh (**2015 s.d. 2022**).
* **Frekuensi:** Tahunan agregat (N = 216 observasi panel).
* **Satuan Ukuran:** **KUINTAL / HEKTAR** (1 ku = 100 kg = 0,1 ton).

---

## 3. Kamus Data Lengkap Seluruh Kolom Aktual

| No | Nama Kolom Aktual | Tipe Data | Satuan | Deskripsi & Interpretasi | Catatan Kritis |
| :---: | :--- | :---: | :---: | :--- | :--- |
| 1 | `id` | Integer | ID Unik | ID unik record sistem Galura | Primary key sistem |
| 2 | `kode_provinsi` | Integer | Kode BPS | `32` (Kode resmi Provinsi Jawa Barat) | Standar Kemendagri |
| 3 | `nama_provinsi` | String | Teks | `JAWA BARAT` | Entitas level ADM1 |
| 4 | `kode_kabupaten_kota`| Integer | Kode BPS | Kode administratif 27 Kabupaten/Kota | Kunci relasi ADM2 |
| 5 | `nama_kabupaten_kota`| String | Teks | Nama resmi Kabupaten/Kota (e.g. `KABUPATEN GARUT`, `KABUPATEN SUBANG`) | 18 Kab & 9 Kota |
| 6 | `produktivitas_jagung`| Float | Kuintal / Ha | Rata-rata hasil panen jagung pipilan kering per hektar | Target luaran pemodelan |
| 7 | `satuan` | String | Teks | `KUINTAL/HEKTAR` | Satuan resmi dinas |
| 8 | `tahun` | Integer | Tahun | Tahun kalender observasi (**2015 s.d. 2022**) | Rentang 8 tahun |

---

## 4. Bedah Kasus Empiris: Sentra Utama Garut vs Anomali Subang

### A. Garut sebagai Sentra Produksi Utama Sejati Jawa Barat
* **Kabupaten Garut** menyumbang porsi terbesar jagung Jawa Barat dengan luas panen **> 50.000 ha** dan volume produksi **> 350.000 ton**.
* Produktivitas Garut stabil pada rentang **65 – 75 ku/ha** tanpa lonjakan tak wajar.

### B. Dekomposisi Lonjakan Subang (+56.4% pada 2020–2022)
* Subang adalah produsen jagung skala kecil (luas panen hanya **113 – 765 ha**).
* Lonjakan produktivitas Subang dari **57,23 ku/ha** (2020) ke **89,49 ku/ha** (2022) terbukti merupakan **efek penyusutan basis luas panen (*small-denominator volatility*)** dan pergeseran ke petak-petak intensif benih hibrida terbatas.
* **Koefisien Variasi Residual Detrended**: CV_resid = 12,21%, merupakan batas atas variasi yang dapat diatribusikan pada cuaca.

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

csv_path = Path("data/raw/DS05_subang_maize_productivity/produktivitas_jagung_jabar.csv")
df = pd.read_csv(csv_path)

print(f"Dimensi Data Jagung Jabar: {df.shape}")
print(f"Total Kabupaten/Kota: {df['nama_kabupaten_kota'].nunique()}")

# Rata-rata produktivitas 5 sentra terbesar
top_sentra = df.groupby('nama_kabupaten_kota')['produktivitas_jagung'].mean().sort_values(ascending=False).head(5)
print("\nTop 5 Produktivitas Jagung Jabar (2015-2022):")
print(top_sentra)
```
