# 🌧️ DS04 — Indonesia Nationwide Agroclimatic Dataset

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS04_indonesia_agroclimatic`
* **Nama Resmi:** Indonesia Nationwide Agroclimatic Indicators Dataset (2016–2025)
* **Penerbit / Institusi:** Elsevier / Mendeley Data
* **DOI:** `10.17632/3pfbdbdkm3.1`
* **Lisensi:** CC BY 4.0 (Open Data)
* **Format File Lokal:** Parquet (10 file tahunan harian di `data/raw/DS04_indonesia_agroclimatic/`) + CSV definisi grid
* **Ukuran Total:** ~60 MB

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:** **612 Titik Grid Daratan Indonesia** (resolusi 0.5° $\times$ 0.5° atau sekitar $55 \times 55\text{ km}$).
  * **Titik di Jawa Barat:** Tepat **14 titik grid** melingkupi seluruh daratan Jawa Barat dari Anyer/Bogor hingga Cirebon/Pangandaran.
* **Rentang Waktu:** 10 Tahun Harian Penuh (**1 Januari 2016 s.d. 31 Desember 2025**).
* **Frekuensi:** Harian (*Daily Time-Series*).

---

## 3. Kamus Data 12 Indikator Agroklimat Terapan

Dataset ini secara khusus menghitung indikator agroklimat turunan (*derived indicators*) yang siap pakai untuk evaluasi neraca air dan kekeringan:

| Nama Variabel | Definisi Agronomis | Satuan | Ambang & Fungsi Kunci |
| :--- | :--- | :--- | :--- |
| `rainfall_7d` | Akumulasi curah hujan 7 hari berjalan | $mm$ | Pemantauan kebasahan tanah mingguan. |
| `rainfall_30d` | Akumulasi curah hujan 30 hari berjalan | $mm$ | Evaluasi kebutuhan fase vegetatif bulanan. |
| `rainfall_90d` | Akumulasi curah hujan 90 hari berjalan | $mm$ | Kecukupan air 1 musim tanam penuh. |
| `rainy_days_30d` | Jumlah hari hujan ($P \ge 1.0\text{ mm}$) dalam 30 hari | Hari | Frekuensi kejadian hujan vs kekeringan. |
| `rainy_days_90d` | Jumlah hari hujan ($P \ge 1.0\text{ mm}$) dalam 90 hari | Hari | Stabilitas ketersediaan air musiman. |
| `max_daily_rainfall_30d` | Curah hujan harian tertinggi dalam 30 hari | $mm/\text{hari}$ | **Indikator Risiko Banjir & Erosi**. |
| `consecutive_dry_days` (CDD)| Hari kering berturut-turut ($P < 1.0\text{ mm}$) | Hari | **Indikator Kunci Bahaya Kekeringan** (Dry Spell). |
| `temperature_range` (DTR) | Rentang suhu harian ($T_{\max} - T_{\min}$) | $^\circ\text{C}$ | Fluktuasi radiasi & pembentukan gula/pati. |
| `rolling_temperature_mean_7d` | Rata-rata suhu 7 hari berjalan | $^\circ\text{C}$ | Akumulasi termal mingguan. |
| `cumulative_et0_30d` | Akumulasi evapotranspirasi acuan 30 hari | $mm$ | Kebutuhan air evaporatif atmosfer bulanan. |
| `water_balance` | Neraca air harian ($P - ET_0$) | $mm/\text{hari}$ | Surplus ($>0$) vs Defisit ($<0$) air harian. |
| `rolling_water_balance_30d` | Neraca air kumulatif 30 hari berjalan | $mm$ | **Indikator Cekaman Air Tanaman** (Water Deficit Index). |

---

## 4. Status Audit Kualitas & Peran di TaniAdapt

### A. Konsistensi Internal dengan AgERA5 (DS01)
* Karena DS04 dan DS01 sama-sama diturunkan dari model reanalisis ECMWF ERA5, korelasi antar-dataset pada titik-titik Jawa Barat mencapai $r > 0.88$ untuk suhu dan $r > 0.79$ untuk presipitasi bulanan.
* Ini membuktikan **konsistensi internal reanalisis ECMWF**, bukan validasi stasiun lapangan independen.

### B. Nilai Tambah di TaniAdapt
* **Deteksi Cekaman Kekeringan Otomatis:** Variabel `consecutive_dry_days` (CDD) dan `rolling_water_balance_30d` memungkinkan Decision Engine langsung mendeteksi kapan fase vegetatif jagung atau padi kekurangan air tanpa perlu menghitung ulang rumus FAO-56 secara manual.

---

## 5. Cuplikan Kode Python

```python
import pandas as pd
from pathlib import Path

raw_dir = Path("data/raw/DS04_indonesia_agroclimatic")
# Membaca grid points Jawa Barat
df_grid = pd.read_csv(raw_dir / "grid_points.csv")
jabar_grid = df_grid[df_grid['province_name'].str.contains('Jawa Barat', case=False, na=False)]
print("Jumlah Grid Points di Jawa Barat:", len(jabar_grid))

# Membaca 1 file parquet tahun 2024
df_2024 = pd.read_parquet(raw_dir / "agroclimate_2024.parquet")
print("Dimensi Data 2024:", df_2024.shape)
display(df_2024[['grid_id', 'date', 'rainfall_30d', 'consecutive_dry_days', 'water_balance']].head())
```
