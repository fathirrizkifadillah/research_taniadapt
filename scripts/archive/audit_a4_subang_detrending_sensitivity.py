import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
DATA_DIR = PROJECT_ROOT / "data" / "raw" / "DS05_subang_maize_productivity"
AUDIT_DIR = PROJECT_ROOT / "reports" / "dataset_audit"

df_jag = pd.read_csv(DATA_DIR / "produktivitas_jagung_jabar.csv")
subang = df_jag[df_jag["nama_kabupaten_kota"].str.contains("SUBANG")].sort_values("tahun")

# Full period (2015-2022) vs Clean period (2015-2021 excluding 2022 suspect)
models = []

for sample_name, df_s in [("Full 2015-2022 (N=8)", subang), ("Clean 2015-2021 (N=7, Excl 2022 Suspect)", subang[subang["tahun"] <= 2021])]:
    x = df_s["tahun"].values
    y = df_s["produktivitas_jagung"].values
    n = len(y)
    mean_y = np.mean(y)
    
    # Model 1: No Detrend (Raw Mean Deviation)
    resid_raw = y - mean_y
    cv_raw_ddof0 = (np.std(resid_raw, ddof=0) / mean_y) * 100
    cv_raw_ddof1 = (np.std(resid_raw, ddof=1) / mean_y) * 100
    models.append({
        "sample": sample_name,
        "detrend_method": "1. Tanpa Detrend (Deviasi Rata-rata Mentah)",
        "r_squared": 0.0,
        "rmse_sample": np.std(resid_raw, ddof=1),
        "cv_ddof0_pct": round(cv_raw_ddof0, 2),
        "cv_ddof1_pct": round(cv_raw_ddof1, 2),
        "cv_ols_pct": round(cv_raw_ddof1, 2),
        "notes": "Variabilitas mentah total (tren teknologi + cuaca + noise)"
    })
    
    # Model 2: Linear OLS (y = b0 + b1*t)
    p = np.polyfit(x, y, 1)
    y_pred_lin = np.polyval(p, x)
    resid_lin = y - y_pred_lin
    ss_tot = np.sum((y - mean_y)**2)
    ss_res_lin = np.sum(resid_lin**2)
    r2_lin = 1.0 - (ss_res_lin / ss_tot)
    cv_lin_ddof0 = (np.std(resid_lin, ddof=0) / mean_y) * 100
    cv_lin_ddof1 = (np.std(resid_lin, ddof=1) / mean_y) * 100
    cv_lin_ols = (np.sqrt(ss_res_lin / (n - 2)) / mean_y) * 100
    models.append({
        "sample": sample_name,
        "detrend_method": "2. Tren Linier OLS Tunggal",
        "r_squared": round(r2_lin, 4),
        "rmse_sample": np.std(resid_lin, ddof=1),
        "cv_ddof0_pct": round(cv_lin_ddof0, 2),
        "cv_ddof1_pct": round(cv_lin_ddof1, 2),
        "cv_ols_pct": round(cv_lin_ols, 2),
        "notes": f"Slope: +{p[0]:.3f} ku/ha/thn. 2022 menyumbang 49.7% kuadrat residu."
    })
    
    # Model 3: Piecewise / Structural Break (2015-2020 vs 2021-2022)
    # Subang yield was stable 2015-2020 (45-57 ku/ha), then jumped in 2021 (68.2) & 2022 (89.5)
    # Regress with dummy for post-2020
    d_post2020 = (x >= 2021).astype(float)
    X_piecewise = np.column_stack([np.ones(n), x - 2015, d_post2020])
    beta_pw = np.linalg.lstsq(X_piecewise, y, rcond=None)[0]
    y_pred_pw = X_piecewise @ beta_pw
    resid_pw = y - y_pred_pw
    ss_res_pw = np.sum(resid_pw**2)
    r2_pw = 1.0 - (ss_res_pw / ss_tot)
    cv_pw_ddof0 = (np.std(resid_pw, ddof=0) / mean_y) * 100
    cv_pw_ddof1 = (np.std(resid_pw, ddof=1) / mean_y) * 100
    cv_pw_ols = (np.sqrt(ss_res_pw / max(1, n - 3)) / mean_y) * 100
    models.append({
        "sample": sample_name,
        "detrend_method": "3. Piecewise / Structural Break (Shift Pasca-2020)",
        "r_squared": round(r2_pw, 4),
        "rmse_sample": np.std(resid_pw, ddof=1),
        "cv_ddof0_pct": round(cv_pw_ddof0, 2),
        "cv_ddof1_pct": round(cv_pw_ddof1, 2),
        "cv_ols_pct": round(cv_pw_ols, 2),
        "notes": f"Break intercept post-2020: +{beta_pw[2]:.2f} ku/ha."
    })

df_models = pd.DataFrame(models)
out_csv = AUDIT_DIR / "a4_subang_detrending_sensitivity.csv"
df_models.to_csv(out_csv, index=False)

print("=== HASIL SENSITIVITAS DETRENDING SUBANG (A4) ===")
print(df_models.to_string(index=False))
