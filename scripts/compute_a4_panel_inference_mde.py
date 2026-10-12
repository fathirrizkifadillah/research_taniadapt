"""
Script: compute_a4_panel_inference_mde.py
Purpose: Complete technical audit for Item A4:
         1. Compute Wild Cluster Bootstrap Webb (cluster = kabupaten) for AVP and Forest LOO-year
         2. Actually compute shifting windows (-1 month, registered, +1 month) and Lead Placebo (weather t+1)
         3. Compute analytical MDE from code with full formula and residual SDs
         4. Compute Rice MDE (T=3) with degrees-of-freedom warning
         5. Apply rigorous inferential logic comparing 95% CI against agronomically relevant effect size
"""

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
import sys

# Add project root to sys.path to import eda_utils
PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
sys.path.append(str(PROJECT_ROOT / "scripts"))
from eda_utils import wild_cluster_bootstrap_webb, compute_analytical_mde

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
AGERA5_DIR = DATA_RAW / "DS01_agera5"

# 1. Load Corn panel
df_corn = pd.read_csv(DATA_RAW / "DS05_subang_maize_productivity" / "produktivitas_jagung_jabar.csv")
sentra_kabs = sorted([k for k in df_corn["nama_kabupaten_kota"].unique() if k.startswith("KABUPATEN")])

# Corn panel 2015-2021 (excluding 2022 SUSPECT)
corn_panel = df_corn[(df_corn["nama_kabupaten_kota"].isin(sentra_kabs)) & 
                     (df_corn["tahun"] >= 2015) & (df_corn["tahun"] <= 2021) & 
                     (df_corn["produktivitas_jagung"] > 0)].copy()

# Extract weather windows from AgERA5 for each kabupaten
weather_records = []
for kab in sentra_kabs:
    slug = kab.lower().replace("kabupaten ", "kab_").replace(" ", "_")
    f_ag = AGERA5_DIR / f"agera5_{slug}_2015_2024.csv"
    if f_ag.exists():
        df_u = pd.read_csv(f_ag)
        df_u["date"] = pd.to_datetime(df_u["valid_time"])
        df_u["year"] = df_u["date"].dt.year
        df_u["month"] = df_u["date"].dt.month
        
        for yr in range(2015, 2023): # up to 2022 for lead weather
            p_jan_mar = df_u[(df_u["year"] == yr) & (df_u["month"].isin([1, 2, 3]))]["Precipitation_Flux"].sum()
            p_feb_apr = df_u[(df_u["year"] == yr) & (df_u["month"].isin([2, 3, 4]))]["Precipitation_Flux"].sum()
            p_mar_may = df_u[(df_u["year"] == yr) & (df_u["month"].isin([3, 4, 5]))]["Precipitation_Flux"].sum()
            weather_records.append({
                "nama_kabupaten_kota": kab,
                "tahun": yr,
                "precip_jan_mar": p_jan_mar,
                "precip_feb_apr": p_feb_apr,
                "precip_mar_may": p_mar_may
            })

df_weather = pd.DataFrame(weather_records)

# Create lead weather (weather at t+1)
df_weather_lead = df_weather[["nama_kabupaten_kota", "tahun", "precip_feb_apr"]].copy()
df_weather_lead["tahun_outcome"] = df_weather_lead["tahun"] - 1 # weather at yr matches outcome at yr-1
df_weather_lead.rename(columns={"precip_feb_apr": "precip_feb_apr_lead"}, inplace=True)

# Merge with corn panel
m_corn = pd.merge(corn_panel, df_weather, on=["nama_kabupaten_kota", "tahun"], how="inner")
m_corn = pd.merge(m_corn, df_weather_lead[["nama_kabupaten_kota", "tahun_outcome", "precip_feb_apr_lead"]], 
                  left_on=["nama_kabupaten_kota", "tahun"], right_on=["nama_kabupaten_kota", "tahun_outcome"], how="left")

m_corn["log_y"] = np.log(m_corn["produktivitas_jagung"])

# Standardize weather variables to z-scores (mean=0, std=1)
for col in ["precip_jan_mar", "precip_feb_apr", "precip_mar_may", "precip_feb_apr_lead"]:
    m_corn[f"{col}_z"] = (m_corn[col] - m_corn[col].mean()) / m_corn[col].std()

# Function to run Two-Way FE and compute wild cluster bootstrap Webb
def run_twfe_and_webb(df_sub, y_col, x_col, cluster_col="nama_kabupaten_kota"):
    # Partial out FE kabupaten and FE tahun
    res_y = sm.OLS.from_formula(f"{y_col} ~ C({cluster_col}) + C(tahun)", data=df_sub).fit().resid
    res_x = sm.OLS.from_formula(f"{x_col} ~ C({cluster_col}) + C(tahun)", data=df_sub).fit().resid
    
    beta_hat, ci_low, ci_high, boot_se = wild_cluster_bootstrap_webb(
        y_resid=res_y, x_resid=res_x, cluster_series=df_sub[cluster_col], n_boot=999, seed=42
    )
    
    sigma_y_resid = float(np.std(res_y, ddof=1))
    sigma_x_resid = float(np.std(res_x, ddof=1))
    n_obs = len(df_sub)
    n_clusters = df_sub[cluster_col].nunique()
    df_resid = n_obs - n_clusters - df_sub["tahun"].nunique()
    
    mde = compute_analytical_mde(sigma_y_resid, sigma_x_resid, n_obs, alpha=0.05, power=0.80, df=df_resid)
    
    return {
        "beta_hat": beta_hat,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "boot_se": boot_se,
        "sigma_y_resid": sigma_y_resid,
        "sigma_x_resid": sigma_x_resid,
        "n_obs": n_obs,
        "n_clusters": n_clusters,
        "df_resid": df_resid,
        "mde": mde,
        "res_y": res_y,
        "res_x": res_x
    }

# 1. Main model: H_CORN_01 (Feb-Apr)
res_main = run_twfe_and_webb(m_corn, "log_y", "precip_feb_apr_z")

# 2. Window shifts and lead placebo
res_shift_neg = run_twfe_and_webb(m_corn, "log_y", "precip_jan_mar_z")
res_shift_pos = run_twfe_and_webb(m_corn, "log_y", "precip_mar_may_z")
res_placebo_lead = run_twfe_and_webb(m_corn.dropna(subset=["precip_feb_apr_lead_z"]), "log_y", "precip_feb_apr_lead_z")

# 3. Forest LOO-Year models
loo_results = []
for yr_drop in sorted(m_corn["tahun"].unique()):
    sub_loo = m_corn[m_corn["tahun"] != yr_drop].copy()
    r_loo = run_twfe_and_webb(sub_loo, "log_y", "precip_feb_apr_z")
    loo_results.append({
        "dropped_year": yr_drop,
        "label": f"Buang {yr_drop}" + (" (Super El Nino)" if yr_drop == 2015 else (" (La Nina)" if yr_drop == 2016 else "")),
        "beta_hat": r_loo["beta_hat"],
        "ci_low": r_loo["ci_low"],
        "ci_high": r_loo["ci_high"],
        "mde": r_loo["mde"]
    })

# 4. Rice MDE (T=3, 2015-2017)
df_rice = pd.read_csv(DATA_RAW / "DS03_west_java_rice_productivity" / "produktivitas_padi_sawah_jabar.csv")
rice_panel = df_rice[(df_rice["nama_kabupaten_kota"].isin(sentra_kabs)) & 
                     (df_rice["tahun"] >= 2015) & (df_rice["tahun"] <= 2017) & 
                     (df_rice["produktivitas_padi"] > 0)].copy()

m_rice = pd.merge(rice_panel, df_weather, on=["nama_kabupaten_kota", "tahun"], how="inner")
m_rice["log_y"] = np.log(m_rice["produktivitas_padi"])
m_rice["precip_veg_z"] = (m_rice["precip_feb_apr"] - m_rice["precip_feb_apr"].mean()) / m_rice["precip_feb_apr"].std()

res_rice = run_twfe_and_webb(m_rice, "log_y", "precip_veg_z")

# Print complete summary
print("=== INFERENCE & MDE AUDIT SUMMARY (ITEM A4) ===")
print(f"MAIN CORN H_CORN_01 (2015-2021, N={res_main['n_obs']}):")
print(f"  Beta Hat: {res_main['beta_hat']:+.4f} log points / SD")
print(f"  Wild Cluster Bootstrap Webb 95% CI: [{res_main['ci_low']:+.4f}, {res_main['ci_high']:+.4f}]")
print(f"  Bootstrap SE: {res_main['boot_se']:.4f}")
print(f"  Sigma Outcome Resid: {res_main['sigma_y_resid']:.4f}, Sigma Weather Resid: {res_main['sigma_x_resid']:.4f}")
print(f"  Analytical MDE (alpha=0.05, power=0.80): +/- {res_main['mde']:.4f}")

print("\nWINDOW SENSITIVITY & LEAD PLACEBO (ACTUALLY COMPUTED):")
print(f"  Jan-Mar (-1 mo): beta={res_shift_neg['beta_hat']:+.4f}, 95% CI=[{res_shift_neg['ci_low']:+.4f}, {res_shift_neg['ci_high']:+.4f}], MDE=+/-{res_shift_neg['mde']:.4f}")
print(f"  Feb-Apr (Reg.):  beta={res_main['beta_hat']:+.4f}, 95% CI=[{res_main['ci_low']:+.4f}, {res_main['ci_high']:+.4f}], MDE=+/-{res_main['mde']:.4f}")
print(f"  Mar-May (+1 mo): beta={res_shift_pos['beta_hat']:+.4f}, 95% CI=[{res_shift_pos['ci_low']:+.4f}, {res_shift_pos['ci_high']:+.4f}], MDE=+/-{res_shift_pos['mde']:.4f}")
print(f"  Lead Placebo (t+1): beta={res_placebo_lead['beta_hat']:+.4f}, 95% CI=[{res_placebo_lead['ci_low']:+.4f}, {res_placebo_lead['ci_high']:+.4f}], MDE=+/-{res_placebo_lead['mde']:.4f}")

print(f"\nRICE MDE (T=3, 2015-2017, N={res_rice['n_obs']}, df={res_rice['df_resid']}):")
print(f"  Beta Hat: {res_rice['beta_hat']:+.4f}, 95% CI=[{res_rice['ci_low']:+.4f}, {res_rice['ci_high']:+.4f}]")
print(f"  Analytical MDE: +/- {res_rice['mde']:.4f} (Caveat: Residual kecil karena degrees of freedom sedikit df={res_rice['df_resid']}, BUKAN daya statistik tinggi!)")

# Save processed panel data and results to disk
m_corn.to_csv(DATA_PROCESSED / "corn_panel_weather_matched.csv", index=False)
m_rice.to_csv(DATA_PROCESSED / "rice_panel_weather_matched.csv", index=False)

res_summary = {
    "corn_main": {k: v for k, v in res_main.items() if not isinstance(v, pd.Series)},
    "corn_shift_neg": {k: v for k, v in res_shift_neg.items() if not isinstance(v, pd.Series)},
    "corn_shift_pos": {k: v for k, v in res_shift_pos.items() if not isinstance(v, pd.Series)},
    "corn_placebo_lead": {k: v for k, v in res_placebo_lead.items() if not isinstance(v, pd.Series)},
    "corn_loo": loo_results,
    "rice_t3": {k: v for k, v in res_rice.items() if not isinstance(v, pd.Series)}
}
pd.Series(res_summary).to_json(PROJECT_ROOT / "reports" / "dataset_audit" / "a10_panel_mde_audit.json")
print("Saved panel MDE audit results to reports/dataset_audit/a10_panel_mde_audit.json!")
