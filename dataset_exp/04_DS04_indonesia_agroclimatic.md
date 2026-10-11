# 🌧️ DS04 — Indonesia Nationwide Agroclimatic Indicators Dataset (Cross-Validation Reference)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS04_indonesia_agroclimatic`
* **Nama Resmi:** Indonesia Nationwide Agroclimatic Indicators Dataset (2016–2025)
* **Penerbit / Institusi:** Elsevier / Mendeley Data
* **DOI Terverifikasi:** `10.17632/3pfbdbzfff.1`
* **URL Resmi:** [Mendeley Data — Dataset 3pfbdbzfff](https://data.mendeley.com/datasets/3pfbdbzfff/1)
* **Lisensi:** CC BY 4.0 (Open Data)
* **Format File Lokal:** Parquet (10 file tahunan di `data/raw/DS04_indonesia_agroclimatic/`) + CSV grid points
* **Ukuran Total:** ~60 MB

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:** **612 Titik Grid Daratan Indonesia** (resolusi $0.5^\circ \times 0.5^\circ$ atau $\approx 55 \times 55\text{ km}$).
  * Daratan Jawa Barat diliput oleh 14 titik grid yang berada dalam batas spasial $106.3^\circ - 108.8^\circ\text{ BT}$ dan $-7.8^\circ - -5.9^\circ\text{ LS}$.
* **Rentang Waktu:** 10 Tahun Harian Penuh (**1 Januari 2016 s.d. 31 Desember 2025**).
* **Frekuensi:** Harian (*Daily Time-Series*).

---

## 3. Kamus Data 12 Indikator Agroklimat Terapan

Dataset ini memuat indikator agroklimat turunan (*derived indicators*):

| Nama Variabel | Definisi Agronomis | Satuan | Fungsi |
| :--- | :--- | :--- | :--- |
| `rainfall_7d` | Akumulasi curah hujan 7 hari berjalan | $mm$ | Pemantauan kebasahan tanah mingguan. |
| `rainfall_30d` | Akumulasi curah hujan 30 hari berjalan | $mm$ | Evaluasi kebutuhan air bulanan. |
| `rainfall_90d` | Akumulasi curah hujan 90 hari berjalan | $mm$ | Kecukupan air satu musim tanam penuh. |
| `rainy_days_30d` | Jumlah hari hujan ($P \ge 1.0\text{ mm}$) dalam 30 hari | Hari | Frekuensi kejadian hujan vs kekeringan. |
| `rainy_days_90d` | Jumlah hari hujan ($P \ge 1.0\text{ mm}$) dalam 90 hari | Hari | Stabilitas ketersediaan air musiman. |
| `max_daily_rainfall_30d` | Curah hujan harian tertinggi dalam 30 hari | $mm/\text{hari}$ | Indikator risiko banjir dan erosi. |
| `consecutive_dry_days` (CDD)| Hari kering berturut-turut ($P < 1.0\text{ mm}$) | Hari | Indikator cekaman kekeringan (*dry spell*). |
| `temperature_range` (DTR) | Rentang suhu harian ($T_{\max} - T_{\min}$) | $^\circ\text{C}$ | Fluktuasi radiasi & pembentukan gula/pati. |
| `rolling_temperature_mean_7d` | Rata-rata suhu 7 hari berjalan | $^\circ\text{C}$ | Akumulasi termal mingguan. |
| `cumulative_et0_30d` | Akumulasi evapotranspirasi acuan 30 hari | $mm$ | Kebutuhan air evaporatif atmosfer bulanan. |
| `water_balance` | Neraca air harian ($P - ET_0$) | $mm/\text{hari}$ | Surplus ($>0$) vs Defisit ($<0$) air harian. |
| `rolling_water_balance_30d` | Neraca air kumulatif 30 hari berjalan | $mm$ | Indikator cekaman defisit air tanaman. |

---

## 4. Pembatasan Peran di TaniAdapt & Catatan Metodologi

> [!IMPORTANT]
> **PERAN DIBATASI SEBAGAI VALIDASI SILANG (CROSS-VALIDATION)**:
> 1. **Bukan Sumber Indikator Produksi Live**: Seluruh indikator operasional (CDD, CWD, Water Balance) dalam sistem TaniAdapt **harus dihitung melalui pipeline internal sendiri**, bukan diambil dari DS04. Hal ini penting agar definisi dan formulasi matematis identik antara data historis dan data live/forecast harian.
> 2. **Perbedaan Resolusi & Sumber**: DS04 beresolusi kasar $0.5^\circ$ ($\approx 55\text{ km}$), sedangkan AgERA5 beresolusi $0.1^\circ$ ($\approx 11\text{ km}$). Formulasi $ET_0$ dan reanalisis dasar keduanya dapat memiliki deviasi lokal.
> 3. **Bukan Validasi Akurasi Independen**: Karena DS04 dan AgERA5 sama-sama bertumpu pada model reanalisis ECMWF ERA5, kesesuaian antara DS01 dan DS04 mencerminkan *internal consistency* model ECMWF, bukan validasi observasi empiris independen (validasi independen sesungguhnya menggunakan satelit-gauge CHIRPS v2).

---

## 5. Cuplikan Kode Python yang Terverifikasi

```python
import pandas as pd
from pathlib import Path

raw_dir = Path("data/raw/DS04_indonesia_agroclimatic")

# Membaca grid points dan menyaring bbox Jawa Barat (-7.8 s.d -5.9 LS, 106.3 s.d 108.8 BT)
df_grid = pd.read_csv(raw_dir / "grid_points.csv")
jabar_grid = df_grid[
    (df_grid['latitude'] >= -7.8) & (df_grid['latitude'] <= -5.9) &
    (df_grid['longitude'] >= 106.3) & (df_grid['longitude'] <= 108.8)
]
print(f"Jumlah Titik Grid DS04 di Jawa Barat: {len(jabar_grid)}")

# Membaca file parquet tahun 2024
df_2024 = pd.read_parquet(raw_dir / "agroclimate_2024.parquet")
# Filter titik Jawa Barat
df_jabar_2024 = df_2024[df_2024['grid_id'].isin(jabar_grid['grid_id'])].copy()

print(f"Dimensi Data Jabar 2024: {df_jabar_2024.shape}")
print(df_jabar_2024[['grid_id', 'date', 'precipitation_sum', 'temperature_2m_mean', 'et0_fao_evapotranspiration']].head())
```
