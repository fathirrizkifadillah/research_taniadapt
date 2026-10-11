# 🌤️ DS01 — AgERA5 Agrometeorological Indicators Time-Series (2015–2024)

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

> [!NOTE]
> **Catatan Centroid Geometris & Sel Grid AgERA5**: Titik koordinat yang digunakan adalah centroid geometris poligon ADM2 dari database geoBoundaries. Sebagaimana didokumentasikan pada audit spasial M2, kabupaten agraris luas seperti Sukabumi (36 sel grid) dan Cianjur (30 sel grid) mencakup variasi mikroklimat pesisir hingga pegunungan.

---

## 3. Kamus Data & Variabel Agrometeorologi (24 Parameter)

Setiap file CSV memuat kolom waktu `valid_time` (format `YYYY-MM-DD`) dan 23 variabel agroklimat.

> [!IMPORTANT]
> **Koreksi Satuan Presipitasi**: Kolom `Precipitation_Flux` pada berkas CSV hasil unduhan CDS API **SUDAH DALAM SATUAN mm/hari** (akumulasi harian). Tidak boleh dikalikan 86.400.

| Nama Kolom Aktual di CSV | Variabel Cuaca | Satuan Asli | Konversi Agronomis | Fungsi di TaniAdapt |
| :--- | :--- | :--- | :--- | :--- |
| `valid_time` | Tanggal Kalender | Tanggal | `YYYY-MM-DD` | Kunci pencocokan deret waktu. |
| `Temperature_Air_2m_Mean_24h` | Suhu Udara Rata-rata 24 Jam | Kelvin ($K$) | Kurangi $273.15 \rightarrow ^\circ\text{C}$ | Perhitungan Growing Degree Days (GDD). |
| `Temperature_Air_2m_Min_24h` | Suhu Udara Minimum 24 Jam | Kelvin ($K$) | Kurangi $273.15 \rightarrow ^\circ\text{C}$ | Deteksi chilling & depresiasi titik embun malam. |
| `Temperature_Air_2m_Max_24h` | Suhu Udara Maksimum 24 Jam | Kelvin ($K$) | Kurangi $273.15 \rightarrow ^\circ\text{C}$ | Pemantauan cekaman panas saat anthesis. |
| `Precipitation_Flux` | Curah Hujan Harian | $\text{mm/hari}$ | Natively $\text{mm/hari}$ | Akumulasi hujan, jadwal tanam, deteksi banjir. |
| `Solar_Radiation_Flux` | Radiasi Matahari Harian | $J/m^2$ | Bagi $10^6 \rightarrow MJ/m^2/\text{hari}$ | Akumulasi radiasi fotosintesis (PAR). |
| `Vapour_Pressure_Mean_24h` | Tekanan Uap Rata-rata | $hPa$ | Bagi $10 \rightarrow kPa$ | Transpirasi dan kelembaban atmosfer. |
| `Dew_Point_Temperature_2m_Mean_24h` | Suhu Titik Embun 2m | Kelvin ($K$) | Kurangi $273.15 \rightarrow ^\circ\text{C}$ | Menghitung depresiasi titik embun ($T_{\min} - T_d$). |
| `Derived_Relative_Humidity_2m_Max_24h` | Kelembaban Relatif Maksimum | Persen ($\%$) | $0 - 100\%$ | Indikator kebasahan malam & spora jamur. |
| `Derived_Relative_Humidity_2m_Min_24h` | Kelembaban Relatif Minimum | Persen ($\%$) | $0 - 100\%$ | Kelembaban siang hari / evaporasi. |
| `Vapour_Pressure_Deficit_at_Maximum_Temperature` | VPD pada Suhu Maksimum | $hPa$ | Bagi $10 \rightarrow kPa$ | Cekaman kekeringan atmosfer dan stomata daun. |
| `ReferenceET_PenmanMonteith_FAO56` | Evapotranspirasi Acuan FAO-56 | $mm/\text{hari}$ | $mm/\text{hari}$ | Kebutuhan air tanaman & neraca irigasi. |
| `Wind_Speed_10m_Mean_24h` | Kecepatan Angin Rata-rata | $m/s$ | $m/s$ | Evaporasi dan risiko rebah batang. |

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
if not fpath.exists():
    fpath = Path("data/raw/DS01_agera5/agera5_bandung_2015_2024.csv")

df = pd.read_csv(fpath)
df['valid_time'] = pd.to_datetime(df['valid_time'])

# Konversi Suhu ke Celcius
df['tmean_c'] = df['Temperature_Air_2m_Mean_24h'] - 273.15
df['tmin_c'] = df['Temperature_Air_2m_Min_24h'] - 273.15
df['tmax_c'] = df['Temperature_Air_2m_Max_24h'] - 273.15

# Hitung Depresiasi Titik Embun Malam (Proksi Kebasahan Daun / Penyakit)
df['dew_point_c'] = df['Dew_Point_Temperature_2m_Mean_24h'] - 273.15
df['night_dew_depression'] = df['tmin_c'] - df['dew_point_c']

# Curah hujan sudah dalam mm/hari
df['rain_mm'] = df['Precipitation_Flux']

print(df[['valid_time', 'tmean_c', 'rain_mm', 'night_dew_depression']].head())
```
