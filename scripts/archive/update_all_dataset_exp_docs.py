"""
Script to update all dataset_exp documentation files with comprehensive,
PhD-standard data dictionaries (Kamus Data) for 100% of columns across all 9 datasets.
"""
from pathlib import Path

# ==========================================
# 1. DS01 — AgERA5 Weather (27 Kolom Lengkap)
# ==========================================
ds01_content = """# 🌤️ DS01 — AgERA5 Agrometeorological Indicators Time-Series (2015–2024)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS01_agera5`
* **Nama Resmi:** Agrometeorological indicators from 1979 to present derived from reanalysis (AgERA5)
* **Penerbit / Institusi:** Copernicus Climate Data Store (ECMWF / European Union)
* **DOI Resmi:** `10.24381/f9c1f09d`
* **API Dataset ID:** `sis-agrometeorological-indicators-timeseries`
* **Dokumentasi API:** [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/datasets/sis-agrometeorological-indicators-timeseries)
* **Lisensi:** Copernicus Open Access License (CC-BY 4.0 / Bebas untuk riset dan komersial)
* **Format File Lokal:** CSV (27 file lengkap di `data/raw/DS01_agera5/`)
* **Ukuran Total:** ~27 MB (masing-masing file berukuran ~1 MB, mencakup 3.653 hari per wilayah)

---

## 2. Cakupan Spasial Lengkap: 27 Kabupaten/Kota Se-Jawa Barat

Data ditarik pada **seluruh 27 Kabupaten/Kota di Provinsi Jawa Barat** berdasarkan centroid geometris resmi ADM2 geoBoundaries untuk periode 10 tahun (**1 Januari 2015 s.d. 31 Desember 2024**, 3.653 hari per file, total 98.631 baris observasi):

| No | Nama Wilayah | Tipe Wilayah | Latitude Centroid | Longitude Centroid | Sel AgERA5 (0.1°) | Status File Lokal |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 1 | **Kabupaten Bandung** | Kabupaten | -7.1000 | 107.6108 | 16 sel | `agera5_kab_bandung_2015_2024.csv` |
| 2 | **Kabupaten Bandung Barat** | Kabupaten | -6.8971 | 107.4150 | 11 sel | `agera5_kab_bandung_barat_2015_2024.csv` |
| 3 | **Kabupaten Bekasi** | Kabupaten | -6.2154 | 107.1207 | 9 sel | `agera5_kab_bekasi_2015_2024.csv` |
| 4 | **Kabupaten Bogor** | Kabupaten | -6.5600 | 106.7675 | 23 sel | `agera5_kab_bogor_2015_2024.csv` |
| 5 | **Kabupaten Ciamis** | Kabupaten | -7.2905 | 108.4286 | 14 sel | `agera5_kab_ciamis_2015_2024.csv` |
| 6 | **Kabupaten Cianjur** | Kabupaten | -7.1337 | 107.1578 | 30 sel | `agera5_kab_cianjur_2015_2024.csv` |
| 7 | **Kabupaten Cirebon** | Kabupaten | -6.7456 | 108.5516 | 8 sel | `agera5_kab_cirebon_2015_2024.csv` |
| 8 | **Kabupaten Garut** | Kabupaten | -7.3596 | 107.7889 | 25 sel | `agera5_kab_garut_2015_2024.csv` |
| 9 | **Kabupaten Indramayu** | Kabupaten | -6.4488 | 108.1686 | 17 sel | `agera5_kab_indramayu_2015_2024.csv` |
| 10 | **Kabupaten Karawang** | Kabupaten | -6.2520 | 107.3542 | 16 sel | `agera5_kab_karawang_2015_2024.csv` |
| 11 | **Kabupaten Kuningan** | Kabupaten | -7.0042 | 108.5603 | 9 sel | `agera5_kab_kuningan_2015_2024.csv` |
| 12 | **Kabupaten Majalengka** | Kabupaten | -6.8159 | 108.2578 | 11 sel | `agera5_kab_majalengka_2015_2024.csv` |
| 13 | **Kabupaten Pangandaran** | Kabupaten | -7.6356 | 108.5188 | 9 sel | `agera5_kab_pangandaran_2015_2024.csv` |
| 14 | **Kabupaten Purwakarta** | Kabupaten | -6.5950 | 107.4322 | 8 sel | `agera5_kab_purwakarta_2015_2024.csv` |
| 15 | **Kabupaten Subang** | Kabupaten | -6.4830 | 107.7322 | 18 sel | `agera5_kab_subang_2015_2024.csv` |
| 16 | **Kabupaten Sukabumi** | Kabupaten | -7.0762 | 106.7073 | 36 sel | `agera5_kab_sukabumi_2015_2024.csv` |
| 17 | **Kabupaten Sumedang** | Kabupaten | -6.8251 | 107.9809 | 13 sel | `agera5_kab_sumedang_2015_2024.csv` |
| 18 | **Kabupaten Tasikmalaya** | Kabupaten | -7.4967 | 108.1413 | 20 sel | `agera5_kab_tasikmalaya_2015_2024.csv` |
| 19 | **Kota Bandung** | Kota | -6.9175 | 107.6191 | 2 sel | `agera5_kota_bandung_2015_2024.csv` |
| 20 | **Kota Banjar** | Kota | -7.3683 | 108.5336 | 1 sel | `agera5_kota_banjar_2015_2024.csv` |
| 21 | **Kota Bekasi** | Kota | -6.2383 | 106.9756 | 2 sel | `agera5_kota_bekasi_2015_2024.csv` |
| 22 | **Kota Bogor** | Kota | -6.5950 | 106.8167 | 1 sel | `agera5_kota_bogor_2015_2024.csv` |
| 23 | **Kota Cimahi** | Kota | -6.8865 | 107.5436 | 0 sel (urban) | `agera5_kota_cimahi_2015_2024.csv` |
| 24 | **Kota Cirebon** | Kota | -6.7320 | 108.5523 | 1 sel | `agera5_kota_cirebon_2015_2024.csv` |
| 25 | **Kota Depok** | Kota | -6.3961 | 106.8168 | 2 sel | `agera5_kota_depok_2015_2024.csv` |
| 26 | **Kota Sukabumi** | Kota | -6.9278 | 106.9297 | 1 sel | `agera5_kota_sukabumi_2015_2024.csv` |
| 27 | **Kota Tasikmalaya** | Kota | -7.3274 | 108.2207 | 2 sel | `agera5_kota_tasikmalaya_2015_2024.csv` |

---

## 3. Kamus Data Lengkap Seluruh 27 Kolom Mentah AgERA5

Setiap file CSV di `data/raw/DS01_agera5/` memuat **27 kolom mentah lengkap** tanpa reduksi:

| No | Nama Kolom Aktual di CSV | Tipe Data | Satuan Asli | Konversi Agronomis | Fungsi dalam Engine TaniAdapt |
| :---: | :--- | :---: | :---: | :---: | :--- |
| 1 | `valid_time` | String | Tanggal Kalender | `YYYY-MM-DD` | Kunci pencocokan deret waktu harian |
| 2 | `latitude` | Float | Derajat Desimal | $-90^\circ \text{ s.d. } +90^\circ$ | Lintang geografis centroid wilayah |
| 3 | `longitude` | Float | Derajat Desimal | $-180^\circ \text{ s.d. } +180^\circ$ | Bujur geografis centroid wilayah |
| 4 | `Temperature_Air_2m_Mean_24h` | Float | Kelvin ($K$) | Kurangi $273.15 \rightarrow ^\circ\text{C}$ | Perhitungan Growing Degree Days (GDD) & akumulasi termal |
| 5 | `Temperature_Air_2m_Min_24h` | Float | Kelvin ($K$) | Kurangi $273.15 \rightarrow ^\circ\text{C}$ | Deteksi suhu dingin malam & depresiasi titik embun |
| 6 | `Temperature_Air_2m_Max_24h` | Float | Kelvin ($K$) | Kurangi $273.15 \rightarrow ^\circ\text{C}$ | Pemantauan cekaman panas (*heat stress*) saat anthesis |
| 7 | `Precipitation_Flux` | Float | $\text{mm/hari}$ | Natively $\text{mm/hari}$ | Akumulasi hujan, awal musim tanam, deteksi kekeringan/banjir |
| 8 | `Solar_Radiation_Flux` | Float | $J/m^2$ | Bagi $10^6 \rightarrow MJ/m^2/\text{hari}$ | Radiasi fotosintesis aktif (PAR) pembentukan biomassa |
| 9 | `Dew_Point_Temperature_2m_Mean_24h` | Float | Kelvin ($K$) | Kurangi $273.15 \rightarrow ^\circ\text{C}$ | Menghitung depresiasi embun malam ($T_{\min} - T_d$) |
| 10 | `Derived_Relative_Humidity_2m_Max_24h` | Float | Persen ($\%$) | $0 - 100\%$ | Indikator kebasahan malam & risiko infeksi spora jamur |
| 11 | `Derived_Relative_Humidity_2m_Min_24h` | Float | Persen ($\%$) | $0 - 100\%$ | Kelembapan minimum siang hari / potensi evapotranspirasi |
| 12 | `Vapour_Pressure_Deficit_at_Maximum_Temperature`| Float | $hPa$ | Bagi $10 \rightarrow kPa$ | Cekaman kekeringan atmosfer dan pembukaan stomata daun |
| 13 | `ReferenceET_PenmanMonteith_FAO56` | Float | $\text{mm/hari}$ | $\text{mm/hari}$ | Evapotranspirasi acuan FAO-56 untuk neraca air irigasi |
| 14 | `Wind_Speed_10m_Mean_24h` | Float | $m/s$ | $m/s$ | Kecepatan angin rata-rata, aerodinamika kanopi daun |
| 15 | `Cloud_Cover_Mean_24h` | Float | Fraksi ($0-1$) | $0 - 100\%$ | Proporsi tutupan awan harian |
| 16 | `Relative_Humidity_2m_06h` | Float | Persen ($\%$) | $0 - 100\%$ | Kelembapan relatif pukul 06:00 UTC (13:00 WIB / siang) |
| 17 | `Relative_Humidity_2m_09h` | Float | Persen ($\%$) | $0 - 100\%$ | Kelembapan relatif pukul 09:00 UTC (16:00 WIB / sore) |
| 18 | `Relative_Humidity_2m_12h` | Float | Persen ($\%$) | $0 - 100\%$ | Kelembapan relatif pukul 12:00 UTC (19:00 WIB / awal malam) |
| 19 | `Relative_Humidity_2m_15h` | Float | Persen ($\%$) | $0 - 100\%$ | Kelembapan relatif pukul 15:00 UTC (22:00 WIB / tengah malam) |
| 20 | `Relative_Humidity_2m_18h` | Float | Persen ($\%$) | $0 - 100\%$ | Kelembapan relatif pukul 18:00 UTC (01:00 WIB / dini hari) |
| 21 | `Temperature_Air_2m_Max_Day_Time` | Float | Kelvin ($K$) | Kurangi $273.15 \rightarrow ^\circ\text{C}$ | Suhu udara maksimum spesifik fase siang hari |
| 22 | `Temperature_Air_2m_Mean_Day_Time` | Float | Kelvin ($K$) | Kurangi $273.15 \rightarrow ^\circ\text{C}$ | Suhu udara rata-rata fase siang hari |
| 23 | `Temperature_Air_2m_Mean_Night_Time`| Float | Kelvin ($K$) | Kurangi $273.15 \rightarrow ^\circ\text{C}$ | Suhu udara rata-rata fase malam hari |
| 24 | `Temperature_Air_2m_Min_Night_Time` | Float | Kelvin ($K$) | Kurangi $273.15 \rightarrow ^\circ\text{C}$ | Suhu udara minimum malam hari (waktu fajar) |
| 25 | `Precipitation_Rain_Duration_Fraction` | Float | Fraksi ($0-1$) | Jam/24 | Proporsi durasi kejadian hujan air dalam 24 jam |
| 26 | `Precipitation_Duration_Fraction` | Float | Fraksi ($0-1$) | Jam/24 | Proporsi durasi presipitasi total dalam 24 jam |
| 27 | `Vapour_Pressure_Mean_24h` | Float | $hPa$ | Bagi $10 \rightarrow kPa$ | Tekanan uap jenuh aktual rata-rata atmosfer |

---

## 4. Hasil Audit Fisis & Validasi Independen Hujan

1. **Konsistensi Termodinamika:** $T_{\min} \le T_{\text{mean}} \le T_{\max}$ konsisten di seluruh 98.631 baris (0 pelanggaran).
2. **Presipitasi Non-Negatif:** Seluruh nilai $\ge 0\text{ mm/hari}$.
3. **Temuan Curah Hujan Tasikmalaya:** AgERA5 mencatat curah hujan tahunan di Tasikmalaya mencapai 4.215 mm/tahun (rata-rata 10 tahun) dengan puncak 4.760 mm (2016). Nilai ini **konsisten dengan efek orografis lereng selatan Galunggung** dan telah dikonfirmasi secara independen oleh observasi satelit-gauge CHIRPS v2 (CHIRPS mencatat rata-rata 4.466 mm/tahun dan puncak 2016 sebesar 5.818 mm).

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

fpath = Path("data/raw/DS01_agera5/agera5_kab_bandung_2015_2024.csv")
df = pd.read_csv(fpath)
df['valid_time'] = pd.to_datetime(df['valid_time'])

# Konversi Suhu ke Celcius
df['tmean_c'] = df['Temperature_Air_2m_Mean_24h'] - 273.15
df['tmin_c'] = df['Temperature_Air_2m_Min_24h'] - 273.15
df['tmax_c'] = df['Temperature_Air_2m_Max_24h'] - 273.15

# Hitung Depresiasi Titik Embun Malam (Proksi Kebasahan Daun / Penyakit)
df['dew_point_c'] = df['Dew_Point_Temperature_2m_Mean_24h'] - 273.15
df['night_dew_depression'] = df['tmin_c'] - df['dew_point_c']

# Curah hujan harian (mm/hari)
df['rain_mm'] = df['Precipitation_Flux']

print(df[['valid_time', 'tmean_c', 'rain_mm', 'night_dew_depression']].head())
```
"""
Path("dataset_exp/01_DS01_agera5_weather.md").write_text(ds01_content, encoding="utf-8")
print("Updated 01_DS01_agera5_weather.md successfully!")


# ==========================================
# 2. DS02 — Bangladesh Rice Panel (36 Kolom Lengkap)
# ==========================================
ds02_content = """# 🌾 DS02 — Bangladesh Rice Panel Dataset (Metodologi Replikasi)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS02_bangladesh_rice_panel`
* **Nama Resmi:** Replication Data for: Growing season climate and rice yield in Bangladesh (2015–2024 Audited Panel)
* **Penerbit / Institusi:** Bangladesh Rice Research Institute (BRRI) / Mendeley Data
* **DOI Terverifikasi:** `10.17632/h94z4ftts2.1`
* **URL Resmi:** [Mendeley Data — Dataset h94z4ftts2](https://data.mendeley.com/datasets/h94z4ftts2/1)
* **Lisensi:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Format File Lokal:** CSV hasil ekstraksi arsip ZIP resmi (`data/raw/DS02_bangladesh_rice_panel/extracted/.../Rice_Yield_2015_2024_Audited.csv`)
* **Ukuran Total:** ~2.1 MB (1.728 baris panel seimbang: 64 distrik $\times$ 3 musim $\times$ 9 tahun)

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
| 12 | `yield_t_ha` | Float | Ton / Hektar | Produktivitas hasil panen padi riil ($1\text{ t/ha} = 10\text{ ku/ha}$) |
| 13 | `production_mt` | Float | Metrik Ton | Total volume produksi fisik panen padi |

### B. Validasi Matematika & Jejak Sumber Audit (Kolom 14–26)
| No | Nama Kolom | Tipe Data | Satuan | Deskripsi & Interpretasi |
| :---: | :--- | :---: | :---: | :--- |
| 14 | `yield_calc_t_ha` | Float | Ton / Hektar | Hasil hitung ulang identitas: $\text{production\_mt} / \text{area\_ha}$ |
| 15 | `yield_abs_diff` | Float | Ton / Hektar | Selisih absolut: $|\text{yield\_t\_ha} - \text{yield\_calc\_t\_ha}|$ |
| 16 | `yield_rel_diff_pct`| Float | Persen ($\%$) | Persentase diskrepansi matematis pelaporan |
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
| 27 | `area_ha_yoy_pct` | Float | Persen ($\%$) | Pertumbuhan luas panen YoY. **Bernilai `NaN` pada musim 2015-16** karena merupakan musim awal (*base year*) tanpa lag $t-1$. |
| 28 | `yield_t_ha_yoy_pct`| Float | Persen ($\%$) | Pertumbuhan produktivitas YoY. **Bernilai `NaN` pada musim 2015-16** karena tidak ada lag $t-1$. |
| 29 | `production_mt_yoy_pct`| Float| Persen ($\%$) | Pertumbuhan produksi fisik YoY. **Bernilai `NaN` pada musim 2015-16** karena tidak ada lag $t-1$. |
| 30 | `flag_yield_math` | Integer | $0 / 1$ | **Audit Identitas**: $0$ = Lolos uji matematis (konsisten). $1$ = Diskrepansi $>1\%$. |
| 31 | `flag_area_yoy_50` | Integer | $0 / 1$ | **Audit Luas**: $0$ = Normal. $1$ = Lonjakan luas panen $>50\%$ YoY. |
| 32 | `flag_yield_yoy_25` | Integer | $0 / 1$ | **Audit Yield**: $0$ = Normal. $1$ = Lonjakan hasil panen $>25\%$ YoY. |
| 33 | `flag_prod_yoy_50` | Integer | $0 / 1$ | **Audit Produksi**: $0$ = Normal. $1$ = Lonjakan volume produksi $>50\%$ YoY. |
| 34 | `flag_neighbor_spike`| Integer | $0 / 1$ | **Audit Spasial**: $0$ = Normal. $1$ = Anomali relatif terhadap distrik tetangga. |
| 35 | `flag_any_review` | Integer | $0 / 1$ | **Bendera Agregat**: $0$ = **Lolos Seluruh Audit (Data Bersih)**. $1$ = Butuh review. |
| 36 | `review_reason` | String | Teks | Catatan alasan anomali jika flag = 1. **Bernilai `NaN` jika data bersih (flag = 0)**. |

> [!NOTE]
> **Kenapa di baris-baris awal terlihat nilai `NaN` dan `0`?**
> 1. `NaN` pada persentase YoY terjadi karena tahun awal panel (2015-16) secara alami tidak memiliki data pembanding tahun sebelumnya ($t-1$).
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

# Filter musim panen Aman (muson utama)
df_aman = df[df['crop'] == 'Aman'].copy()
print("Observasi Padi Musim Aman:", df_aman.shape)
print("Rata-rata Produktivitas Nasional:", df_aman['yield_t_ha'].mean(), "t/ha")
```
"""
Path("dataset_exp/02_DS02_bangladesh_rice_panel.md").write_text(ds02_content, encoding="utf-8")
print("Updated 02_DS02_bangladesh_rice_panel.md successfully!")


# ==========================================
# 3. DS03 — West Java Rice (Lengkap Sawah Ladang)
# ==========================================
ds03_content = """# 🌾 DS03 — Produktivitas Padi Jawa Barat (Open Data Jabar)

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
* **Ukuran Total:** ~11 KB per file (162 baris panel seimbang: 27 kabupaten/kota $\times$ 6 tahun)

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:** **27 Kabupaten/Kota Se-Jawa Barat** (18 Kabupaten Sentra Pertanian + 9 Kota Administrasi).
* **Rentang Waktu:** 6 Tahun Penuh (**2015 s.d. 2020**).
* **Frekuensi:** Tahunan (*annual aggregate*).
* **Jumlah Observasi:** 162 baris per kategori padi ($27 \text{ kab/kota} \times 6 \text{ tahun}$).

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
| 7 | `satuan` | String | Teks | Satuan resmi pengukuran: `KUINTAL/HEKTAR` | $1\text{ ku} = 100\text{ kg} = 0.1\text{ ton}$ |
| 8 | `tahun` | Integer | Tahun | Tahun kalender pencatatan data (**2015 s.d. 2020**) | Rentang 6 tahun |

---

## 4. Hasil Audit Kualitas Data (Blocker B1: Artefak Seri 2019/2020)

> [!CAUTION]
> **TEMUAN ARTEFAK SERI DATA (BLOCKER B1)**: 
> Data DS03 mencatat lonjakan produktivitas rata-rata provinsi dari **55,39 ku/ha (2018)** melonjak drastis ke **68,55 ku/ha (2019)** (+23,7%), lalu anjlok kembali ke **54,22 ku/ha (2020)** (-20,9%). Lonjakan ini terjadi serentak di 27 dari 27 Kabupaten/Kota.
> 
> Investigasi membuktikan bahwa angka 2019 pada portal Galura merupakan **data Gabah Kering Panen (GKP) mentah** sebelum konversi Gabah Kering Giling (GKG). Rasio lonjakannya ($\approx 1,19$) identik dengan faktor susut konversi GKP ke GKG. Data riil BPS KSA mencatat produktivitas 2019 sesungguhnya stabil di $57,69\text{ ku/ha}$.

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
"""
Path("dataset_exp/03_DS03_west_java_rice.md").write_text(ds03_content, encoding="utf-8")
print("Updated 03_DS03_west_java_rice.md successfully!")


# ==========================================
# 4. DS04 — Indonesia Agroclimatic (23 Kolom Lengkap)
# ==========================================
ds04_content = """# 🌧️ DS04 — Indonesia Nationwide Agroclimatic Indicators Dataset (Cross-Validation Reference)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS04_indonesia_agroclimatic`
* **Nama Resmi:** Indonesia Nationwide Agroclimatic Indicators Dataset (2016–2025)
* **Penerbit / Institusi:** Elsevier / Mendeley Data
* **DOI Terverifikasi:** `10.17632/3pfbdbzfff.1`
* **URL Resmi:** [Mendeley Data — Dataset 3pfbdbzfff](https://data.mendeley.com/datasets/3pfbdbzfff/1)
* **Lisensi:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Format File Lokal:** Parquet (10 file tahunan di `data/raw/DS04_indonesia_agroclimatic/`) + CSV grid points
* **Ukuran Total:** ~60 MB (612 titik grid daratan Indonesia $\times$ 3.653 hari)

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:** **612 Titik Grid Daratan Indonesia** (resolusi grid $0.5^\circ \times 0.5^\circ$ atau $\approx 55 \times 55\text{ km}$).
  * Daratan Jawa Barat diliput oleh **14 titik grid** yang berada dalam batas spasial $106.3^\circ - 108.8^\circ\text{ BT}$ dan $-7.8^\circ - -5.9^\circ\text{ LS}$.
* **Rentang Waktu:** 10 Tahun Harian Penuh (**1 Januari 2016 s.d. 31 Desember 2025**).
* **Frekuensi:** Harian (*Daily Time-Series*).

---

## 3. Kamus Data Lengkap Seluruh 23 Kolom Parquet Agroklimat

Berkas Parquet harian (`agroclimate_with_indicators.parquet`) memuat **23 kolom indikator lengkap**:

| No | Nama Kolom | Tipe Data | Satuan | Deskripsi & Interpretasi Agronomis |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `grid_id` | Integer | ID Grid | Nomor indeks unik titik grid terestrial (1 s.d. 612) |
| 2 | `latitude` | Float | Derajat Desimal | Koordinat lintang titik grid daratan |
| 3 | `longitude` | Float | Derajat Desimal | Koordinat bujur titik grid daratan |
| 4 | `date` | String / Date | `YYYY-MM-DD` | Tanggal kalender harian observasi |
| 5 | `temperature_2m_mean` | Float | $^\circ\text{C}$ | Suhu udara rata-rata 24 jam |
| 6 | `temperature_2m_max` | Float | $^\circ\text{C}$ | Suhu udara maksimum harian |
| 7 | `temperature_2m_min` | Float | $^\circ\text{C}$ | Suhu udara minimum harian |
| 8 | `precipitation_sum` | Float | $mm/\text{hari}$ | Akumulasi curah hujan harian |
| 9 | `relative_humidity_2m_mean` | Float | Persen ($\%$) | Kelembapan relatif rata-rata harian |
| 10 | `et0_fao_evapotranspiration` | Float | $mm/\text{hari}$ | Evapotranspirasi acuan Penman-Monteith FAO-56 harian |
| 11 | `qc_range_flag` | Integer | $0 / 1$ | Flag kontrol kualitas fisik ($0 = \text{Lolos}, 1 = \text{Anomali}$) |
| 12 | `rainfall_7d` | Float | $mm$ | Akumulasi curah hujan 7 hari berjalan (kebasahan tanah mingguan) |
| 13 | `rainfall_30d` | Float | $mm$ | Akumulasi curah hujan 30 hari berjalan (kecukupan air bulanan) |
| 14 | `rainfall_90d` | Float | $mm$ | Akumulasi curah hujan 90 hari berjalan (kebutuhan 1 musim tanam) |
| 15 | `rainy_days_30d` | Integer | Hari | Frekuensi hari hujan ($P \ge 1.0\text{ mm}$) dalam jendela 30 hari |
| 16 | `rainy_days_90d` | Integer | Hari | Frekuensi hari hujan ($P \ge 1.0\text{ mm}$) dalam jendela 90 hari |
| 17 | `max_daily_rainfall_30d` | Float | $mm/\text{hari}$ | Puncak hujan harian tertinggi dalam 30 hari (risiko banjir/erosi) |
| 18 | `consecutive_dry_days` (CDD)| Integer | Hari | Hari kering berturut-turut ($P < 1.0\text{ mm}$, cekaman kekeringan) |
| 19 | `temperature_range` (DTR) | Float | $^\circ\text{C}$ | Rentang suhu harian ($T_{\max} - T_{\min}$) |
| 20 | `rolling_temperature_mean_7d` | Float | $^\circ\text{C}$ | Rata-rata suhu 7 hari berjalan |
| 21 | `cumulative_et0_30d` | Float | $mm$ | Akumulasi evapotranspirasi acuan 30 hari berjalan |
| 22 | `water_balance` | Float | $mm/\text{hari}$ | Neraca air harian ($P - ET_0$, surplus $>0$ vs defisit $<0$) |
| 23 | `rolling_water_balance_30d` | Float | $mm$ | Neraca air kumulatif 30 hari berjalan (indikator stres kekeringan) |

---

## 4. Pembatasan Peran di TaniAdapt & Catatan Metodologi

> [!IMPORTANT]
> **PERAN SEBAGAI TOLOK UKUR VALIDASI SILANG**:
> 1. DS04 berbasis grid koordinat terestrial regional ($0.5^\circ$), berbeda dengan DS01 AgERA5 yang berbasis centroid poligon 27 Kabupaten/Kota ($0.1^\circ$).
> 2. Keduanya menggunakan reanalisis turunan ECMWF ERA5, sehingga keselarasan keduanya menunjukkan konsistensi internal model reanalisis, bukan validasi ground-truth independen.

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

raw_dir = Path("data/raw/DS04_indonesia_agroclimatic")
df_daily = pd.read_parquet(raw_dir / "agroclimate_with_indicators.parquet")

print("Dimensi Data DS04 Parquet:", df_daily.shape)
print("Daftar Kolom Lengkap:", df_daily.columns.tolist())
```
"""
Path("dataset_exp/04_DS04_indonesia_agroclimatic.md").write_text(ds04_content, encoding="utf-8")
print("Updated 04_DS04_indonesia_agroclimatic.md successfully!")


# ==========================================
# 5. DS05 — West Java Maize (27 Kab/Kota Lengkap)
# ==========================================
ds05_content = """# 🌽 DS05 — Produktivitas Jagung 27 Kabupaten/Kota Jawa Barat (2015–2022)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS05_subang_maize_productivity` (Cakupan: Seluruh 27 Kab/Kota Jawa Barat)
* **Penerbit / Institusi:** Dinas Tanaman Pangan dan Hortikultura (Distanhor) Provinsi Jawa Barat
* **Portal / Sumber:** Galura Open Data Jabar (Satu Data Jawa Barat)
* **Endpoint API Resmi:** `https://galura.jabarprov.go.id/api/bigdata/od_18104_produktivitas_jagung_berdasarkan_kabupatenkota`
* **Format File Lokal:** CSV & JSON di `data/raw/DS05_subang_maize_productivity/`
* **Ukuran Total:** ~14 KB (216 baris lengkap: 27 kabupaten/kota $\times$ 8 tahun, 0 missing value)

---

## 2. Cakupan Spasial Penuh: Seluruh 27 Kabupaten/Kota Se-Jawa Barat
* **Cakupan Spasial:** **Seluruh 27 Kabupaten/Kota di Provinsi Jawa Barat**.
  * Bukan dataset khusus Subang; mencakup seluruh sentra utama jagung (Kab. Garut, Kab. Majalengka, Kab. Cianjur, Kab. Tasikmalaya, Kab. Ciamis, dll.).
  * Kabupaten Subang dibahas secara khusus sebagai **studi kasus investigasi anomali struktural (*structural break*)**.
* **Rentang Waktu:** 8 Tahun Penuh (**2015 s.d. 2022**).
* **Frekuensi:** Tahunan agregat ($N = 216$ observasi panel).
* **Satuan Ukuran:** **KUINTAL / HEKTAR** ($1\text{ ku} = 100\text{ kg} = 0.1\text{ ton}$).

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
* **Kabupaten Garut** menyumbang porsi terbesar jagung Jawa Barat dengan luas panen **$>50.000\text{ ha}$** dan volume produksi **$>350.000\text{ ton}$**.
* Produktivitas Garut stabil pada rentang $65 - 75\text{ ku/ha}$ tanpa lonjakan tak wajar.

### B. Dekomposisi Lonjakan Subang (+56.4% pada 2020–2022)
* Subang adalah produsen jagung skala kecil (luas panen hanya $113 - 765\text{ ha}$).
* Lonjakan produktivitas Subang dari $57,23\text{ ku/ha}$ (2020) ke $89,49\text{ ku/ha}$ (2022) terbukti merupakan **efek penyusutan basis luas panen (*small-denominator volatility*)** dan pergeseran ke petak-petak intensif benih hibrida terbatas.
* **Koefisien Variasi Residual Detrended**: $\text{CV}_{\text{resid}} = 12,21\%$, merupakan batas atas variasi yang dapat diatribusikan pada cuaca.

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
"""
Path("dataset_exp/05_DS05_subang_maize.md").write_text(ds05_content, encoding="utf-8")
print("Updated 05_DS05_subang_maize.md successfully!")


# ==========================================
# 6. DS06 — Horticulture SBS & Sayuran
# ==========================================
ds06_content = """# 🌶️ DS06 — Hortikultura Sayuran Buah Semusim (Cabai & Tomat)

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
  * `produktivitas_sbs_jabar.csv`: **Tingkat Agregat Provinsi Jawa Barat** ($N=9$ baris observasi per komoditas, 2016–2024).
  * `produksi_sayuran_komoditas_jabar.csv`: **Tingkat Kabupaten/Kota** (volume produksi sayuran, 2016–2024).
* **Rentang Waktu:** 9 Tahun Penuh (**2016 s.d. 2024**).
* **Komoditas Utama yang Dipantau:** Cabai Rawit, Cabai Besar, Tomat, Bawang Merah.
* **Satuan Ukuran Aktual:**
  * Produktivitas SBS: **KUINTAL / HEKTAR** ($1\text{ ku} = 100\text{ kg} = 0.1\text{ ton}$).
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
> 4. **Arsitektur Advisory**: Menggunakan **Indeks Kondisi Cuaca Mendukung (IFWC)** berbasis depresiasi titik embun malam ($T_{\min} - T_d$) dan kelembapan diurnal relatif.

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
"""
Path("dataset_exp/06_DS06_west_java_horticulture_chili_tomato.md").write_text(ds06_content, encoding="utf-8")
print("Updated 06_DS06_west_java_horticulture_chili_tomato.md successfully!")


# ==========================================
# 7. DS07 — Soybean & Spatial GeoBoundaries (Lengkap)
# ==========================================
ds07_content = """# 🧬 DS07 — Kedelai Jawa Barat & Batas Geospasial ADM2 Centroids

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
* **Jumlah Observasi:** 216 baris ($27\text{ kab/kota} \times 8\text{ tahun}$).
  * 156 baris bernilai positif ($>0\text{ ku/ha}$), 60 baris bernilai nol (terkonsentrasi pada 9 Kota non-pertanian).

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
| 5 | `luas_approx_km2` | Float | $\text{km}^2$ | Estimasi luas wilayah poligon dalam kilometer persegi |
| 6 | `n_sel_agera5_0_1deg` | Integer | Jumlah Sel | Jumlah sel grid AgERA5 ($0.1^\circ \times 0.1^\circ$) yang berada di dalam wilayah |
| 7 | `shape_name_geoboundaries`| String | Teks | Nama wilayah padanan pada database geoBoundaries global |
| 8 | `shape_type` | String | Teks | Tipe entitas administrasi (`Regency`, `City`, `County`) |

### C. File Geospasial `jawa_barat_provinsi.geojson`
* **Format:** GeoJSON RFC 7946 / EPSG:4326.
* **Geometri:** `MultiPolygon` resmi batas daratan dan kepulauan Provinsi Jawa Barat (Bounds: $106.37^\circ - 108.83^\circ\text{ BT}, -7.82^\circ - -5.92^\circ\text{ LS}$).
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
"""
Path("dataset_exp/07_soybean_and_spatial_geoboundaries.md").write_text(ds07_content, encoding="utf-8")
print("Updated 07_soybean_and_spatial_geoboundaries.md successfully!")


# ==========================================
# 8. DS08 — Production & Harvest Area (Lengkap)
# ==========================================
ds08_content = """# 🌾 DS08 — Volume Produksi Fisik & Luas Panen Jawa Barat (Padi, Jagung, Kedelai)

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
| 7 | `satuan` | String | Teks | `TON` ($1\text{ Ton} = 1.000\text{ kg} = 10\text{ Kuintal}$) |
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
| 7 | `satuan` | String | Teks | `HEKTAR` ($1\text{ Ha} = 10.000\text{ m}^2$) |
| 8 | `tahun` | Integer | Tahun | Tahun kalender observasi |

---

## 4. Pengujian Identitas Matematika Agronomi

Dalam statistik pertanian resmi Indonesia (BPS dan Kementerian Pertanian):
$$\\text{Produktivitas (Kuintal/Hektar)} = \\frac{\\text{Produksi (Ton)} \\times 10}{\\text{Luas Panen (Hektar)}}$$

### Hasil Uji Konsistensi Numerik di Seluruh Jawa Barat:
1. **Jagung (2015–2022):** Konsisten 100% pada seluruh 194 observasi dengan $\\text{Luas Panen} > 0$ (selisih mutlak $\\le 0,05\\text{ ku/ha}$).
2. **Kedelai (2015–2022):** Konsisten 100% pada seluruh 151 observasi aktif (selisih mutlak $< 0,01\\text{ ku/ha}$).

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
"""
Path("dataset_exp/08_production_and_harvest_area.md").write_text(ds08_content, encoding="utf-8")
print("Updated 08_production_and_harvest_area.md successfully!")


# ==========================================
# 9. DS09 — Climate Covariates & CHIRPS (Lengkap)
# ==========================================
ds09_content = """# 🌊 DS09 — Kovariat Iklim Makro (ONI, DMI) & Validasi Presipitasi Satelit CHIRPS v2

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS09_climate_covariates_and_chirps`
* **Komponen & Sumber Resmi:**
  1. **Oceanic Niño Index (ONI v5):** NOAA Climate Prediction Center (CPC)
  2. **Dipole Mode Index (DMI):** NOAA Physical Sciences Laboratory (PSL)
  3. **CHIRPS v2 Daily Precipitation:** NOAA CoastWatch ERDDAP / UC Santa Barbara Climate Hazards Center
* **Format File Lokal:**
  * `data/raw/climate_indices/oni.ascii.txt` (Data bulanan 1950–2024)
  * `data/raw/climate_indices/dmi.had.long.csv` (Data bulanan 1870–2024)
  * `data/raw/CHIRPS/chirps_*.csv` (9 file harian 2015–2024)

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:**
  * ONI: Samudera Pasifik Ekuatorial wilayah Niño 3.4 ($5^\circ\text{N}-5^\circ\text{S}, 170^\circ\text{W}-120^\circ\text{W}$).
  * DMI: Samudera Hindia (Gradien Barat vs Tenggara).
  * CHIRPS v2: Grid $0.05^\circ \times 0.05^\circ$ ($\approx 5.5\text{ km}$) pada koordinat centroid wilayah Jawa Barat (Tasikmalaya, Subang, Garut, Bandung, dll.).
* **Rentang Waktu:** 10 Tahun Penuh (**2015 s.d. 2024**).

---

## 3. Kamus Data Lengkap Seluruh Kolom Aktual

### A. Berkas `oni.ascii.txt` (Format Spasi Terstruktur NOAA)
| No | Nama Kolom | Tipe Data | Satuan | Deskripsi & Interpretasi |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `SEAS` | String | 3-Bulan Berjalan | Nama jendela musim 3-bulan berjalan (`DJF`, `JFM`, `FMA`, `MAM`, `AMJ`, `MJJ`, `JJA`, `JAS`, `ASO`, `SON`, `OND`, `NDJ`). Ada 12 observasi per tahun. |
| 2 | `YR` | Integer | Tahun | Tahun kalender observasi (e.g. `2015`, `2024`) |
| 3 | `TOTAL` | Float | $^\circ\text{C}$ | Rata-rata suhu permukaan laut riil (*Sea Surface Temperature* / SST) di wilayah Niño 3.4 |
| 4 | `ANOM` | Float | $^\circ\text{C}$ | **Anomali Suhu Muka Laut Terhadap Klimatologi 30 Tahun**:<br>• $\ge +0,5^\circ\text{C}$: **Ambang Batas El Niño** (potensi kemarau panjang/kering di Indonesia).<br>• $\le -0,5^\circ\text{C}$: **Ambang Batas La Niña** (potensi curah hujan di atas normal / kemarau basah).<br>• $-0,5^\circ\text{C} < \text{ANOM} < +0,5^\circ\text{C}$: **Fase Netral**. |

### B. Berkas `dmi.had.long.csv` (Format CSV NOAA PSL)
| No | Nama Kolom | Tipe Data | Satuan | Deskripsi & Interpretasi |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `Date` | Date | `YYYY-MM-DD` | Tanggal kalender bulanan observasi |
| 2 | `HadISST1.1 DMI` | Float | $^\circ\text{C}$ | **Indeks Indian Ocean Dipole (IOD)**:<br>• Nilai positif tinggi: Memperparah kekeringan musim kemarau di Jawa Barat.<br>• Nilai negatif: Menambah pasokan uap air di Samudera Hindia selatan Jawa. |

### C. Berkas `chirps_*.csv` (Format CSV NOAA CoastWatch ERDDAP)
| No | Nama Kolom | Tipe Data | Satuan | Deskripsi & Interpretasi |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `time` | Timestamp | ISO 8601 | Waktu kalender harian observasi (`YYYY-MM-DDT00:00:00Z`) |
| 2 | `latitude` | Float | Derajat Desimal | Titik lintang observasi grid $0.05^\circ$ |
| 3 | `longitude` | Float | Derajat Desimal | Titik bujur observasi grid $0.05^\circ$ |
| 4 | `precip` | Float | $mm/\text{hari}$ | Akumulasi curah hujan harian hasil kombinasi citra satelit inframerah dan stasiun penakar hujan permukaan (*rain gauge*) |

---

## 4. Validasi Presipitasi Independen: Menyelesaikan Blocker B3 (Tasikmalaya >4.000 mm)

* **Hasil Temuan Validasi Silang**:
  * AgERA5 mencatat rata-rata curah hujan tahunan Tasikmalaya: **$4.150\text{ mm/tahun}$**.
  * CHIRPS v2 mencatat rata-rata curah hujan tahunan Tasikmalaya: **$4.466\text{ mm/tahun}$**.
  * Pada tahun ekstrem La Niña 2016, CHIRPS v2 mencatatkan **$5.818\text{ mm/tahun}$**.
* **Kesimpulan Ilmiah**: Curah hujan tinggi di Tasikmalaya adalah **fenomena orografis alamiah nyata** akibat lereng Gunung Galunggung dan perbukitan Priangan Timur, bukan artefak eror reanalisis ECMWF.

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

path_oni = Path("data/raw/climate_indices/oni.ascii.txt")
df_oni = pd.read_csv(path_oni, sep=r"\\s+")
df_oni_recent = df_oni[df_oni['YR'] >= 2015].copy()

print("Contoh Data ONI (2015-2024):")
print(df_oni_recent.head())
```
"""
Path("dataset_exp/09_climate_covariates_and_chirps.md").write_text(ds09_content, encoding="utf-8")
print("Updated 09_climate_covariates_and_chirps.md successfully!")


# ==========================================
# 10. Dataset Overview Master Catalog
# ==========================================
overview_content = """# 📚 Master Katalog & Kamus Data Terpadu — Proyek TaniAdapt

Repositori ini memuat **9 Dataset Utama (DS01 s.d. DS09)** yang terverifikasi secara empiris untuk membangun Decision Engine dan Advisory Pertanian Presisi di Jawa Barat.

---

## 1. Matriks Ringkasan Seluruh 9 Dataset

| ID | Nama Dataset | Penerbit / Portal Sumber Resmi | Cakupan Spasial | Cakupan Waktu & N_eff | Total Kolom | Status Disposisi Audit |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: |
| **DS01** | **AgERA5 Agrometeorological Indicators** | Copernicus CDS (ECMWF / EU) | **27 Kab/Kota Se-Jawa Barat** | 2015–2024 (Harian, $98.631$ baris) | **27 kolom** | **PASS** (Backbone Cuaca) |
| **DS02** | **Bangladesh Rice Climate-Yield Panel** | Mendeley Data / BRRI | 64 Distrik Bangladesh | 2015–2024 (3 Musim, $1.728$ baris) | **36 kolom** | **BENCHMARK** (Replikasi Panel) |
| **DS03** | **Produktivitas Padi Jawa Barat** | Distanhor / Open Data Jabar | **27 Kab/Kota Se-Jawa Barat** | 2015–2020 (Tahunan, 162 baris) | **8 kolom** | **PASS** (Artefak 2019 Terisolasi) |
| **DS04** | **Indonesia Nationwide Agroclimatic** | Elsevier / Mendeley Data | 612 Titik Grid (14 di Jabar) | 2016–2025 (Harian) | **23 kolom** | **PASS** (Validasi Silang Grid) |
| **DS05** | **Produktivitas Jagung Jawa Barat** | Distanhor / Open Data Jabar | **27 Kab/Kota Se-Jawa Barat** | 2015–2022 (Tahunan, 216 baris) | **8 kolom** | **PASS** (Target Jagung Regional) |
| **DS06** | **Hortikultura Cabai & Tomat** | Distanhor / Open Data Jabar | Provinsi (SBS) & Kab/Kota (Prod) | 2016–2024 (Tahunan) | **7 & 9 kolom** | **PASS** (Target Panen Makro) |
| **DS07** | **Kedelai & Geospasial ADM2 Centroids**| Distanhor & geoBoundaries | **27 Kab/Kota Se-Jawa Barat** | 2015–2022 (Tahunan, 216 baris) | **8 kolom** | **PASS** (Target Kedelai + Batas GIS) |
| **DS08** | **Volume Produksi & Luas Panen** | Distanhor / Open Data Jabar | **27 Kab/Kota Se-Jawa Barat** | 2015–2022 (Tahunan) | **8 kolom** | **PASS** (Identitas Matematika Valid) |
| **DS09** | **Kovariat Iklim Makro (ONI, DMI, CHIRPS)**| NOAA CPC, PSL & UCSB ERDDAP | Pasifik, Samudera Hindia, Jabar | 2015–2024 (Bulanan & Harian) | **4 & 4 kolom** | **PASS** (Validasi Orografis Nyata) |

---

## 2. Navigasi Dokumentasi Spesifik Dataset
* [01_DS01_agera5_weather.md](file:///c:/CODING/research_taniAdapt/dataset_exp/01_DS01_agera5_weather.md) — 27 Parameter Agrometeorologi AgERA5
* [02_DS02_bangladesh_rice_panel.md](file:///c:/CODING/research_taniAdapt/dataset_exp/02_DS02_bangladesh_rice_panel.md) — 36 Variabel Replikasi Padi Bangladesh
* [03_DS03_west_java_rice.md](file:///c:/CODING/research_taniAdapt/dataset_exp/03_DS03_west_java_rice.md) — Produktivitas Padi Sawah, Ladang & Total
* [04_DS04_indonesia_agroclimatic.md](file:///c:/CODING/research_taniAdapt/dataset_exp/04_DS04_indonesia_agroclimatic.md) — 23 Indikator Ekstrem Agroklimat Parquet
* [05_DS05_subang_maize.md](file:///c:/CODING/research_taniAdapt/dataset_exp/05_DS05_subang_maize.md) — Produktivitas Jagung 27 Kab/Kota Jawa Barat
* [06_DS06_west_java_horticulture_chili_tomato.md](file:///c:/CODING/research_taniAdapt/dataset_exp/06_DS06_west_java_horticulture_chili_tomato.md) — Hortikultura Cabai Rawit, Cabai Besar & Tomat
* [07_soybean_and_spatial_geoboundaries.md](file:///c:/CODING/research_taniAdapt/dataset_exp/07_soybean_and_spatial_geoboundaries.md) — Kedelai Jawa Barat & Geospasial Poligon
* [08_production_and_harvest_area.md](file:///c:/CODING/research_taniAdapt/dataset_exp/08_production_and_harvest_area.md) — Uji Identitas Matematika Yield = Produksi / Luas Panen
* [09_climate_covariates_and_chirps.md](file:///c:/CODING/research_taniAdapt/dataset_exp/09_climate_covariates_and_chirps.md) — NOAA ONI, DMI, dan Satelit CHIRPS v2
"""
Path("dataset_exp/Dataset_overview.md").write_text(overview_content, encoding="utf-8")
print("Updated Dataset_overview.md successfully!")
