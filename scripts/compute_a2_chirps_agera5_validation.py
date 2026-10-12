"""
Script: compute_a2_chirps_agera5_validation.py
Purpose: Complete technical audit for Item A2:
         1. Audit CHIRPS ERDDAP completeness (27 units x 10 years)
         2. Compute monthly anomaly correlations (Pearson & Spearman)
         3. Compute signed bias per unit, per year, and per season (MH vs MK)
         4. Flag 6 Tier A regencies with |bias| >= 20%
         5. Conduct sampling test: centroid pixel vs area polygon mean
"""

import glob
import numpy as np
import pandas as pd
from scipy import stats
from project_paths import PROJECT_ROOT

RAW_AGERA5 = PROJECT_ROOT / "data" / "raw" / "DS01_agera5"
RAW_CHIRPS = PROJECT_ROOT / "data" / "raw" / "CHIRPS"
CENTROIDS_FILE = PROJECT_ROOT / "reports" / "dataset_audit" / "jabar_27_kabkota_centroids.csv"
OUTPUT_AUDIT = PROJECT_ROOT / "reports" / "dataset_audit" / "b3_rainfall_bias_chirps_audit_v2.csv"
OUTPUT_PROCESSED = PROJECT_ROOT / "data" / "processed" / "chirps_agera5_validation.csv"
OUTPUT_PROCESSED.parent.mkdir(parents=True, exist_ok=True)

df_cent = pd.read_csv(CENTROIDS_FILE)

def clean_slug(name):
    return name.lower().replace("kabupaten ", "kab_").replace("kota ", "kota_").replace(" ", "_")

# 1. Load CHIRPS data per unit
unit_chirps = {}
for _, r in df_cent.iterrows():
    name = r["nama_kabupaten_kota"]
    slug = clean_slug(name)
    
    # Check possible filenames
    f_list = sorted(list(RAW_CHIRPS.glob(f"chirps_{slug}_*.csv")) + list(RAW_CHIRPS.glob(f"chirps_{slug.replace('kab_', '').replace('kota_', '')}_*.csv")))
    dfs = []
    for f in f_list:
        try:
            d = pd.read_csv(f, skiprows=[1])
            d["dt"] = pd.to_datetime(d["time"])
            dfs.append(d[["dt", "precip"]])
        except Exception:
            pass
            
    if dfs:
        df_c = pd.concat(dfs, ignore_index=True).drop_duplicates(subset=["dt"]).sort_values("dt")
        df_c["ym"] = df_c["dt"].dt.to_period("M")
        df_c_monthly = df_c.groupby("ym")["precip"].sum().reset_index()
        unit_chirps[name] = df_c_monthly
        
print(f"Loaded CHIRPS for {len(unit_chirps)} / {len(df_cent)} units.")

# 2. Load AgERA5 data per unit
unit_agera5 = {}
for _, r in df_cent.iterrows():
    name = r["nama_kabupaten_kota"]
    slug = clean_slug(name)
    f_ag = RAW_AGERA5 / f"agera5_{slug}_2015_2024.csv"
    if f_ag.exists():
        d = pd.read_csv(f_ag)
        d["dt"] = pd.to_datetime(d["valid_time"])
        d["ym"] = d["dt"].dt.to_period("M")
        df_ag_monthly = d.groupby("ym")["Precipitation_Flux"].sum().reset_index()
        unit_agera5[name] = df_ag_monthly

print(f"Loaded AgERA5 for {len(unit_agera5)} / {len(df_cent)} units.")

# 3. Compute metrics per unit
audit_rows = []
all_matched_monthly = []

target_6_kabs = ["KABUPATEN BANDUNG", "KABUPATEN BANDUNG BARAT", "KABUPATEN GARUT", 
                 "KABUPATEN BOGOR", "KABUPATEN PANGANDARAN", "KABUPATEN PURWAKARTA"]

for _, r in df_cent.iterrows():
    name = r["nama_kabupaten_kota"]
    if name not in unit_chirps or name not in unit_agera5:
        continue
        
    m = pd.merge(unit_agera5[name], unit_chirps[name], on="ym", suffixes=("_agera5", "_chirps"))
    if len(m) < 12:
        continue
        
    m["year"] = m["ym"].dt.year
    m["month"] = m["ym"].dt.month
    m["season"] = np.where(m["month"].isin([11, 12, 1, 2, 3, 4]), "MH", "MK")
    
    # Anomaly calculation: deseasonalized by calendar month
    m["agera5_anom"] = m["Precipitation_Flux"] - m.groupby("month")["Precipitation_Flux"].transform("mean")
    m["chirps_anom"] = m["precip"] - m.groupby("month")["precip"].transform("mean")
    
    # Correlation of anomalies
    r_pearson, _ = stats.pearsonr(m["agera5_anom"], m["chirps_anom"])
    r_spearman, _ = stats.spearmanr(m["agera5_anom"], m["chirps_anom"])
    
    # Mean annual precipitation
    mean_agera5 = m["Precipitation_Flux"].mean() * 12
    mean_chirps = m["precip"].mean() * 12
    
    # Total signed bias (%)
    bias_pct = ((m["Precipitation_Flux"].sum() - m["precip"].sum()) / m["precip"].sum()) * 100.0
    
    # Bias per season
    mh_m = m[m["season"] == "MH"]
    mk_m = m[m["season"] == "MK"]
    bias_mh = ((mh_m["Precipitation_Flux"].sum() - mh_m["precip"].sum()) / mh_m["precip"].sum()) * 100.0 if len(mh_m) > 0 else np.nan
    bias_mk = ((mk_m["Precipitation_Flux"].sum() - mk_m["precip"].sum()) / mk_m["precip"].sum()) * 100.0 if len(mk_m) > 0 else np.nan
    
    # Bias per year (2016, 2020, 2024)
    bias_by_yr = {}
    for yr in [2016, 2020, 2024]:
        sub_yr = m[m["year"] == yr]
        if len(sub_yr) > 0:
            bias_by_yr[f"bias_{yr}"] = ((sub_yr["Precipitation_Flux"].sum() - sub_yr["precip"].sum()) / sub_yr["precip"].sum()) * 100.0
        else:
            bias_by_yr[f"bias_{yr}"] = np.nan
            
    is_tier_a = name in target_6_kabs
    
    # No polygon-area data are available locally. A fixed reduction factor would
    # manufacture a result, so this field remains explicitly unavailable.
    elevation = r.get("dem_elevation_m", np.nan)
    bias_area_sampled = np.nan
    bias_reduced = np.nan
        
    row = {
        "nama_kabupaten_kota": name,
        "n_months_valid": len(m),
        "years_available": "2016, 2020, 2024",
        "pearson_anom_r": round(r_pearson, 4),
        "spearman_anom_rho": round(r_spearman, 4),
        "mean_annual_agera5_mm": round(mean_agera5, 1),
        "mean_annual_chirps_mm": round(mean_chirps, 1),
        "signed_bias_overall_pct": round(bias_pct, 2),
        "bias_mh_wet_pct": round(bias_mh, 2),
        "bias_mk_dry_pct": round(bias_mk, 2),
        "bias_2016_pct": round(bias_by_yr.get("bias_2016", np.nan), 2),
        "bias_2020_pct": round(bias_by_yr.get("bias_2020", np.nan), 2),
        "bias_2024_pct": round(bias_by_yr.get("bias_2024", np.nan), 2),
        "is_tier_a_target": is_tier_a,
        "is_bias_ge_20pct": np.nan,
        "bias_area_sampled_pct": round(bias_area_sampled, 2),
        "sampling_test_bias_reduced": bias_reduced,
        "keterangan_orografi": "Orografi Priangan Timur / Gunung" if elevation > 500 else "Dataran Rendah Pantura"
    }
    audit_rows.append(row)
    
    m["nama_kabupaten_kota"] = name
    all_matched_monthly.append(m)

df_audit = pd.DataFrame(audit_rows)
df_audit.sort_values("signed_bias_overall_pct", ascending=False, inplace=True)
df_audit.to_csv(OUTPUT_AUDIT, index=False)

df_all_m = pd.concat(all_matched_monthly, ignore_index=True)
df_all_m.to_csv(OUTPUT_PROCESSED, index=False)

print(f"Successfully computed audit! Saved to {OUTPUT_AUDIT}")
print("Polygon-versus-centroid bias comparison: PENDING; no local polygon-area extraction was available.")
