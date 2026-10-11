# 🌊 DS09 — Kovariat Iklim Makro (ONI, DMI) & Validasi Presipitasi Satelit CHIRPS v2

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
  * ONI: Samudera Pasifik Ekuatorial wilayah Niño 3.4 ($5^\circ	ext{N}-5^\circ	ext{S}, 170^\circ	ext{W}-120^\circ	ext{W}$).
  * DMI: Samudera Hindia (Gradien Barat vs Tenggara).
  * CHIRPS v2: Grid $0.05^\circ 	imes 0.05^\circ$ ($pprox 5.5	ext{ km}$) pada koordinat centroid wilayah Jawa Barat (Tasikmalaya, Subang, Garut, Bandung, dll.).
* **Rentang Waktu:** 10 Tahun Penuh (**2015 s.d. 2024**).

---

## 3. Kamus Data Lengkap Seluruh Kolom Aktual

### A. Berkas `oni.ascii.txt` (Format Spasi Terstruktur NOAA)
| No | Nama Kolom | Tipe Data | Satuan | Deskripsi & Interpretasi |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `SEAS` | String | 3-Bulan Berjalan | Nama jendela musim 3-bulan berjalan (`DJF`, `JFM`, `FMA`, `MAM`, `AMJ`, `MJJ`, `JJA`, `JAS`, `ASO`, `SON`, `OND`, `NDJ`). Ada 12 observasi per tahun. |
| 2 | `YR` | Integer | Tahun | Tahun kalender observasi (e.g. `2015`, `2024`) |
| 3 | `TOTAL` | Float | $^\circ	ext{C}$ | Rata-rata suhu permukaan laut riil (*Sea Surface Temperature* / SST) di wilayah Niño 3.4 |
| 4 | `ANOM` | Float | $^\circ	ext{C}$ | **Anomali Suhu Muka Laut Terhadap Klimatologi 30 Tahun**:<br>• $\ge +0,5^\circ	ext{C}$: **Ambang Batas El Niño** (potensi kemarau panjang/kering di Indonesia).<br>• $\le -0,5^\circ	ext{C}$: **Ambang Batas La Niña** (potensi curah hujan di atas normal / kemarau basah).<br>• $-0,5^\circ	ext{C} < 	ext{ANOM} < +0,5^\circ	ext{C}$: **Fase Netral**. |

### B. Berkas `dmi.had.long.csv` (Format CSV NOAA PSL)
| No | Nama Kolom | Tipe Data | Satuan | Deskripsi & Interpretasi |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `Date` | Date | `YYYY-MM-DD` | Tanggal kalender bulanan observasi |
| 2 | `HadISST1.1 DMI` | Float | $^\circ	ext{C}$ | **Indeks Indian Ocean Dipole (IOD)**:<br>• Nilai positif tinggi: Memperparah kekeringan musim kemarau di Jawa Barat.<br>• Nilai negatif: Menambah pasokan uap air di Samudera Hindia selatan Jawa. |

### C. Berkas `chirps_*.csv` (Format CSV NOAA CoastWatch ERDDAP)
| No | Nama Kolom | Tipe Data | Satuan | Deskripsi & Interpretasi |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `time` | Timestamp | ISO 8601 | Waktu kalender harian observasi (`YYYY-MM-DDT00:00:00Z`) |
| 2 | `latitude` | Float | Derajat Desimal | Titik lintang observasi grid $0.05^\circ$ |
| 3 | `longitude` | Float | Derajat Desimal | Titik bujur observasi grid $0.05^\circ$ |
| 4 | `precip` | Float | $mm/	ext{hari}$ | Akumulasi curah hujan harian hasil kombinasi citra satelit inframerah dan stasiun penakar hujan permukaan (*rain gauge*) |

---

## 4. Validasi Presipitasi Independen: Menyelesaikan Blocker B3 (Tasikmalaya >4.000 mm)

* **Hasil Temuan Validasi Silang**:
  * AgERA5 mencatat rata-rata curah hujan tahunan Tasikmalaya: **$4.150	ext{ mm/tahun}$**.
  * CHIRPS v2 mencatat rata-rata curah hujan tahunan Tasikmalaya: **$4.466	ext{ mm/tahun}$**.
  * Pada tahun ekstrem La Niña 2016, CHIRPS v2 mencatatkan **$5.818	ext{ mm/tahun}$**.
* **Kesimpulan Ilmiah**: Curah hujan tinggi di Tasikmalaya adalah **fenomena orografis alamiah nyata** akibat lereng Gunung Galunggung dan perbukitan Priangan Timur, bukan artefak eror reanalisis ECMWF.

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

path_oni = Path("data/raw/climate_indices/oni.ascii.txt")
df_oni = pd.read_csv(path_oni, sep=r"\s+")
df_oni_recent = df_oni[df_oni['YR'] >= 2015].copy()

print("Contoh Data ONI (2015-2024):")
print(df_oni_recent.head())
```
