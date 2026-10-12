"""Create auditable Phase 4 counts from local raw files without credential access."""
import json
from pathlib import Path
import pandas as pd
from project_paths import PROJECT_ROOT

RAW = PROJECT_ROOT / "data" / "raw"
OUT = PROJECT_ROOT / "reports" / "logs"
OUT.mkdir(parents=True, exist_ok=True)

grid = pd.read_csv(PROJECT_ROOT / "reports" / "dataset_audit" / "a8_spatial_grid_cells_audit.csv")
results = []
for crop, rel, outcome in [
    ("padi", "DS03_west_java_rice_productivity/produktivitas_padi_sawah_jabar.csv", "produktivitas_padi"),
    ("jagung", "DS05_subang_maize_productivity/produktivitas_jagung_jabar.csv", "produktivitas_jagung"),
    ("kedelai", "produktivitas_kedelai_jabar.csv", "produktivitas_kedelai"),
]:
    d = pd.read_csv(RAW / rel)
    max_year = 2017 if crop == "padi" else 2021
    d = d[d["tahun"].between(2015, max_year) & d["nama_kabupaten_kota"].str.startswith("KABUPATEN")].copy()
    med = d[outcome].median()
    mad = (d[outcome] - med).abs().median()
    if mad == 0:
        d["outlier_near_zero_flag"] = False
    else:
        d["outlier_near_zero_flag"] = (0.6745 * (d[outcome] - med).abs() / mad > 3.5) | (d[outcome] <= 0)
    active = d[~d["outlier_near_zero_flag"]]
    cells = grid[grid["nama_kabupaten_kota"].isin(active["nama_kabupaten_kota"])]["agera5_cell_id"].nunique()
    results.append({"crop": crop, "period": f"2015-{max_year}", "n_after_robust_flag": len(active), "unique_agera5_cells": cells, "median": med, "mad": mad})

pd.DataFrame(results).to_csv(OUT / "crop_cell_and_outlier_audit.csv", index=False)
print((OUT / "crop_cell_and_outlier_audit.csv").as_posix())
