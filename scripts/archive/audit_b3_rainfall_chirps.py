import os
from pathlib import Path
import pandas as pd
import numpy as np
import urllib.request
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
AGERA5_DIR = PROJECT_ROOT / "data" / "raw" / "DS01_agera5"
CHIRPS_DIR = PROJECT_ROOT / "data" / "raw" / "CHIRPS"
CHIRPS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_DIR = REPORTS_DIR / "dataset_audit"

LOCATIONS = {
    "bandung": {"lat": -6.9, "lon": 107.6, "agera5_file": "agera5_bandung_2015_2024.csv"},
    "bekasi": {"lat": -6.2, "lon": 107.0, "agera5_file": "agera5_bekasi_2015_2024.csv"},
    "cirebon": {"lat": -6.7, "lon": 108.6, "agera5_file": "agera5_cirebon_2015_2024.csv"},
    "karawang": {"lat": -6.3, "lon": 107.3, "agera5_file": "agera5_karawang_2015_2024.csv"},
    "purwakarta": {"lat": -6.6, "lon": 107.4, "agera5_file": "agera5_purwakarta_2015_2024.csv"},
    "sukabumi": {"lat": -6.9, "lon": 106.9, "agera5_file": "agera5_sukabumi_2015_2024.csv"},
    "tasikmalaya": {"lat": -7.3, "lon": 108.2, "agera5_file": "agera5_tasikmalaya_2015_2024.csv"},
}

def get_chirps_df(loc_name, lat, lon):
    out_file = CHIRPS_DIR / f"chirps_{loc_name}_2015_2024.csv"
    if not out_file.exists() or out_file.stat().st_size < 50000:
        print(f"[{loc_name}] Fetching full 2015-2024 from ERDDAP...")
        url = (
            f"https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalDailyP05.csv?"
            f"precip[(2015-01-01T00:00:00Z):1:(2024-12-31T00:00:00Z)][({lat})][({lon})]"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            content = resp.read().decode("utf-8")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(content)
            
    df = pd.read_csv(out_file, skiprows=[1])
    return df

comparison_rows = []
annual_series = []

for loc_name, meta in LOCATIONS.items():
    df_ch = get_chirps_df(loc_name, meta["lat"], meta["lon"])
    df_ag = pd.read_csv(AGERA5_DIR / meta["agera5_file"])
    
    df_ag["date_str"] = pd.to_datetime(df_ag["valid_time"]).dt.strftime("%Y-%m-%d")
    df_ag["ag_precip"] = pd.to_numeric(df_ag["Precipitation_Flux"], errors="coerce")
    
    df_ch["date_str"] = pd.to_datetime(df_ch["time"]).dt.strftime("%Y-%m-%d")
    df_ch["ch_precip"] = pd.to_numeric(df_ch["precip"], errors="coerce")
    
    merged = pd.merge(df_ag[["date_str", "ag_precip"]], df_ch[["date_str", "ch_precip"]], on="date_str", how="inner").dropna()
    merged["year"] = pd.to_datetime(merged["date_str"]).dt.year
    merged["month"] = pd.to_datetime(merged["date_str"]).dt.to_period("M")
    
    r_daily = merged["ag_precip"].corr(merged["ch_precip"])
    
    monthly = merged.groupby("month")[["ag_precip", "ch_precip"]].sum().reset_index()
    r_monthly = monthly["ag_precip"].corr(monthly["ch_precip"])
    
    annual = merged.groupby("year")[["ag_precip", "ch_precip"]].sum().reset_index()
    annual["location"] = loc_name
    annual_series.append(annual)
    
    ag_ann_mean = annual["ag_precip"].mean()
    ch_ann_mean = annual["ch_precip"].mean()
    bias_ann_pct = ((ag_ann_mean - ch_ann_mean) / ch_ann_mean) * 100
    
    spearman_rank = annual["ag_precip"].rank().corr(annual["ch_precip"].rank())
    
    row_2016 = annual[annual["year"] == 2016]
    p_2016_ag = row_2016["ag_precip"].values[0] if len(row_2016) > 0 else np.nan
    p_2016_ch = row_2016["ch_precip"].values[0] if len(row_2016) > 0 else np.nan
    
    comparison_rows.append({
        "lokasi": loc_name,
        "lat": meta["lat"],
        "lon": meta["lon"],
        "agera5_annual_mean_mm": ag_ann_mean,
        "chirps_annual_mean_mm": ch_ann_mean,
        "bias_annual_pct": bias_ann_pct,
        "r_daily": r_daily,
        "r_monthly": r_monthly,
        "spearman_annual_rank": spearman_rank,
        "precip_2016_agera5_mm": p_2016_ag,
        "precip_2016_chirps_mm": p_2016_ch
    })

df_comp = pd.DataFrame(comparison_rows)
df_annual_all = pd.concat(annual_series, ignore_index=True)

print("=== HASIL PERBANDINGAN LENGKAP AGERA5 VS CHIRPS (2015-2024) ===")
print(df_comp.to_string(index=False))

df_comp.to_csv(AUDIT_DIR / "b3_rainfall_chirps_validation.csv", index=False)
df_annual_all.to_csv(AUDIT_DIR / "b3_annual_rainfall_comparison.csv", index=False)

# Diagnostic Plot
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=150)

# Subplot 1: Annual Rainfall Comparison for Tasikmalaya
ax1 = axes[0]
tasik_ann = df_annual_all[df_annual_all["location"] == "tasikmalaya"].sort_values("year")
w = 0.35
ax1.bar(tasik_ann["year"] - w/2, tasik_ann["ag_precip"], width=w, label="AgERA5 (Copernicus)", color="#3182bd")
ax1.bar(tasik_ann["year"] + w/2, tasik_ann["ch_precip"], width=w, label="CHIRPS v2 (NOAA/UCSB)", color="#e6550d")
ax1.set_title("Audit B3: Validasi Hujan Tahunan Tasikmalaya (2015-2024)", fontsize=11, fontweight="bold")
ax1.set_xlabel("Tahun", fontsize=10)
ax1.set_ylabel("Presipitasi Tahunan (mm/tahun)", fontsize=10)
ax1.set_xticks(tasik_ann["year"])
ax1.grid(True, linestyle=":", alpha=0.6)
ax1.legend()

peak_ag = tasik_ann.loc[tasik_ann['year']==2016, 'ag_precip'].values[0]
peak_ch = tasik_ann.loc[tasik_ann['year']==2016, 'ch_precip'].values[0]
ax1.annotate(f"Puncak 2016:\nAgERA5: {peak_ag:.0f} mm\nCHIRPS: {peak_ch:.0f} mm", 
             xy=(2016, peak_ag), xytext=(2016.3, peak_ag - 600),
             arrowprops=dict(arrowstyle="->", color="black", lw=1.2), fontsize=8.5,
             bbox=dict(boxstyle="round,pad=0.3", fc="#ffffcc", ec="gray"))

# Subplot 2: Multi-location Scatter of Monthly Rainfall
ax2 = axes[1]
colors = {"bandung": "#1b9e77", "tasikmalaya": "#d95f02", "karawang": "#7570b3", "cirebon": "#e7298a",
          "sukabumi": "#66a61e", "purwakarta": "#e6ab02", "bekasi": "#a6761d"}

for loc_name in LOCATIONS.keys():
    sub_ann = df_annual_all[df_annual_all["location"] == loc_name].sort_values("year")
    ax2.scatter(sub_ann["ch_precip"], sub_ann["ag_precip"], s=55, label=loc_name.capitalize(), color=colors.get(loc_name))

ax2.plot([1500, 6000], [1500, 6000], "k--", alpha=0.7, label="Garis 1:1")
ax2.set_title("Hujan Tahunan AgERA5 vs CHIRPS di 7 Lokasi (2015-2024)", fontsize=11, fontweight="bold")
ax2.set_xlabel("CHIRPS v2 Tahunan (mm)", fontsize=10)
ax2.set_ylabel("AgERA5 Tahunan (mm)", fontsize=10)
ax2.grid(True, linestyle=":", alpha=0.6)
ax2.legend(fontsize=8, loc="upper left")

plt.tight_layout()
fig_out = FIGURES_DIR / "b3_rainfall_chirps_validation.png"
plt.savefig(fig_out)
plt.close()
print(f"Grafik diagnostik disimpan di: {fig_out}")
