# 🌾 DS03 — Produktivitas Padi Jawa Barat (Open Data Jabar)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS03_west_java_rice_productivity`
* **Nama Sumber:** Satu Data Jawa Barat (Open Data Jabar / Galura API)
* **Dataset ID:**
  * Padi Total: `od_18103_produktivitas_padi_berdasarkan_kabupatenkota`
  * Padi Sawah: `od_18099_produktivitas_padi_sawah_berdasarkan_kabupatenkota`
  * Padi Ladang: `od_18102_produktivitas_padi_ladang_berdasarkan_kabupatenkota`
* **Penerbit:** Dinas Tanaman Pangan dan Hortikultura Provinsi Jawa Barat
* **Lisensi:** Open Data Pemerintah Provinsi Jawa Barat (Bebas Riset)
* **Format File Lokal:** CSV dan JSON di `data/raw/DS03_west_java_rice_productivity/`
* **Ukuran Total:** ~11 KB per file (162 baris panel seimbang: 27 kabupaten/kota × 6 tahun)

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:** **27 Kabupaten/Kota Se-Jawa Barat** (18 Kabupaten Sentra Pertanian + 9 Kota Administrasi).
* **Rentang Waktu:** 6 Tahun Penuh (**2015 s.d. 2020**).
* **Frekuensi:** Tahunan (*annual aggregate*).
* **Jumlah Observasi:** 162 baris per kategori padi (27 kab/kota × 6 tahun).

---

## 3. Kamus Data Lengkap Seluruh Kolom Aktual

Ketiga berkas CSV (`produktivitas_padi_jabar.csv`, `produktivitas_padi_sawah_jabar.csv`, `produktivitas_padi_ladang_jabar.csv`) memuat 8 kolom terstruktur:

| No | Nama Kolom Aktual | Tipe Data | Satuan | Deskripsi & Interpretasi | Catatan Kritis |
| :---: | :--- | :---: | :---: | :--- | :--- |
| 1 | `id` | Integer | ID Unik | Nomor identitas baris sistem basis data Galura | Primary key sistem |
| 2 | `kode_provinsi` | Integer | Kode BPS | Kode resmi Provinsi Jawa Barat (`32`) | Standar Kemendagri / BPS |
| 3 | `nama_provinsi` | String | Teks | Nama administratif provinsi (`JAWA BARAT`) | Entitas level ADM1 |
| 4 | `kode_kabupaten_kota`| Integer | Kode BPS | Kode administratif 27 Kabupaten/Kota (e.g. `3204` Kab. Bandung) | Kunci relasi ADM2 |
| 5 | `nama_kabupaten_kota`| String | Teks | Nama resmi Kabupaten atau Kota (e.g. `KABUPATEN BANDUNG`, `KOTA BANDUNG`) | 18 Kab & 9 Kota |
| 6 | `produktivitas_padi2` / `produktivitas_padi` | Float | Kuintal / Ha | Rata-rata produktivitas padi hasil panen per hektar | **Kolom di file total bernama `produktivitas_padi2`, sedangkan di sawah & ladang bernama `produktivitas_padi`** |
| 7 | `satuan` | String | Teks | Satuan resmi pengukuran: `KUINTAL/HEKTAR` | 1 ku = 100 kg = 0.1 ton |
| 8 | `tahun` | Integer | Tahun | Tahun kalender pencatatan data (**2015 s.d. 2020**) | Rentang 6 tahun |

---

## 4. Hasil Audit Kualitas Data (Blocker B1: Artefak Seri 2019/2020)

> [!CAUTION]
> **TEMUAN ARTEFAK SERI DATA (BLOCKER B1)**: 
> Data DS03 mencatat lonjakan produktivitas rata-rata provinsi dari **55,39 ku/ha (2018)** melonjak drastis ke **68,55 ku/ha (2019)** (+23,7%), lalu anjlok kembali ke **54,22 ku/ha (2020)** (-20,9%). Lonjakan ini terjadi serentak di 27 dari 27 Kabupaten/Kota.
> 
> Investigasi membuktikan bahwa angka 2019 pada portal Galura merupakan **data Gabah Kering Panen (GKP) mentah** sebelum konversi Gabah Kering Giling (GKG). Rasio lonjakannya (≈ 1.19) identik dengan faktor susut konversi GKP ke GKG. Data riil BPS KSA mencatat produktivitas 2019 sesungguhnya stabil di 57.69 ku/ha.

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

fpath = Path("data/raw/DS03_west_java_rice_productivity/produktivitas_padi_jabar.csv")
df = pd.read_csv(fpath)

print(f"Dimensi Data Padi: {df.shape}")
print(f"Kolom Aktual: {df.columns.tolist()}")

# Rata-rata produktivitas per tahun
annual = df.groupby('tahun')['produktivitas_padi2'].agg(['count', 'mean', 'std']).reset_index()
print("\nTrayektori Produktivitas Padi Total Jabar (ku/ha):")
print(annual)
```
