# 🌾 DS02 — Bangladesh Rice Panel Dataset (Metodologi Replikasi)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS02_bangladesh_rice_panel`
* **Nama Resmi:** Replication Data for: Growing season climate and rice yield in Bangladesh (2015–2024 Audited Panel)
* **Penerbit / Institusi:** Bangladesh Rice Research Institute (BRRI) / Mendeley Data
* **DOI Terverifikasi:** `10.17632/h94z4ftts2.1`
* **URL Resmi:** [Mendeley Data — Dataset h94z4ftts2](https://data.mendeley.com/datasets/h94z4ftts2/1)
* **Lisensi:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Format File Lokal:** CSV hasil ekstraksi arsip ZIP resmi (`data/raw/DS02_bangladesh_rice_panel/extracted/.../Rice_Yield_2015_2024_Audited.csv`)
* **Ukuran Total:** ~2.1 MB (1.728 baris panel seimbang: 64 distrik × 3 musim × 9 tahun)

---

## 2. Cakupan Spasial, Musim Tanam, & Resolusi Waktu
* **Cakupan Spasial:** 64 Distrik di seluruh Bangladesh (setara tingkat Kabupaten/ADM2).
* **Rentang Waktu:** 9 Tahun Kalender Tanam Penuh (**2015-16 s.d. 2023-24**).
* **Tiga Musim Tanam Padi Tropis:**
  1. **Aus**: Musim tanam hujan awal / pra-muson (April s.d. Juli).
  2. **Aman**: Musim tanam muson utama / rendeng (Juli s.d. November/Desember).
  3. **Boro**: Musim tanam kemarau beririgasi intensif (Desember s.d. Mei).

---

## 3. Kamus Data Lengkap Seluruh 36 Kolom Mentah `Rice_Yield_2015_2024_Audited.csv`

File data memuat 36 kolom yang terbagi menjadi 3 kelompok fungsional:

### A. Variabel Pokok Agronomi & Wilayah (Kolom 1–13)
| No | Nama Kolom | Tipe Data | Satuan | Deskripsi & Interpretasi |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `district_id` | Integer | ID Angka | Nomor urut unik distrik (1 s.d. 64) |
| 2 | `adm2_code` | String | Kode ISO | Kode geospasial ADM2 resmi distrik |
| 3 | `district` | String | Teks | Nama resmi distrik (e.g. Gazipur, Mymensingh, Bogura) |
| 4 | `district_bbs` | String | Teks | Nama distrik menurut standar Biro Statistik Bangladesh (BBS) |
| 5 | `district_climate` | String | Teks | Stasiun meteorologi rujukan terdekat untuk distrik tersebut |
| 6 | `crop_id` | Integer | ID Angka | Kode numerik musim tanam (1 = Aus, 2 = Aman, 3 = Boro) |
| 7 | `crop` | String | Kategori | Nama musim tanam (`Aus`, `Aman`, `Boro`) |
| 8 | `crop_year` | String | Teks | Periode tahun kalender tanam (e.g. `2015-16`, `2023-24`) |
| 9 | `year_start` | Integer | Tahun | Tahun awal siklus tanam (e.g. `2015`) |
| 10 | `year_end` | Integer | Tahun | Tahun akhir / panen siklus tanam (e.g. `2016`) |
| 11 | `area_ha` | Float | Hektar | Luas panen riil setelah audit |
| 12 | `yield_t_ha` | Float | Ton / Hektar | Produktivitas hasil panen padi riil (1 t/ha = 10 ku/ha) |
| 13 | `production_mt` | Float | Metrik Ton | Total volume produksi fisik panen padi |

### B. Validasi Matematika & Jejak Sumber Audit (Kolom 14–26)
| No | Nama Kolom | Tipe Data | Satuan | Deskripsi & Interpretasi |
| :---: | :--- | :---: | :---: | :--- |
| 14 | `yield_calc_t_ha` | Float | Ton / Hektar | Hasil hitung ulang identitas: `production_mt / area_ha` |
| 15 | `yield_abs_diff` | Float | Ton / Hektar | Selisih absolut: `|yield_t_ha - yield_calc_t_ha|` |
| 16 | `yield_rel_diff_pct`| Float | Persen (%) | Persentase diskrepansi matematis pelaporan |
| 17 | `area_ha_raw` | Float | Hektar | Angka luas panen mentah sebelum verifikasi dokumen sumber |
| 18 | `yield_t_ha_raw` | Float | Ton / Hektar | Angka produktivitas mentah sebelum audit |
| 19 | `production_mt_raw`| Float | Metrik Ton | Angka produksi mentah sebelum audit |
| 20 | `verified_source_correction` | Boolean | True/False | Apakah baris ini mengalami koreksi sumber resmi |
| 21 | `correction_note` | String | Teks | Catatan detail perbaikan data |
| 22 | `correction_source`| String | Teks | Dokumen resmi rujukan koreksi (BBS Yearbook) |
| 23 | `correction_url` | String | URL | Tautan digital berkas verifikasi |
| 24 | `source_page` | String | Halaman | Nomor halaman dokumen sumber cetak |
| 25 | `source_document` | String | Teks | Nama file dokumen publikasi resmi BBS |
| 26 | `source_url` | String | URL | Tautan unduhan publikasi resmi BBS |

### C. Indikator Pertumbuhan YoY & Flags Audit Kualitas (Kolom 27–36)
| No | Nama Kolom | Tipe Data | Satuan | Deskripsi & Arti Nilai |
| :---: | :--- | :---: | :---: | :--- |
| 27 | `area_ha_yoy_pct` | Float | Persen (%) | Pertumbuhan luas panen YoY. **Bernilai `NaN` pada musim 2015-16** karena merupakan musim awal (*base year*) tanpa lag t-1. |
| 28 | `yield_t_ha_yoy_pct`| Float | Persen (%) | Pertumbuhan produktivitas YoY. **Bernilai `NaN` pada musim 2015-16** karena tidak ada lag t-1. |
| 29 | `production_mt_yoy_pct`| Float| Persen (%) | Pertumbuhan produksi fisik YoY. **Bernilai `NaN` pada musim 2015-16** karena tidak ada lag t-1. |
| 30 | `flag_yield_math` | Integer | 0 / 1 | **Audit Identitas**: 0 = Lolos uji matematis (konsisten). 1 = Diskrepansi > 1%. |
| 31 | `flag_area_yoy_50` | Integer | 0 / 1 | **Audit Luas**: 0 = Normal. 1 = Lonjakan luas panen > 50% YoY. |
| 32 | `flag_yield_yoy_25` | Integer | 0 / 1 | **Audit Yield**: 0 = Normal. 1 = Lonjakan hasil panen > 25% YoY. |
| 33 | `flag_prod_yoy_50` | Integer | 0 / 1 | **Audit Produksi**: 0 = Normal. 1 = Lonjakan volume produksi > 50% YoY. |
| 34 | `flag_neighbor_spike`| Integer | 0 / 1 | **Audit Spasial**: 0 = Normal. 1 = Anomali relatif terhadap distrik tetangga. |
| 35 | `flag_any_review` | Integer | 0 / 1 | **Bendera Agregat**: 0 = **Lolos Seluruh Audit (Data Bersih)**. 1 = Butuh review. |
| 36 | `review_reason` | String | Teks | Catatan alasan anomali jika flag = 1. **Bernilai `NaN` jika data bersih (flag = 0)**. |

> [!NOTE]
> **Kenapa di baris-baris awal terlihat nilai `NaN` dan `0`?**
> 1. `NaN` pada persentase YoY terjadi karena tahun awal panel (2015-16) secara alami tidak memiliki data pembanding tahun sebelumnya (t-1).
> 2. Angka `0` pada seluruh kolom `flag_*` menandakan bahwa data tersebut **100% LOLOS AUDIT (BERSIH)**, tidak memiliki kesalahan kalkulasi atau lonjakan mencurigakan.
> 3. `NaN` pada `review_reason` berarti data tersebut valid sehingga tidak memerlukan catatan koreksi.

---

## 4. Status Audit Metodologi & Batasan Peran di TaniAdapt

> [!IMPORTANT]
> **BUKAN DATASET KEPUTUSAN JAWA BARAT**: Dataset ini tidak merepresentasikan petani di Jawa Barat. Perannya dalam proyek TaniAdapt adalah sebagai **demonstrasi metodologis replikasi** atas arsitektur regresi panel ber-resolusi musim (*Season-Specific Panel Fixed Effects Regression*).

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

csv_path = Path("data/raw/DS02_bangladesh_rice_panel/extracted/Growing_Season_Climate_Rice_Bangladesh_Replication/Rice_Yield_2015_2024_Audited.csv")
df = pd.read_csv(csv_path)

print(f"Dimensi Data Padi Bangladesh: {df.shape}")
print(f"Musim Tanam Tersedia: {df['crop'].unique().tolist()}")
print(f"Total Distrik: {df['district'].nunique()}")
print(f"Tingkat Kelulusan Audit Identitas Matematika: {(df['flag_yield_math'] == 0).mean()*100:.1f}%")
```
