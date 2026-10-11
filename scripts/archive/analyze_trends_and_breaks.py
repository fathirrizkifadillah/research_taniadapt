import os
from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
REPORTS_DIR = PROJECT_ROOT / "reports"
AUDIT_DIR = REPORTS_DIR / "dataset_audit"

# -----------------------------------------------------------------------------
# 1. KOREKSI BUG R2 & HITUNG TREN UNTUK SEMUA 27 KABUPATEN (PADI & JAGUNG)
# -----------------------------------------------------------------------------
def calculate_trend(x, y):
    """
    Menghitung tren linier OLS tanpa bug penempatan kurung.
    x: array tahun
    y: array produktivitas
    """
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    n = len(x)
    if n < 3 or np.isnan(y).any():
        return np.nan, np.nan, np.nan, np.nan, np.nan
    
    p = np.polyfit(x, y, 1)
    y_pred = np.polyval(p, x)
    
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    ss_res = np.sum((y - y_pred) ** 2)  # CATATAN: kuadrat HARUS di dalam sum!
    
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    cv_raw = (np.std(y, ddof=1) / np.mean(y)) * 100.0 if np.mean(y) > 0 else np.nan
    cv_resid = (np.std(y - y_pred, ddof=1) / np.mean(y)) * 100.0 if np.mean(y) > 0 else np.nan
    
    return p[0], p[1], r2, cv_raw, cv_resid

# A. Jagung (DS05: 2015-2022)
df_maize = pd.read_csv(PROJECT_ROOT / "data/raw/DS05_subang_maize_productivity/produktivitas_jagung_jabar.csv")
maize_trends = []

for kab, grp in df_maize.groupby('nama_kabupaten_kota'):
    grp = grp.sort_values('tahun')
    slope, intercept, r2, cv_raw, cv_resid = calculate_trend(grp['tahun'], grp['produktivitas_jagung'])
    maize_trends.append({
        'komoditas': 'Jagung',
        'nama_kabupaten_kota': kab,
        'periode': '2015-2022',
        'n_tahun': len(grp),
        'mean_yield': grp['produktivitas_jagung'].mean(),
        'slope_ku_ha_thn': slope,
        'r2_linear': r2,
        'cv_raw_pct': cv_raw,
        'cv_resid_pct': cv_resid
    })

df_maize_trends = pd.DataFrame(maize_trends)
df_maize_trends.to_csv(AUDIT_DIR / "maize_27_kab_trends.csv", index=False)

# Cek spesifik Subang
subang_row = df_maize_trends[df_maize_trends['nama_kabupaten_kota'].str.contains('SUBANG')].iloc[0]
print("=== VERIFIKASI A1: KOREKSI BUG SUBANG MAIZE ===")
print(f"Subang Slope     : {subang_row['slope_ku_ha_thn']:.4f} ku/ha/tahun")
print(f"Subang R2        : {subang_row['r2_linear']:.4f} (SEBELUMNYA TERTULIS SALAH 1.000)")
print(f"Subang CV Raw    : {subang_row['cv_raw_pct']:.2f}%")
print(f"Subang CV Resid  : {subang_row['cv_resid_pct']:.2f}%")

print("\nRata-rata Jagung Se-Jawa Barat (27 Kab/Kota):")
print(f"  Rata-rata Slope  : {df_maize_trends['slope_ku_ha_thn'].mean():.4f} ku/ha/tahun")
print(f"  Rata-rata R2     : {df_maize_trends['r2_linear'].mean():.4f}")
print(f"  Rata-rata CV Raw : {df_maize_trends['cv_raw_pct'].mean():.2f}%")
print(f"  Rata-rata CV Res : {df_maize_trends['cv_resid_pct'].mean():.2f}%")

# B. Padi (DS03: 2015-2020)
df_rice = pd.read_csv(PROJECT_ROOT / "data/raw/DS03_west_java_rice_productivity/produktivitas_padi_jabar.csv")
rice_trends = []

for kab, grp in df_rice.groupby('nama_kabupaten_kota'):
    grp = grp.sort_values('tahun')
    slope, intercept, r2, cv_raw, cv_resid = calculate_trend(grp['tahun'], grp['produktivitas_padi2'])
    rice_trends.append({
        'komoditas': 'Padi Total',
        'nama_kabupaten_kota': kab,
        'periode': '2015-2020',
        'n_tahun': len(grp),
        'mean_yield': grp['produktivitas_padi2'].mean(),
        'slope_ku_ha_thn': slope,
        'r2_linear': r2,
        'cv_raw_pct': cv_raw,
        'cv_resid_pct': cv_resid
    })

df_rice_trends = pd.DataFrame(rice_trends)
df_rice_trends.to_csv(AUDIT_DIR / "rice_27_kab_trends.csv", index=False)

print("\nRata-rata Padi Total Se-Jawa Barat (27 Kab/Kota):")
print(f"  Rata-rata Slope  : {df_rice_trends['slope_ku_ha_thn'].mean():.4f} ku/ha/tahun")
print(f"  Rata-rata R2     : {df_rice_trends['r2_linear'].mean():.4f}")
print(f"  Rata-rata CV Raw : {df_rice_trends['cv_raw_pct'].mean():.2f}%")
print(f"  Rata-rata CV Res : {df_rice_trends['cv_resid_pct'].mean():.2f}%")

# -----------------------------------------------------------------------------
# 2. ANALISIS LONJAKAN TAHUN-KE-TAHUN (LOG-DIFF) 27 KABUPATEN
# -----------------------------------------------------------------------------
print("\n=== VERIFIKASI A2: ANALISIS LONJAKAN TAHUN-KE-TAHUN (LOG-DIFF) ===")

# A. Jagung Log-diff
piv_mz = df_maize.pivot(index='tahun', columns='nama_kabupaten_kota', values='produktivitas_jagung')
log_diff_mz = np.log(piv_mz) - np.log(piv_mz.shift(1))
log_diff_mz = log_diff_mz.dropna()

# Hitung statistik per tahun lintas 27 kabupaten
stats_mz_year = []
for yr in log_diff_mz.index:
    vals = log_diff_mz.loc[yr]
    subang_val = log_diff_mz.loc[yr, [c for c in log_diff_mz.columns if 'SUBANG' in c][0]]
    stats_mz_year.append({
        'tahun': yr,
        'median_log_diff': vals.median(),
        'mean_log_diff': vals.mean(),
        'std_log_diff': vals.std(),
        'min_log_diff': vals.min(),
        'max_log_diff': vals.max(),
        'subang_log_diff': subang_val,
        'pct_kab_positif': (vals > 0).mean() * 100.0,
        'pct_kab_lonjak_gt_15pct': (vals > 0.15).mean() * 100.0
    })

df_mz_yoy = pd.DataFrame(stats_mz_year)
df_mz_yoy.to_csv(AUDIT_DIR / "maize_yoy_log_diff_summary.csv", index=False)
log_diff_mz.to_csv(AUDIT_DIR / "maize_27_kab_log_diff_matrix.csv")

print("Ringkasan Log-Diff Jagung Antar-Tahun (Lintas 27 Kabupaten):")
print(df_mz_yoy.to_string(index=False))

# B. Padi Log-diff
piv_rc = df_rice.pivot(index='tahun', columns='nama_kabupaten_kota', values='produktivitas_padi2')
log_diff_rc = np.log(piv_rc) - np.log(piv_rc.shift(1))
log_diff_rc = log_diff_rc.dropna()

stats_rc_year = []
for yr in log_diff_rc.index:
    vals = log_diff_rc.loc[yr]
    stats_rc_year.append({
        'tahun': yr,
        'median_log_diff': vals.median(),
        'mean_log_diff': vals.mean(),
        'std_log_diff': vals.std(),
        'min_log_diff': vals.min(),
        'max_log_diff': vals.max(),
        'pct_kab_positif': (vals > 0).mean() * 100.0,
        'pct_kab_lonjak_gt_10pct': (vals > 0.10).mean() * 100.0
    })

df_rc_yoy = pd.DataFrame(stats_rc_year)
df_rc_yoy.to_csv(AUDIT_DIR / "rice_yoy_log_diff_summary.csv", index=False)
log_diff_rc.to_csv(AUDIT_DIR / "rice_27_kab_log_diff_matrix.csv")

print("\nRingkasan Log-Diff Padi Antar-Tahun (Lintas 27 Kabupaten):")
print(df_rc_yoy.to_string(index=False))

# -----------------------------------------------------------------------------
# 3. PERBANDINGAN TIGA METODE PEMBERSIHAN TREN (DETRENDING) PADA JAGUNG
# -----------------------------------------------------------------------------
print("\n=== PERBANDINGAN 3 METODE DETRENDING (JAGUNG 2015-2022) ===")

# Siapkan panel jagung
df_mz_panel = df_maize[['tahun', 'nama_kabupaten_kota', 'produktivitas_jagung']].copy()
y = df_mz_panel['produktivitas_jagung'].values
ss_tot = np.sum((y - np.mean(y)) ** 2)

# (i) Linier per kabupaten
y_pred_m1 = np.zeros_like(y)
for kab in df_mz_panel['nama_kabupaten_kota'].unique():
    mask = df_mz_panel['nama_kabupaten_kota'] == kab
    x_k = df_mz_panel.loc[mask, 'tahun'].values
    y_k = df_mz_panel.loc[mask, 'produktivitas_jagung'].values
    p_k = np.polyfit(x_k, y_k, 1)
    y_pred_m1[mask] = np.polyval(p_k, x_k)

res_m1 = y - y_pred_m1
ss_res_m1 = np.sum(res_m1 ** 2)
r2_m1 = 1.0 - (ss_res_m1 / ss_tot)
cv_res_m1 = (np.std(res_m1, ddof=54) / np.mean(y)) * 100.0

# (ii) Fixed effect kabupaten + Fixed effect tahun (Two-Way FE)
# y_it = alpha_i + gamma_t + e_it
# Estimasi OLS via dummy variables
df_dummies = pd.get_dummies(df_mz_panel[['nama_kabupaten_kota', 'tahun']], drop_first=True, dtype=float)
X_m2 = np.column_stack([np.ones(len(df_mz_panel)), df_dummies.values])
beta_m2, _, _, _ = np.linalg.lstsq(X_m2, y, rcond=None)
y_pred_m2 = X_m2 @ beta_m2
res_m2 = y - y_pred_m2
ss_res_m2 = np.sum(res_m2 ** 2)
r2_m2 = 1.0 - (ss_res_m2 / ss_tot)
k_m2 = X_m2.shape[1]
cv_res_m2 = (np.std(res_m2, ddof=k_m2) / np.mean(y)) * 100.0

# (iii) Kabupaten FE + Tren Provinsi (Provincial Mean / Median Trend)
prov_mean_yr = df_mz_panel.groupby('tahun')['produktivitas_jagung'].mean()
df_mz_panel['prov_mean'] = df_mz_panel['tahun'].map(prov_mean_yr)
kab_dummies = pd.get_dummies(df_mz_panel['nama_kabupaten_kota'], drop_first=True, dtype=float)
X_m3 = np.column_stack([np.ones(len(df_mz_panel)), df_mz_panel['prov_mean'].values, kab_dummies.values])
beta_m3, _, _, _ = np.linalg.lstsq(X_m3, y, rcond=None)
y_pred_m3 = X_m3 @ beta_m3
res_m3 = y - y_pred_m3
ss_res_m3 = np.sum(res_m3 ** 2)
r2_m3 = 1.0 - (ss_res_m3 / ss_tot)
k_m3 = X_m3.shape[1]
cv_res_m3 = (np.std(res_m3, ddof=k_m3) / np.mean(y)) * 100.0

detrending_comparison = pd.DataFrame([
    {
        'metode': '(i) Linear Trend per Kabupaten',
        'formula': 'y_it = alpha_i + beta_i * t + e_it',
        'n_params': 54,
        'ss_res': round(ss_res_m1, 2),
        'r2_model': round(r2_m1, 4),
        'cv_residual_pct': round(cv_res_m1, 2),
        'variasi_cuaca_tersisa': 'Variasi antar-tahun & antar-kabupaten di luar tren linier lokal. Kelemahan: mengasumsikan teknologi linier mulus.'
    },
    {
        'metode': '(ii) Two-Way Fixed Effects (Kab FE + Year FE)',
        'formula': 'y_it = alpha_i + gamma_t + e_it',
        'n_params': k_m2,
        'ss_res': round(ss_res_m2, 2),
        'r2_model': round(r2_m2, 4),
        'cv_residual_pct': round(cv_res_m2, 2),
        'variasi_cuaca_tersisa': 'HANYA variasi cuaca SPASIAL antar-kabupaten dalam tahun yang sama. Guncangan makro iklim seprovinsi (ENSO El Nino/La Nina) TERSERAP HABIS oleh Year FE.'
    },
    {
        'metode': '(iii) Kab FE + Provincial Trend',
        'formula': 'y_it = alpha_i + beta * prov_mean_t + e_it',
        'n_params': k_m3,
        'ss_res': round(ss_res_m3, 2),
        'r2_model': round(r2_m3, 4),
        'cv_residual_pct': round(cv_res_m3, 2),
        'variasi_cuaca_tersisa': 'Variasi deviasi lokal kabupaten dari rata-rata provinsi. Menjaga sebagian sinyal tahunan tanpa mengorbankan derajat kebebasan sebanyak Year FE.'
    }
])

detrending_comparison.to_csv(AUDIT_DIR / "maize_detrending_methods_comparison.csv", index=False)
print(detrending_comparison[['metode', 'n_params', 'r2_model', 'cv_residual_pct']].to_string(index=False))

print("\nEksekusi script analisis tren & break selesai 100%!")
