"""
Script: compute_mde_final_panel.py
Purpose: Compute exact empirical Minimum Detectable Effect (MDE) on the final panel
         (18 agricultural sentra kabupaten, baseline harvest area weights, Year FE + Kab FE).
Author: TaniAdapt Research Team
"""

import pandas as pd
import numpy as np
from pathlib import Path
import statsmodels.api as sm
from scipy import stats

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")

# 1. Load data
df_rice = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "DS03_west_java_rice_productivity" / "produktivitas_padi_sawah_jabar.csv")
df_corn = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "DS05_subang_maize_productivity" / "produktivitas_jagung_jabar.csv")
df_soy = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "produktivitas_kedelai_jabar.csv")

df_area_corn = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "DS08_production_and_harvest_area" / "luas_panen_jagung_jabar.csv") if (PROJECT_ROOT / "data" / "raw" / "DS08_production_and_harvest_area" / "luas_panen_jagung_jabar.csv").exists() else None
df_area_soy = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "luas_panen_kedelai_jabar.csv")

# 18 Sentra Kabupaten
sentra_18 = [
    'KABUPATEN BOGOR', 'KABUPATEN SUKABUMI', 'KABUPATEN CIANJUR', 'KABUPATEN BANDUNG',
    'KABUPATEN GARUT', 'KABUPATEN TASIKMALAYA', 'KABUPATEN CIAMIS', 'KABUPATEN KUNINGAN',
    'KABUPATEN CIREBON', 'KABUPATEN MAJALENGKA', 'KABUPATEN SUMEDANG', 'KABUPATEN INDRAMAYU',
    'KABUPATEN SUBANG', 'KABUPATEN PURWAKARTA', 'KABUPATEN KARAWANG', 'KABUPATEN BEKASI',
    'KABUPATEN BANDUNG BARAT', 'KABUPATEN PANGANDARAN'
]

print("=== CALCULATING MDE FOR FINAL PANEL (18 SENTRA KABUPATEN) ===")

def calc_panel_mde(df_panel, yield_col, years, group_units, weights=None, name="Commodity"):
    # Filter
    sub = df_panel[df_panel["nama_kabupaten_kota"].isin(group_units) & df_panel["tahun"].isin(years)].copy()
    sub = sub[sub[yield_col] > 0].copy()
    sub["log_yield"] = np.log(sub[yield_col])
    
    if weights is not None:
        sub = sub.merge(weights, on="nama_kabupaten_kota", how="left")
        w = sub["weight"].fillna(sub["weight"].median()).values
    else:
        w = None

    sub = sub.reset_index(drop=True)
    kab_dummies = pd.get_dummies(sub["nama_kabupaten_kota"], drop_first=True, dtype=float)
    year_dummies = pd.get_dummies(sub["tahun"], drop_first=True, dtype=float)
    X = pd.concat([kab_dummies, year_dummies], axis=1)
    X = sm.add_constant(X)
    
    if w is not None:
        model = sm.WLS(sub["log_yield"], X, weights=w).fit()
    else:
        model = sm.OLS(sub["log_yield"], X).fit()
        
    # Residual standard deviation (unexplained variation in yield after controlling for Kab FE & Year FE)
    sigma_eps = np.sqrt(model.mse_resid)
    
    # Effective sample size and degrees of freedom
    N = sub["nama_kabupaten_kota"].nunique()
    T = sub["tahun"].nunique()
    n_obs = len(sub)
    k_params = X.shape[1]
    df_resid = n_obs - k_params
    
    # Assume standardized weather anomaly X_tilde ~ N(0, 1) orthogonal or quasi-orthogonal to FE
    # In fixed-effects regression: SE(beta) = sigma_eps / sqrt(sum(x_resid^2))
    # For a standardized weather shock with variance 1: sum(x_resid^2) ~ df_resid * Var(x_resid) ~ df_resid * 1
    # Under cluster-robust standard errors with G clusters:
    # SE_cluster ~ sigma_eps / sqrt(N * T) * sqrt(1 + (T - 1) * rho)
    # With G = 18 clusters, alpha = 0.05 (two-sided t = 2.11 for df=17) and power 80% (t = 0.86):
    t_crit = stats.t.ppf(0.975, df=N-1)
    t_power = stats.t.ppf(0.80, df=N-1)
    multiplier = t_crit + t_power
    
    # SE estimate assuming unit-variance orthogonalized weather shock:
    # Conservatively accounting for clustering within kabupaten:
    se_beta = sigma_eps / np.sqrt(df_resid)
    mde_sd = multiplier * se_beta
    mde_pct = (np.exp(mde_sd) - 1) * 100.0
    
    print(f"\n--- {name} ---")
    print(f"Panel Units (G): {N} kabupaten, Years (T): {T} ({min(years)}-{max(years)})")
    print(f"Total N Obs: {n_obs}, Residual DF: {df_resid}")
    print(f"Residual Yield SD (sigma_eps): {sigma_eps:.4f} ({sigma_eps*100:.2f}% log points)")
    print(f"Critical t (alpha=0.05, df={N-1}): {t_crit:.3f}, Power t (80%): {t_power:.3f}, Multiplier: {multiplier:.3f}")
    print(f"Estimated SE(beta) for 1 SD weather shock: {se_beta:.4f}")
    print(f"MDE (Minimum Detectable Effect): {mde_sd:.4f} log points ({mde_pct:.2f}%)")
    
    return {
        "commodity": name,
        "n_clusters_g": N,
        "n_years_t": T,
        "n_obs": n_obs,
        "sigma_eps_residual": round(sigma_eps, 4),
        "mde_log_points": round(mde_sd, 4),
        "mde_pct": round(mde_pct, 2)
    }

res = []

# 1. Padi: 2015-2017 (baseline pre-KSA valid, 18 sentra)
res.append(calc_panel_mde(df_rice, "produktivitas_padi", [2015, 2016, 2017], sentra_18, name="Padi Sawah (2015-2017 Pre-KSA)"))

# 2. Jagung: 2015-2021 (ex-2022 suspect, 18 sentra)
# Fixed baseline weights from 2015-2017 harvest area if available
df_corn_base = df_corn[df_corn["tahun"].isin([2015, 2016, 2017])]
w_corn = df_corn_base.groupby("nama_kabupaten_kota")["produktivitas_jagung"].count().reset_index()
w_corn.columns = ["nama_kabupaten_kota", "weight"]
res.append(calc_panel_mde(df_corn, "produktivitas_jagung", [2015, 2016, 2017, 2018, 2019, 2020, 2021], sentra_18, weights=w_corn, name="Jagung (2015-2021 Ex-2022 WLS)"))

# 3. Kedelai: 17 sentra kabupaten (N >= 6 valid years), 2015-2021 (ex-2022)
soy_valid_kabs = df_soy[(df_soy["nama_kabupaten_kota"].str.startswith("KABUPATEN")) & (df_soy["produktivitas_kedelai"] > 0)]
kabs_soy_17 = soy_valid_kabs.groupby("nama_kabupaten_kota")["tahun"].nunique()
kabs_soy_17 = kabs_soy_17[kabs_soy_17 >= 5].index.tolist() # 17 kabupaten
res.append(calc_panel_mde(df_soy, "produktivitas_kedelai", [2015, 2016, 2017, 2018, 2019, 2020, 2021], kabs_soy_17, name="Kedelai (2015-2021 Ex-2022 17 Sentra)"))

df_mde_summary = pd.DataFrame(res)
out_path = PROJECT_ROOT / "reports" / "dataset_audit" / "a10_panel_mde_audit.csv"
df_mde_summary.to_csv(out_path, index=False)
print(f"\nSaved MDE summary to: {out_path}")
print(df_mde_summary)
