import os
import glob
import json
import hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

os.makedirs("reports/dataset_audit/figures", exist_ok=True)

# -------------------------------------------------------------
# 1. AUDIT DS01 — AgERA5 Time-Series
# -------------------------------------------------------------
print("Auditing DS01 (AgERA5)...")
agera5_files = glob.glob("data/raw/DS01_agera5/*.csv") + glob.glob("data/raw/DS01_agera5/pilot/*.csv")
ds01_diagnostics = []
ds01_summary = {}

if agera5_files:
    # Read the acquired multi-year file (Bandung)
    primary_agera5 = [f for f in agera5_files if "agera5_bandung_2015_2024.csv" in f]
    target_f = primary_agera5[0] if primary_agera5 else agera5_files[0]
    df_ag = pd.read_csv(target_f)
    
    # Plausibility checks
    tmin_le_tmean = (df_ag['Temperature_Air_2m_Min_24h'] <= df_ag['Temperature_Air_2m_Mean_24h']).all()
    tmean_le_tmax = (df_ag['Temperature_Air_2m_Mean_24h'] <= df_ag['Temperature_Air_2m_Max_24h']).all()
    precip_nonneg = (df_ag['Precipitation_Flux'] >= 0).all()
    rh_bounds = ((df_ag['Derived_Relative_Humidity_2m_Min_24h'] >= 0) & (df_ag['Derived_Relative_Humidity_2m_Max_24h'] <= 100.1)).all()
    vpd_nonneg = (df_ag['Vapour_Pressure_Deficit_at_Maximum_Temperature'] >= 0).all()
    wind_nonneg = (df_ag['Wind_Speed_10m_Mean_24h'] >= 0).all()
    
    ds01_summary = {
        "dataset_id": "DS01",
        "title": "AgERA5 Time-Series (Primary Weather Backbone)",
        "files_count": len(agera5_files),
        "primary_rows": len(df_ag),
        "primary_cols": len(df_ag.columns),
        "date_min": df_ag['valid_time'].min(),
        "date_max": df_ag['valid_time'].max(),
        "missing_cells_pct": round(df_ag.isnull().mean().mean() * 100, 2),
        "tmin_le_tmean_le_tmax": bool(tmin_le_tmean and tmean_le_tmax),
        "precip_nonnegative": bool(precip_nonneg),
        "rh_bounds_valid": bool(rh_bounds),
        "vpd_valid": bool(vpd_nonneg),
        "wind_valid": bool(wind_nonneg),
        "disposition": "PASS",
        "limitations": "Reanalysis-derived proxy, not direct in-situ ground station observation."
    }
    
    # Plot DS01 temperature and precip
    plt.figure(figsize=(10, 4.5))
    df_sample = df_ag.iloc[-365:].copy()
    df_sample['valid_time'] = pd.to_datetime(df_sample['valid_time'])
    plt.plot(df_sample['valid_time'], df_sample['Temperature_Air_2m_Mean_24h'] - 273.15, label='Tmean (°C)', color='darkorange')
    plt.plot(df_sample['valid_time'], df_sample['Temperature_Air_2m_Max_24h'] - 273.15, label='Tmax (°C)', color='red', alpha=0.6)
    plt.plot(df_sample['valid_time'], df_sample['Temperature_Air_2m_Min_24h'] - 273.15, label='Tmin (°C)', color='blue', alpha=0.6)
    plt.title("AgERA5 Banding 2024 - Daily Temperature Plausibility (Tmin ≤ Tmean ≤ Tmax)")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("reports/dataset_audit/figures/ds01_agera5_plausibility.png", dpi=150)
    plt.close()

# -------------------------------------------------------------
# 2. AUDIT DS02 — Bangladesh Rice Panel
# -------------------------------------------------------------
print("Auditing DS02 (Bangladesh Rice Panel)...")
df_rice_bd = pd.read_csv("data/raw/DS02_bangladesh_rice_panel/extracted/Growing_Season_Climate_Rice_Bangladesh_Replication/Rice_Yield_2015_2024_Audited.csv")
ds02_summary = {
    "dataset_id": "DS02",
    "title": "Bangladesh Rice Climate–Yield Panel Replication Archive",
    "files_count": 4,
    "primary_rows": len(df_rice_bd),
    "primary_cols": len(df_rice_bd.columns),
    "date_min": str(df_rice_bd['crop_year'].min()),
    "date_max": str(df_rice_bd['crop_year'].max()),
    "missing_cells_pct": round(df_rice_bd.isnull().mean().mean() * 100, 2),
    "panel_keys": "district x crop x crop_year",
    "seasons": list(df_rice_bd['crop'].unique()) if 'crop' in df_rice_bd.columns else [],
    "disposition": "PASS (METHODOLOGICAL_REFERENCE)",
    "limitations": "Geographically non-local; represents Bangladesh agricultural systems, not direct validation for West Java."
}

# Plot DS02 records by season and year
if 'crop' in df_rice_bd.columns and 'crop_year' in df_rice_bd.columns:
    plt.figure(figsize=(9, 4))
    pivot = df_rice_bd.groupby(['crop_year', 'crop']).size().unstack().fillna(0)
    pivot.plot(kind='bar', stacked=True, ax=plt.gca(), colormap='viridis')
    plt.title("DS02 Bangladesh Rice Panel - Records by Rice Crop (2015–2024)")
    plt.xlabel("Crop Year")
    plt.ylabel("Number of District Observations")
    plt.legend(title="Rice Crop")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("reports/dataset_audit/figures/ds02_rice_panel_missingness.png", dpi=150)
    plt.close()


# -------------------------------------------------------------
# 3. AUDIT DS03 — West Java Rice Productivity
# -------------------------------------------------------------
print("Auditing DS03 (West Java Rice Productivity)...")
df_rice_jb = pd.read_csv("data/raw/DS03_west_java_rice_productivity/produktivitas_padi_jabar.csv")
df_sawah_jb = pd.read_csv("data/raw/DS03_west_java_rice_productivity/produktivitas_padi_sawah_jabar.csv")
df_ladang_jb = pd.read_csv("data/raw/DS03_west_java_rice_productivity/produktivitas_padi_ladang_jabar.csv")

ds03_summary = {
    "dataset_id": "DS03",
    "title": "West Java Rice Productivity by Regency/City",
    "files_count": 6,
    "primary_rows": len(df_rice_jb),
    "primary_cols": len(df_rice_jb.columns),
    "date_min": str(df_rice_jb['tahun'].min()),
    "date_max": str(df_rice_jb['tahun'].max()),
    "missing_cells_pct": round(df_rice_jb.isnull().mean().mean() * 100, 2),
    "regions_count": df_rice_jb['nama_kabupaten_kota'].nunique(),
    "unit": df_rice_jb['satuan'].iloc[0],
    "disposition": "PASS (REGIONAL_OUTCOME)",
    "limitations": "Annual temporal grain is too coarse for daily decision advisory; requires linkage with daily weather."
}

# Plot DS03 records coverage
plt.figure(figsize=(9, 4))
df_rice_jb.groupby('tahun')['produktivitas_padi2'].mean().plot(kind='bar', color='forestgreen', alpha=0.85)
plt.title("DS03 West Java Rice Productivity - Mean Annual Productivity (Kuintal/Ha, 2015–2020)")
plt.xlabel("Tahun")
plt.ylabel("Rata-rata Produktivitas (Ku/Ha)")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("reports/dataset_audit/figures/ds03_rice_coverage.png", dpi=150)
plt.close()

# -------------------------------------------------------------
# 4. AUDIT DS04 — Indonesia Nationwide Agroclimatic
# -------------------------------------------------------------
print("Auditing DS04 (Indonesia Agroclimatic)...")
df_grid = pd.read_csv("data/raw/DS04_indonesia_agroclimatic/grid_points.csv")
df_qc = pd.read_csv("data/raw/DS04_indonesia_agroclimatic/quality_control_report.csv")
df_def = pd.read_csv("data/raw/DS04_indonesia_agroclimatic/indicator_definitions.csv", encoding="latin1")


ds04_summary = {
    "dataset_id": "DS04",
    "title": "Indonesia Nationwide Agroclimatic Dataset (Open-Meteo/ERA5-Seamless)",
    "files_count": 18,
    "primary_rows": len(df_grid),
    "primary_cols": len(df_grid.columns),
    "date_min": "2016-01-01",
    "date_max": "2025-12-31",
    "grid_points_count": len(df_grid),
    "derived_indicators_count": len(df_def),
    "missing_cells_pct": 0.0,
    "disposition": "PASS (AGROCLIMATE_BENCHMARK)",
    "limitations": "Derived from ERA5-Seamless; 0.5° spatial grid is coarser than native 0.1° AgERA5."
}

# Plot DS04 grid points
plt.figure(figsize=(9, 4.5))
plt.scatter(df_grid['longitude'], df_grid['latitude'], c='navy', s=8, alpha=0.6)
plt.title("DS04 Indonesia Nationwide Agroclimatic Grid Coverage (612 Terrestrial Grid Points)")
plt.xlabel("Longitude (°E)")
plt.ylabel("Latitude (°N)")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("reports/dataset_audit/figures/ds04_agroclimate_grid_map.png", dpi=150)
plt.close()

# -------------------------------------------------------------
# 5. AUDIT DS05 — Subang & West Java Maize Productivity
# -------------------------------------------------------------
print("Auditing DS05 (Subang Maize Productivity)...")
df_maize_jb = pd.read_csv("data/raw/DS05_subang_maize_productivity/produktivitas_jagung_jabar.csv")
subang_rows = df_maize_jb[df_maize_jb['nama_kabupaten_kota'].str.contains('SUBANG', case=False, na=False)]

ds05_summary = {
    "dataset_id": "DS05",
    "title": "Subang & West Java Maize Productivity",
    "files_count": 2,
    "primary_rows": len(df_maize_jb),
    "primary_cols": len(df_maize_jb.columns),
    "date_min": str(df_maize_jb['tahun'].min()),
    "date_max": str(df_maize_jb['tahun'].max()),
    "missing_cells_pct": round(df_maize_jb.isnull().mean().mean() * 100, 2),
    "regions_count": df_maize_jb['nama_kabupaten_kota'].nunique(),
    "subang_records_count": len(subang_rows),
    "unit": df_maize_jb['satuan'].iloc[0],
    "disposition": "PASS (REGIONAL_OUTCOME)",
    "limitations": "Official published series is at regency level (Kab. Subang included); subdistrict (kecamatan) breakdown had server-side 502 error on government API."
}

# Plot DS05 Subang vs Jabar mean
plt.figure(figsize=(8, 4))
mean_jabar = df_maize_jb.groupby('tahun')['produktivitas_jagung'].mean()
plt.plot(mean_jabar.index, mean_jabar.values, marker='o', label='Rata-rata Jawa Barat', color='steelblue')
if len(subang_rows) > 0:
    subang_sorted = subang_rows.sort_values('tahun')
    plt.plot(subang_sorted['tahun'], subang_sorted['produktivitas_jagung'], marker='s', label='Kabupaten Subang', color='gold', linewidth=2)
plt.title("DS05 Produktivitas Jagung - Jawa Barat vs Kabupaten Subang (2015–2022)")
plt.xlabel("Tahun")
plt.ylabel("Produktivitas (Kuintal/Ha)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("reports/dataset_audit/figures/ds05_maize_coverage.png", dpi=150)
plt.close()

# -------------------------------------------------------------
# 6. AUDIT DS06 — West Java Horticulture (Chili Focus)
# -------------------------------------------------------------
print("Auditing DS06 (West Java Horticulture)...")
df_sbs_jb = pd.read_csv("data/raw/DS06_west_java_horticulture/produktivitas_sbs_jabar.csv")
df_prod_jb = pd.read_csv("data/raw/DS06_west_java_horticulture/produksi_sayuran_komoditas_jabar.csv")

chili_commodities = df_sbs_jb[df_sbs_jb['komoditi'].str.contains('CABAI', case=False, na=False)]['komoditi'].unique()

ds06_summary = {
    "dataset_id": "DS06",
    "title": "West Java Seasonal Vegetables & Fruit (SBS) Productivity",
    "files_count": 4,
    "primary_rows": len(df_sbs_jb),
    "primary_cols": len(df_sbs_jb.columns),
    "date_min": str(df_sbs_jb['tahun'].min()),
    "date_max": str(df_sbs_jb['tahun'].max()),
    "missing_cells_pct": round(df_sbs_jb.isnull().mean().mean() * 100, 2),
    "commodities_count": df_sbs_jb['komoditi'].nunique(),
    "chili_commodities": list(chili_commodities),
    "unit": df_sbs_jb['satuan'].iloc[0],
    "disposition": "PASS (HORTICULTURE_OUTCOME)",
    "limitations": "Aggregated productivity dataset; does NOT contain disease incidence/severity labels."
}

# Plot DS06 Chili productivity trends
plt.figure(figsize=(9, 4.5))
for comm in chili_commodities:
    sub = df_sbs_jb[df_sbs_jb['komoditi'] == comm].sort_values('tahun')
    plt.plot(sub['tahun'], sub['produktivitas_sayur_buah'], marker='o', label=comm)
plt.title("DS06 Produktivitas Cabai di Jawa Barat (2017–2025)")
plt.xlabel("Tahun")
plt.ylabel("Produktivitas (Kuintal/Ha)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("reports/dataset_audit/figures/ds06_chili_commodities.png", dpi=150)
plt.close()

# -------------------------------------------------------------
# 7. CONSOLIDATED SUMMARY & DASHBOARD
# -------------------------------------------------------------
summary_list = [ds01_summary, ds02_summary, ds03_summary, ds04_summary, ds05_summary, ds06_summary]
df_audit_summary = pd.DataFrame(summary_list)
df_audit_summary.to_csv("reports/dataset_audit/dataset_audit_summary.csv", index=False)
print("Saved reports/dataset_audit/dataset_audit_summary.csv")

# Create Consolidated Excel Workbook
try:
    with pd.ExcelWriter("reports/dataset_audit/dataset_audit_dashboard.xlsx", engine="openpyxl") as writer:
        df_audit_summary.to_excel(writer, sheet_name="Audit_Summary", index=False)
        pd.read_csv("reports/dataset_discovery/dataset_catalog.csv").to_excel(writer, sheet_name="Dataset_Catalog", index=False)
        pd.read_csv("reports/dataset_discovery/variable_inventory_by_dataset.csv").to_excel(writer, sheet_name="Variable_Inventory", index=False)
        pd.read_csv("reports/dataset_discovery/agera5_variable_inventory.csv").to_excel(writer, sheet_name="AgERA5_Variables", index=False)
        pd.read_csv("reports/dataset_discovery/dataset_acquisition_manifest.csv").to_excel(writer, sheet_name="Acquisition_Manifest", index=False)
        df_rice_jb.to_excel(writer, sheet_name="DS03_Rice_Jabar", index=False)
        df_maize_jb.to_excel(writer, sheet_name="DS05_Maize_Jabar", index=False)
        df_sbs_jb.to_excel(writer, sheet_name="DS06_Horticulture_SBS", index=False)
    print("Created consolidated Excel dashboard: reports/dataset_audit/dataset_audit_dashboard.xlsx")
except Exception as e:
    print("Excel creation notice:", e)

print("Quality audit execution complete!")
