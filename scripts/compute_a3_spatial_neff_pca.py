"""
Script: compute_a3_spatial_neff_pca.py
Purpose: Compute spatial dependence and PCA decomposition on DESEASONALIZED monthly anomalies
         across the 22 unique AgERA5 grid cells in West Java (2015-2024, 120 months).
Encodes PhD-level methods from .agents/skills/data-scientist.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
RAW_AGERA5 = PROJECT_ROOT / "data" / "raw" / "DS01_agera5"
AUDIT_CELLS = PROJECT_ROOT / "reports" / "dataset_audit" / "a8_spatial_grid_cells_audit.csv"
OUTPUT_PROCESSED = PROJECT_ROOT / "data" / "processed" / "agera5_22_cells_monthly_anomalies.csv"

df_cells = pd.read_csv(AUDIT_CELLS)

# Select one representative per unique agera5_cell_id
unique_cell_reps = df_cells.drop_duplicates(subset=["agera5_cell_id"]).copy()
print(f"Total unique AgERA5 cells: {len(unique_cell_reps)}")

cell_monthly = {}
for _, r in unique_cell_reps.iterrows():
    cell_id = r["agera5_cell_id"]
    slug = r["agera5_file"].replace("agera5_", "").replace("_2015_2024.csv", "")
    f_path = RAW_AGERA5 / r["agera5_file"]
    
    df = pd.read_csv(f_path)
    df["dt"] = pd.to_datetime(df["valid_time"])
    df["ym"] = df["dt"].dt.to_period("M")
    df["month"] = df["dt"].dt.month
    
    # Monthly sum of precipitation
    m_sum = df.groupby(["ym", "month"])["Precipitation_Flux"].sum().reset_index()
    # Deseasonalized anomaly: subtract 10-year calendar month mean
    m_sum["calendar_month_mean"] = m_sum.groupby("month")["Precipitation_Flux"].transform("mean")
    m_sum["anomaly"] = m_sum["Precipitation_Flux"] - m_sum["calendar_month_mean"]
    
    cell_monthly[cell_id] = m_sum.set_index("ym")["anomaly"]

df_anom = pd.DataFrame(cell_monthly).dropna()
print(f"Deseasonalized anomaly matrix shape: {df_anom.shape} (120 months x 22 cells)")
df_anom.to_csv(OUTPUT_PROCESSED)

# 1. Spatial correlation of anomalies
corr_anom = df_anom.corr()
mean_offdiag_corr = float(corr_anom.values[np.triu_indices_from(corr_anom.values, k=1)].mean())
min_offdiag_corr = float(corr_anom.values[np.triu_indices_from(corr_anom.values, k=1)].min())
max_offdiag_corr = float(corr_anom.values[np.triu_indices_from(corr_anom.values, k=1)].max())

# 2. PCA on anomalies
pca = PCA()
pca.fit(df_anom)
var_ratio = pca.explained_variance_ratio_ * 100.0
cum_var = np.cumsum(var_ratio)

# Components needed for 80% variance
n_comp_80 = int(np.argmax(cum_var >= 80.0) + 1)
n_comp_90 = int(np.argmax(cum_var >= 90.0) + 1)

print("\n=== RESULTS OF SPATIAL N_EFF & ANOMALY PCA AUDIT ===")
print(f"Mean pairwise anomaly correlation: {mean_offdiag_corr:.4f} (range: {min_offdiag_corr:.4f} to {max_offdiag_corr:.4f})")
print(f"PCA Variance Explained: PC1={var_ratio[0]:.2f}%, PC2={var_ratio[1]:.2f}%, PC3={var_ratio[2]:.2f}%")
print(f"Components required for 80% cumulative variance: {n_comp_80} components")
print(f"Components required for 90% cumulative variance: {n_comp_90} components")
print(f"Cumulative variance for top {n_comp_80} components: {cum_var[n_comp_80-1]:.2f}%")
