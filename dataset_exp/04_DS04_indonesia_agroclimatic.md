# 🌧️ DS04 — Indonesia Nationwide Agroclimatic Indicators Dataset (Cross-Validation Reference)

## 1. Identitas Dataset & Sumber Resmi
* **Dataset Identifier:** `DS04_indonesia_agroclimatic`
* **Nama Resmi:** Indonesia Nationwide Agroclimatic Indicators Dataset (2016–2025)
* **Penerbit / Institusi:** Elsevier / Mendeley Data
* **DOI Terverifikasi:** `10.17632/3pfbdbzfff.1`
* **URL Resmi:** [Mendeley Data — Dataset 3pfbdbzfff](https://data.mendeley.com/datasets/3pfbdbzfff/1)
* **Lisensi:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Format File Lokal:** Parquet (10 file tahunan di `data/raw/DS04_indonesia_agroclimatic/`) + CSV grid points
* **Ukuran Total:** ~60 MB (612 titik grid daratan Indonesia $	imes$ 3.653 hari)

---

## 2. Cakupan Spasial & Resolusi Waktu
* **Cakupan Spasial:** **612 Titik Grid Daratan Indonesia** (resolusi grid $0.5^\circ 	imes 0.5^\circ$ atau $pprox 55 	imes 55	ext{ km}$).
  * Daratan Jawa Barat diliput oleh **14 titik grid** yang berada dalam batas spasial $106.3^\circ - 108.8^\circ	ext{ BT}$ dan $-7.8^\circ - -5.9^\circ	ext{ LS}$.
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
| 5 | `temperature_2m_mean` | Float | $^\circ	ext{C}$ | Suhu udara rata-rata 24 jam |
| 6 | `temperature_2m_max` | Float | $^\circ	ext{C}$ | Suhu udara maksimum harian |
| 7 | `temperature_2m_min` | Float | $^\circ	ext{C}$ | Suhu udara minimum harian |
| 8 | `precipitation_sum` | Float | $mm/	ext{hari}$ | Akumulasi curah hujan harian |
| 9 | `relative_humidity_2m_mean` | Float | Persen ($\%$) | Kelembapan relatif rata-rata harian |
| 10 | `et0_fao_evapotranspiration` | Float | $mm/	ext{hari}$ | Evapotranspirasi acuan Penman-Monteith FAO-56 harian |
| 11 | `qc_range_flag` | Integer | $0 / 1$ | Flag kontrol kualitas fisik ($0 = 	ext{Lolos}, 1 = 	ext{Anomali}$) |
| 12 | `rainfall_7d` | Float | $mm$ | Akumulasi curah hujan 7 hari berjalan (kebasahan tanah mingguan) |
| 13 | `rainfall_30d` | Float | $mm$ | Akumulasi curah hujan 30 hari berjalan (kecukupan air bulanan) |
| 14 | `rainfall_90d` | Float | $mm$ | Akumulasi curah hujan 90 hari berjalan (kebutuhan 1 musim tanam) |
| 15 | `rainy_days_30d` | Integer | Hari | Frekuensi hari hujan ($P \ge 1.0	ext{ mm}$) dalam jendela 30 hari |
| 16 | `rainy_days_90d` | Integer | Hari | Frekuensi hari hujan ($P \ge 1.0	ext{ mm}$) dalam jendela 90 hari |
| 17 | `max_daily_rainfall_30d` | Float | $mm/	ext{hari}$ | Puncak hujan harian tertinggi dalam 30 hari (risiko banjir/erosi) |
| 18 | `consecutive_dry_days` (CDD)| Integer | Hari | Hari kering berturut-turut ($P < 1.0	ext{ mm}$, cekaman kekeringan) |
| 19 | `temperature_range` (DTR) | Float | $^\circ	ext{C}$ | Rentang suhu harian ($T_{\max} - T_{\min}$) |
| 20 | `rolling_temperature_mean_7d` | Float | $^\circ	ext{C}$ | Rata-rata suhu 7 hari berjalan |
| 21 | `cumulative_et0_30d` | Float | $mm$ | Akumulasi evapotranspirasi acuan 30 hari berjalan |
| 22 | `water_balance` | Float | $mm/	ext{hari}$ | Neraca air harian ($P - ET_0$, surplus $>0$ vs defisit $<0$) |
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
