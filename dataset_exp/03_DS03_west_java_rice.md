# 🍚 DS03 — Produktivitas Padi Jawa Barat (Distanhor)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS03_west_java_rice_productivity`
* **Penerbit / Institusi:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Provinsi Jawa Barat
* **Portal / Sumber:** Portal Resmi Galura Open Data Jabar (Satu Data Jawa Barat)
* **Endpoint API Resmi:**
  * Padi Total: `https://galura.jabarprov.go.id/api/bigdata/od_18103_produktivitas_padi_berdasarkan_kabupatenkota`
  * Padi Sawah: `https://galura.jabarprov.go.id/api/bigdata/od_18099_produktivitas_padi_sawah_berdasarkan_kabupatenkota`
  * Padi Ladang: `https://galura.jabarprov.go.id/api/bigdata/od_18102_produktivitas_padi_ladang_berdasarkan_kabupatenkota`
* **Format File Lokal:** CSV & JSON di `data/raw/DS03_west_java_rice_productivity/`
* **Ukuran Total:** ~12 KB per file (162 baris per varian, 0 missing value)

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:** **Seluruh 27 Kabupaten/Kota** di Jawa Barat (18 Kabupaten + 9 Kota).
* **Rentang Waktu:** 6 Tahun penuh (**2015 s.d. 2020**).
* **Frekuensi:** Tahunan murni (satu angka produktivitas per kabupaten per tahun kalender).
* **Satuan Ukuran:** **KUINTAL / HEKTAR** (1 Kuintal = 100 kg = 0.1 Ton).

---

## 3. Kamus Data & Struktur Kolom

Dataset memiliki struktur tabel standar Satu Data Indonesia:

| Nama Kolom | Tipe Data | Deskripsi & Nilai Contoh |
| :--- | :--- | :--- |
| `id` | Integer | ID unik record database internal. |
| `kode_provinsi` | Integer | `32` (Kode BPS/Kemendagri untuk Provinsi Jawa Barat). |
| `nama_provinsi` | String | `JAWA BARAT`. |
| `kode_kabupaten_kota` | Integer | Kode wilayah Kemendagri 4-digit (misal: `3215` untuk Karawang, `3213` untuk Subang). |
| `nama_kabupaten_kota` | String | Nama resmi wilayah (misal: `KABUPATEN KARAWANG`, `KABUPATEN SUBANG`). |
| `produktivitas_padi` | Float | Angka hasil panen riil per hektar (misal: `64.21` Ku/Ha). |
| `satuan` | String | `KUINTAL/HEKTAR`. |
| `tahun` | Integer | Tahun observasi (2015 s.d. 2020). |

---

## 4. Temuan Empiris Kunci Hasil Audit (Key Audit Findings)

### A. Tren Produktivitas Padi Flat / Stasioner di Seluruh Jawa Barat
* Berbeda dengan jagung yang mengalami kenaikan tren tajam, regresi OLS padi pada 27 kabupaten/kota menunjukkan tren yang hampir datar sempurna:
  * **Rata-rata Slope OLS:** $-0.1437\text{ ku/ha per tahun}$ (cenderung flat/stagnan).
  * **Rata-rata $R^2$:** Hanya **$0.0542$** (artinya faktor waktu/teknologi tidak mendominasi variasi padi).
  * **Rata-rata CV Residual ($9.46\%$):** Hampir sama persis dengan CV mentah ($9.72\%$), membuktikan variasi padi Jabar bersifat stasioner di sekitar rata-rata historisnya.

### B. Macro Shock Seragam Se-Provinsi (2019 vs 2020)
Analisis Year-over-Year (YoY) log-difference membuktikan adanya shock cuaca makro yang berdampak serentak ke seluruh kabupaten:
* **Tahun 2019:** **100% kabupaten/kota (27 dari 27)** mengalami lonjakan hasil positif (median kenaikan: $+21.3\%$). Ini bertepatan dengan anomali radiasi matahari tinggi pada fase pengisian bulir.
* **Tahun 2020:** **100% kabupaten/kota (27 dari 27)** serentak mengalami penurunan hasil (median penurunan: $-23.5\%$).

### C. Batasan Kritis (Critical Limitation)
* **Ketiadaan Pemisahan Musim:** Angka ini adalah agregasi 1 tahun penuh. Petani di Jawa Barat umumnya menanam padi 2 hingga 3 kali setahun (Musim Tanam 1 Rendengan saat musim hujan, dan Musim Tanam 2 Gadu saat kemarau). Menggabungkan musim rendengan dan gadu menjadi 1 angka tahunan memperhalus (*smoothes out*) respons padi terhadap anomali hujan jangka pendek.

---

## 5. Cuplikan Kode Python

```python
import pandas as pd
from pathlib import Path

csv_path = Path("data/raw/DS03_west_java_rice_productivity/produktivitas_padi_jabar.csv")
df = pd.read_csv(csv_path)

print("Dimensi Data Padi:", df.shape)
print("Kabupaten Terdaftar:", df['nama_kabupaten_kota'].nunique())
display(df[df['nama_kabupaten_kota'] == 'KABUPATEN KARAWANG'][['tahun', 'produktivitas_padi', 'satuan']])
```
