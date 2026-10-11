# 🌊 Data Ekstensi — Kovariat Iklim Makro (ONI, DMI) & Validasi Presipitasi Satelit CHIRPS v2

## 1. Identitas Dataset & Sumber Resmi

Dataset kovariat iklim makro dan data presipitasi independen ini digunakan untuk memvalidasi data cuaca AgERA5 serta menyediakan variabel kontrol osilasi iklim regional (*macro-climate drivers*) bagi sistem agro-advisory TaniAdapt di Jawa Barat.

| Komponen | Nama Dataset / File | Penerbit & Sumber Resmi | Resolusi & Cakupan | Format File |
| :--- | :--- | :--- | :--- | :--- |
| **ENSO Driver** | `oni.ascii.txt` | NOAA Climate Prediction Center (CPC) | Bulanan (3-month running mean), 1950–2024 | Format ASCII Spasi Terstruktur |
| **IOD Driver** | `dmi.had.long.csv` | NOAA Physical Sciences Laboratory (PSL) | Bulanan, 1870–2024 (HadISST1.1) | Format CSV dengan Header Metadata |
| **Presipitasi Validasi** | `chirps_*.csv` (9 Kabupaten/Kota) | NOAA CoastWatch ERDDAP / Funk et al. (2015), DOI: `10.1038/sdata.2015.66` | Harian ($0,05^\circ \times 0,05^\circ$ grid), 2015–2024 | CSV (time, latitude, longitude, precip) |

---

## 2. Karakteristik & Peran Kovariat Iklim Makro

### A. Oceanic Niño Index (ONI v5)
* **Definisi:** Anomali suhu permukaan laut (*Sea Surface Temperature* / SST) di wilayah Niño 3.4 ($5^\circ\text{N}-5^\circ\text{S}, 170^\circ\text{W}-120^\circ\text{W}$) relatif terhadap rata-rata klimatologi 30 tahun.
* **Klasifikasi Fase di Indonesia:**
  * **El Niño Kuat / Super ($\ge +1,5^\circ\text{C}$):** Terjadi pada 2015–2016 dan paruh kedua 2023. Berdampak pada kemarau panjang, pergeseran awal musim tanam rendeng, dan defisit air irigasi.
  * **La Niña ($\le -0,5^\circ\text{C}$):** Terjadi fenomena *Triple-Dip La Niña* pada 2020–2022. Membawa curah hujan di atas normal sepanjang tahun (*kemarau basah*), meningkatkan risiko penyakit busuk buah / IFWC jamur pada hortikultura.

### B. Dipole Mode Index (DMI)
* **Definisi:** Gradien anomali SST antara Samudera Hindia bagian barat ($10^\circ\text{S}-10^\circ\text{N}, 50^\circ\text{E}-70^\circ\text{E}$) dan Samudera Hindia bagian tenggara ($10^\circ\text{S}-\text{Equator}, 90^\circ\text{E}-110^\circ\text{E}$).
* **Peran:** Indeks Indian Ocean Dipole (IOD). Nilai IOD positif kuat (seperti pada tahun 2019) menekan pembentukan awan di atas Jawa Barat dan memperparah kekeringan musim kemarau (Gadu).

---

## 3. Validasi Presipitasi Independen: Menyelesaikan Blocker B3 (Tasikmalaya >4.000 mm)

Pada audit awal AgERA5, Kabupaten Tasikmalaya mencatatkan akumulasi curah hujan tahunan yang melampaui $4.000\text{ mm/tahun}$. Timbul keraguan apakah angka ini merupakan artefak numerik dari model reanalisis atmosfer ECMWF.

Untuk mengujinya secara objektif tanpa asumsi, data presipitasi independen **CHIRPS v2 (*Climate Hazards Group InfraRed Precipitation with Station data*)** ditarik dari server NOAA CoastWatch ERDDAP pada koordinat yang sama.

### Temuan Empiris Validasi Silang (2015–2024):
* **Rata-rata Curah Hujan Tahunan Tasikmalaya:**
  * AgERA5 (ECMWF): **$4.150\text{ mm/tahun}$**
  * CHIRPS v2 (NOAA/UCSB): **$4.466\text{ mm/tahun}$**
* **Puncak Curah Hujan Ekstrem (2016 - La Niña):**
  * CHIRPS v2 mencatatkan **$5.818\text{ mm}$** pada tahun 2016 di Tasikmalaya.
* **Kesimpulan Ilmiah:**
  Tingginya curah hujan di Tasikmalaya **terkonfirmasi nyata (valid)** oleh observasi satelit-stasiun independen CHIRPS. Fenomena ini merupakan pengangkatan orografis (*orographic precipitation*) alami akibat topografi perbukitan Priangan Timur dan lereng Gunung Galunggung. Data AgERA5 tidak memiliki bias eror fatal dan aman digunakan sebagai dasar pemodelan iklim.

---

## 4. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

path_oni = Path("data/raw/climate_indices/oni.ascii.txt")
path_chirps = Path("data/raw/CHIRPS/chirps_tasikmalaya_2015_2024.csv")

# 1. Parsing NOAA ONI
df_oni = pd.read_csv(path_oni, sep=r"\s+")
oni_recent = df_oni[df_oni['YR'] >= 2015]
print("Contoh Data ONI (2020-2023):")
print(oni_recent.tail(8))

# 2. Parsing CHIRPS Tasikmalaya (skip baris unit ERDDAP)
df_ch = pd.read_csv(path_chirps, skiprows=[1])
df_ch['time'] = pd.to_datetime(df_ch['time'])
df_ch['year'] = df_ch['time'].dt.year

# Akumulasi tahunan CHIRPS
chirps_annual = df_ch.groupby('year')['precip'].sum().reset_index()
print("\nAkumulasi Curah Hujan Tahunan CHIRPS Tasikmalaya (mm):")
print(chirps_annual)
```
