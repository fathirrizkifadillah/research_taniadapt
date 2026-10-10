import pandas as pd
import numpy as np

# Baca DS01 Bandung: lat -6.91, lon 107.61
df_ds01_bdg = pd.read_csv("data/raw/DS01_agera5/agera5_bandung_2015_2024.csv")
df_ds01_bdg['date'] = pd.to_datetime(df_ds01_bdg['valid_time']).dt.strftime('%Y-%m-%d')

# Baca DS04 Parquet with indicators
df_ds04 = pd.read_parquet("data/raw/DS04_indonesia_agroclimatic/agroclimate_with_indicators.parquet")
print("Kolom DS04:", df_ds04.columns.tolist()[:15])

# Cari grid terdekat ke Bandung (-6.91, 107.61) di DS04
# Grid DS04 kelipatan 0.5: misal lat -7.0, lon 107.5
df_ds04_bdg = df_ds04[(df_ds04['latitude'] == -7.0) & (df_ds04['longitude'] == 107.5)].copy()
print(f"Jumlah baris DS04 grid (-7.0, 107.5): {len(df_ds04_bdg)}")
df_ds04_bdg['date'] = pd.to_datetime(df_ds04_bdg['date']).dt.strftime('%Y-%m-%d')

merged = pd.merge(df_ds01_bdg, df_ds04_bdg, on='date', suffixes=('_ds01', '_ds04'))
print(f"Jumlah tanggal beririsan Bandung: {len(merged)}")

if not merged.empty:
    # Cek korelasi hujan
    p_ds01 = merged['Precipitation_Flux']
    # Cari nama kolom hujan di DS04
    p_col_ds04 = [c for c in df_ds04.columns if 'precip' in c.lower() or 'rain' in c.lower()]
    print("Kolom hujan DS04:", p_col_ds04)
    if 'precipitation_sum' in merged.columns:
        p_ds04 = merged['precipitation_sum']
        corr_p = p_ds01.corr(p_ds04)
        bias_p = np.mean(p_ds01 - p_ds04)
        print(f"Korelasi Harian Presipitasi DS01 vs DS04: {corr_p:.3f}")
        print(f"Bias Rata-rata Harian Presipitasi (DS01 - DS04): {bias_p:.3f} mm/hari")
    
    # Cek korelasi suhu
    t_ds01 = merged['Temperature_Air_2m_Mean_24h'] - 273.15
    t_col_ds04 = [c for c in df_ds04.columns if 'temp' in c.lower()]
    print("Kolom suhu DS04:", t_col_ds04)
    if 'temperature_2m_mean' in merged.columns:
        t_ds04 = merged['temperature_2m_mean']
        corr_t = t_ds01.corr(t_ds04)
        bias_t = np.mean(t_ds01 - t_ds04)
        print(f"Korelasi Suhu Rata-rata DS01 vs DS04: {corr_t:.3f}")
        print(f"Bias Suhu (DS01 - DS04): {bias_t:.3f} °C")
