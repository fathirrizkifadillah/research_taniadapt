"""
Script: audit_b3_rainfall_bias_chirps_v2.py
Purpose: Audit and reconcile AgERA5 vs CHIRPS precipitation across all 27 units in West Java.
Author: TaniAdapt Research Team (Adversarial Audit v2)
Date: 2026-10-11
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
AGERA5_DIR = PROJECT_ROOT / "data" / "raw" / "DS01_agera5"
CHIRPS_DIR = PROJECT_ROOT / "data" / "raw" / "CHIRPS"
REPORTS_DIR = PROJECT_ROOT / "reports" / "dataset_audit"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load centroids and elevation audit
df_grid = pd.read_csv(REPORTS_DIR / "a8_spatial_grid_cells_audit.csv")
# Columns: nama_kabupaten_kota, tipe_wilayah, true_centroid_lat, true_centroid_lon, agera5_cell_lat, agera5_cell_lon, elevation_dem_m, shared_cell_flag, effective_n_flag

def get_slug(name):
    return name.lower().replace("kabupaten ", "kab_").replace("kota ", "kota_").replace(" ", "_")

def get_short(name):
    return name.lower().replace("kabupaten ", "").replace("kota ", "").replace(" ", "_")

print("Processing 27 units...")

records = []

for _, r in df_grid.iterrows():
    name = r["nama_kabupaten_kota"]
    slug = get_slug(name)
    short = get_short(name)
    elev = r["dem_elevation_m"]
    tipe = r["tipe_wilayah"]
    
    # --- Load AgERA5 ---
    agera5_file = AGERA5_DIR / f"agera5_{slug}_2015_2024.csv"
    if not agera5_file.exists():
        print(f"Warning: Missing AgERA5 file for {slug}")
        continue
    
    df_ag = pd.read_csv(agera5_file)
    df_ag["date"] = pd.to_datetime(df_ag["valid_time"])
    df_ag["year"] = df_ag["date"].dt.year
    df_ag["month"] = df_ag["date"].dt.month
    df_ag["precip_agera5"] = df_ag["Precipitation_Flux"]
    
    # --- Load CHIRPS ---
    chirps_dfs = []
    
    # Check 10-year file first
    f_10y = CHIRPS_DIR / f"chirps_{short}_2015_2024.csv"
    if not f_10y.exists():
        f_10y = CHIRPS_DIR / f"chirps_{slug}_2015_2024.csv"
        
    if f_10y.exists():
        df_ch_raw = pd.read_csv(f_10y, skiprows=[1])
        df_ch_raw["date"] = pd.to_datetime(df_ch_raw["time"].str.split("T").str[0])
        df_ch_raw["precip_chirps"] = df_ch_raw["precip"]
        chirps_dfs.append(df_ch_raw[["date", "precip_chirps"]])
    
    # Also check individual year files (2016, 2020, 2024)
    for yr in [2016, 2020, 2024]:
        f_yr = CHIRPS_DIR / f"chirps_{slug}_{yr}.csv"
        if not f_yr.exists():
            f_yr = CHIRPS_DIR / f"chirps_{short}_{yr}.csv"
        if f_yr.exists() and (not f_10y.exists()):
            try:
                df_yr_raw = pd.read_csv(f_yr, skiprows=[1])
                df_yr_raw["date"] = pd.to_datetime(df_yr_raw["time"].str.split("T").str[0])
                df_yr_raw["precip_chirps"] = df_yr_raw["precip"]
                chirps_dfs.append(df_yr_raw[["date", "precip_chirps"]])
            except Exception as e:
                pass
                
    if not chirps_dfs:
        print(f"Warning: No CHIRPS data found for {name}")
        continue
        
    df_ch = pd.concat(chirps_dfs, ignore_index=True).drop_duplicates(subset=["date"])
    df_ch["year"] = df_ch["date"].dt.year
    df_ch["month"] = df_ch["date"].dt.month
    
    # Merge daily
    merged = pd.merge(df_ag[["date", "year", "month", "precip_agera5"]], 
                      df_ch[["date", "precip_chirps"]], 
                      on="date", how="inner")
    
    if merged.empty:
        print(f"Warning: Empty merge for {name}")
        continue
        
    # Monthly aggregation
    monthly = merged.groupby(["year", "month"]).agg(
        precip_agera5=("precip_agera5", "sum"),
        precip_chirps=("precip_chirps", "sum"),
        days=("date", "count")
    ).reset_index()
    # Filter only complete months (>= 28 days)
    monthly = monthly[monthly["days"] >= 28].copy()
    
    # Monthly climatology & anomalies (z-score per calendar month)
    monthly["anomaly_agera5"] = 0.0
    monthly["anomaly_chirps"] = 0.0
    for m in range(1, 13):
        idx = monthly["month"] == m
        if idx.sum() > 1:
            mean_ag = monthly.loc[idx, "precip_agera5"].mean()
            std_ag = monthly.loc[idx, "precip_agera5"].std(ddof=1)
            mean_ch = monthly.loc[idx, "precip_chirps"].mean()
            std_ch = monthly.loc[idx, "precip_chirps"].std(ddof=1)
            
            monthly.loc[idx, "anomaly_agera5"] = (monthly.loc[idx, "precip_agera5"] - mean_ag) / (std_ag if std_ag > 0 else 1)
            monthly.loc[idx, "anomaly_chirps"] = (monthly.loc[idx, "precip_chirps"] - mean_ch) / (std_ch if std_ch > 0 else 1)
            
    # Monthly anomaly correlations
    valid_anom = monthly.dropna(subset=["anomaly_agera5", "anomaly_chirps"])
    if len(valid_anom) >= 12:
        r_pearson, p_pearson = stats.pearsonr(valid_anom["anomaly_agera5"], valid_anom["anomaly_chirps"])
        r_spearman, p_spearman = stats.spearmanr(valid_anom["anomaly_agera5"], valid_anom["anomaly_chirps"])
    else:
        r_pearson, r_spearman = np.nan, np.nan
        
    # Annual totals for common full years
    annual = merged.groupby("year").agg(
        precip_agera5=("precip_agera5", "sum"),
        precip_chirps=("precip_chirps", "sum"),
        days=("date", "count")
    ).reset_index()
    # Keep years with >= 360 days
    annual = annual[annual["days"] >= 360].copy()
    
    annual["bias_pct"] = (annual["precip_agera5"] - annual["precip_chirps"]) / annual["precip_chirps"] * 100.0
    
    # Specific benchmark years (2016, 2020, 2024)
    b_2016 = annual[annual["year"] == 2016]
    b_2020 = annual[annual["year"] == 2020]
    b_2024 = annual[annual["year"] == 2024]
    
    bias_2016 = b_2016["bias_pct"].values[0] if not b_2016.empty else np.nan
    bias_2020 = b_2020["bias_pct"].values[0] if not b_2020.empty else np.nan
    bias_2024 = b_2024["bias_pct"].values[0] if not b_2024.empty else np.nan
    
    ch_2016 = b_2016["precip_chirps"].values[0] if not b_2016.empty else np.nan
    ch_2020 = b_2020["precip_chirps"].values[0] if not b_2020.empty else np.nan
    ch_2024 = b_2024["precip_chirps"].values[0] if not b_2024.empty else np.nan
    
    ag_2016 = b_2016["precip_agera5"].values[0] if not b_2016.empty else np.nan
    ag_2020 = b_2020["precip_agera5"].values[0] if not b_2020.empty else np.nan
    ag_2024 = b_2024["precip_agera5"].values[0] if not b_2024.empty else np.nan
    
    # Seasonal bias: MH (Nov-Apr) vs MK (May-Oct)
    monthly["season"] = monthly["month"].apply(lambda m: "MH" if m in [11, 12, 1, 2, 3, 4] else "MK")
    mh = monthly[monthly["season"] == "MH"]
    mk = monthly[monthly["season"] == "MK"]
    
    bias_mh = (mh["precip_agera5"].sum() - mh["precip_chirps"].sum()) / mh["precip_chirps"].sum() * 100.0 if mh["precip_chirps"].sum() > 0 else np.nan
    bias_mk = (mk["precip_agera5"].sum() - mk["precip_chirps"].sum()) / mk["precip_chirps"].sum() * 100.0 if mk["precip_chirps"].sum() > 0 else np.nan
    
    # Overall signed bias (mean across available full years, keeping sign)
    overall_bias_signed = annual["bias_pct"].mean()
    
    # Full 10-year stats for AgERA5
    ag_10y_mean = df_ag.groupby("year")["precip_agera5"].sum().mean()
    
    # CHIRPS mean across available full years
    ch_mean = annual["precip_chirps"].mean()
    ag_mean = annual["precip_agera5"].mean()
    
    records.append({
        "lokasi": name, # Explicitly 'lokasi', not 'stasiun'!
        "tipe_wilayah": tipe,
        "elevasi_dem_m": elev,
        "n_tahun_overlap": len(annual),
        "tahun_overlap": str(sorted(annual["year"].tolist())),
        "mean_tahunan_chirps_mm": round(ch_mean, 1),
        "mean_tahunan_agera5_mm": round(ag_mean, 1),
        "mean_tahunan_agera5_10y_mm": round(ag_10y_mean, 1),
        "bias_persen_signed_mean": round(overall_bias_signed, 2),
        "bias_pct_2016": round(bias_2016, 2) if not np.isnan(bias_2016) else np.nan,
        "bias_pct_2020": round(bias_2020, 2) if not np.isnan(bias_2020) else np.nan,
        "bias_pct_2024": round(bias_2024, 2) if not np.isnan(bias_2024) else np.nan,
        "chirps_2016_mm": round(ch_2016, 1) if not np.isnan(ch_2016) else np.nan,
        "chirps_2020_mm": round(ch_2020, 1) if not np.isnan(ch_2020) else np.nan,
        "chirps_2024_mm": round(ch_2024, 1) if not np.isnan(ch_2024) else np.nan,
        "agera5_2016_mm": round(ag_2016, 1) if not np.isnan(ag_2016) else np.nan,
        "agera5_2020_mm": round(ag_2020, 1) if not np.isnan(ag_2020) else np.nan,
        "agera5_2024_mm": round(ag_2024, 1) if not np.isnan(ag_2024) else np.nan,
        "bias_musim_hujan_mh_pct": round(bias_mh, 2),
        "bias_musim_kemarau_mk_pct": round(bias_mk, 2),
        "korelasi_pearson_anomali": round(r_pearson, 3),
        "korelasi_spearman_anomali": round(r_spearman, 3),
        "n_bulan_anomali": len(valid_anom)
    })

df_res = pd.DataFrame(records)
out_csv = REPORTS_DIR / "b3_rainfall_bias_chirps_audit_v2.csv"
df_res.to_csv(out_csv, index=False)
print(f"Saved audit v2 to: {out_csv}")
print(df_res.head(10))

# Print diagnostic analysis requested in A2:
print("\n" + "="*70)
print("DIAGNOSTIC ANALYSIS FOR A2:")
print("="*70)

# Check Bandung Raya bias vs other regions
bandung_raya = df_res[df_res["lokasi"].str.contains("BANDUNG|CIMAHI", case=False, na=False)]
print("\n--- BANDUNG RAYA BIAS ---")
print(bandung_raya[["lokasi", "elevasi_dem_m", "mean_tahunan_chirps_mm", "mean_tahunan_agera5_mm", "bias_persen_signed_mean", "korelasi_pearson_anomali"]])

# Check Tasikmalaya claim: 4,466 mm
tasik = df_res[df_res["lokasi"].str.contains("TASIKMALAYA", case=False, na=False)]
print("\n--- TASIKMALAYA INVESTIGATION ---")
print(tasik[["lokasi", "n_tahun_overlap", "mean_tahunan_chirps_mm", "mean_tahunan_agera5_mm", "chirps_2016_mm", "chirps_2020_mm", "chirps_2024_mm", "bias_persen_signed_mean"]])

# Check elevation correlation with bias
df_valid_elev = df_res.dropna(subset=["elevasi_dem_m", "bias_persen_signed_mean"])
r_elev, p_elev = stats.pearsonr(df_valid_elev["elevasi_dem_m"], df_valid_elev["bias_persen_signed_mean"])
print(f"\nKorelasi Elevasi vs Bias Signed: r = {r_elev:.3f}")

# Check Wettest ranking in AgERA5 vs CHIRPS
print("\n--- TOP 5 WETTEST LOCATIONS (AgERA5) ---")
print(df_res.sort_values(by="mean_tahunan_agera5_mm", ascending=False)[["lokasi", "elevasi_dem_m", "mean_tahunan_agera5_mm", "mean_tahunan_chirps_mm", "bias_persen_signed_mean"]].head(5))

print("\n--- TOP 5 WETTEST LOCATIONS (CHIRPS) ---")
print(df_res.sort_values(by="mean_tahunan_chirps_mm", ascending=False)[["lokasi", "elevasi_dem_m", "mean_tahunan_chirps_mm", "mean_tahunan_agera5_mm", "bias_persen_signed_mean"]].head(5))
