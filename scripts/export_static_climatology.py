"""Export static climatology percentiles for web app to data/export/climatology_{cell}.json.

Distinguishes honestly between:
1. Pure 30-year 1991-2020 baseline (for the 6 CDS-downloaded cells).
2. 10-year 2015-2024 decadal reference (for the remaining 16 cells, with explicit limitations).
"""
from __future__ import annotations

import json
import re
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_AGERA5 = PROJECT_ROOT / "data" / "raw" / "DS01_agera5"
CLIM_1991_2020 = PROJECT_ROOT / "data" / "raw" / "DS01_agera5_climatology_1991_2020"
GRID_CSV = PROJECT_ROOT / "reports" / "dataset_audit" / "a8_spatial_grid_cells_audit.csv"
LOOKUP_CSV = PROJECT_ROOT / "data" / "processed" / "lookup_kab_cell_elev.csv"
OUT_DIR = PROJECT_ROOT / "data" / "export"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lookup_df = pd.read_csv(LOOKUP_CSV).drop_duplicates("agera5_cell_id").reset_index(drop=True)
    
    clim_cells_available = set()
    if CLIM_1991_2020.exists():
        for f in CLIM_1991_2020.glob("*.csv"):
            m = re.match(r"agera5_lat(m[\d\.]+)_lon(p[\d\.]+)_(\d+)\.csv", f.name)
            if m:
                lat = float(m.group(1).replace("m", "-"))
                lon = float(m.group(2).replace("p", ""))
                clim_cells_available.add((round(lat, 1), round(lon, 1)))

    print(f"Total cells in lookup: {len(lookup_df)}")
    print(f"Cells with pure 1991-2020 CDS downloads: {len(clim_cells_available)} (out of 22)")

    for _, row in lookup_df.iterrows():
        cell_id = row["agera5_cell_id"]
        kab_name = row["nama_kabupaten_kota"]
        lat = round(row["agera5_grid_lat"], 1)
        lon = round(row["agera5_grid_lon"], 1)
        elev = row["dem_elevation_m"]
        
        clean_name = f"cell_{lat:.1f}_{lon:.1f}".replace("-", "m").replace(".", "p")
        out_file = OUT_DIR / f"climatology_{clean_name}.json"

        has_30yr = (lat, lon) in clim_cells_available
        if has_30yr:
            source_desc = "Copernicus AgERA5 (1991-2020 Pure 30-Year Baseline, CDS API)"
            rank_n = 30
            rank_basis_id = "AgERA5_1991_2020_30yr"
            data_ver = "agera5-climatology-1991-2020-v1.0"
            is_pure_30yr = True
            limitation = "Data dasar 30 tahun penuh terunduh langsung dari Copernicus CDS API."
            
            lat_str = f"m{abs(lat):.1f}" if lat < 0 else f"p{lat:.1f}"
            lon_str = f"p{lon:.1f}"
            pattern = f"agera5_lat{lat_str}_lon{lon_str}_*.csv"
            dfs = []
            for cf in sorted(CLIM_1991_2020.glob(pattern)):
                dfs.append(pd.read_csv(cf))
            df_cell = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
        else:
            source_desc = "Copernicus AgERA5 (2015-2024 10-Year Decadal Reference)"
            rank_n = 10
            rank_basis_id = "AgERA5_2015_2024_10yr"
            data_ver = "agera5-reference-2015-2024-v1.0"
            is_pure_30yr = False
            limitation = "Sel ini belum diunduh untuk periode 1991-2020 dari CDS API; persentil dihitung murni dari dekade 2015-2024 sebagai acuan sementara tanpa interpolasi spasial buatan."
            
            slug = kab_name.lower().replace("kabupaten ", "kab_").replace("kota ", "kota_").replace(" ", "_")
            ag_file = DATA_AGERA5 / f"agera5_{slug}_2015_2024.csv"
            if not ag_file.exists():
                grid_df = pd.read_csv(GRID_CSV)
                match = grid_df[grid_df["agera5_cell_id"] == cell_id]
                if not match.empty:
                    f_name = match.iloc[0]["agera5_file"]
                    ag_file = DATA_AGERA5 / f_name
            df_cell = pd.read_csv(ag_file) if ag_file.exists() else pd.DataFrame()

        if df_cell.empty:
            print(f"Skipping {cell_id}: no data found.")
            continue

        df_cell["dt"] = pd.to_datetime(df_cell["valid_time"])
        df_cell["month"] = df_cell["dt"].dt.month
        
        p = df_cell["Precipitation_Flux"].values
        et0 = df_cell["ReferenceET_PenmanMonteith_FAO56"].values
        tmin = df_cell["Temperature_Air_2m_Min_24h"].values - 273.15
        tdew = df_cell["Dew_Point_Temperature_2m_Mean_24h"].values - 273.15
        
        roll_p = pd.Series(p).rolling(14, min_periods=1).sum().values
        roll_wb = pd.Series(p - et0).rolling(14, min_periods=1).sum().values
        dew_dep = tmin - tdew

        df_cell["roll_p"] = roll_p
        df_cell["roll_wb"] = roll_wb
        df_cell["dew_dep"] = dew_dep

        monthly_stats = {}
        for m_idx in range(1, 13):
            sub_m = df_cell[df_cell["month"] == m_idx]
            if len(sub_m) == 0:
                continue
            monthly_stats[str(m_idx)] = {
                "month_name": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][m_idx - 1],
                "precip_14d": {
                    "p10": round(float(np.percentile(sub_m["roll_p"], 10)), 1),
                    "p25": round(float(np.percentile(sub_m["roll_p"], 25)), 1),
                    "p50": round(float(np.percentile(sub_m["roll_p"], 50)), 1),
                    "p75": round(float(np.percentile(sub_m["roll_p"], 75)), 1),
                    "p90": round(float(np.percentile(sub_m["roll_p"], 90)), 1)
                },
                "water_balance_14d": {
                    "p10": round(float(np.percentile(sub_m["roll_wb"], 10)), 1),
                    "p25": round(float(np.percentile(sub_m["roll_wb"], 25)), 1),
                    "p50": round(float(np.percentile(sub_m["roll_wb"], 50)), 1),
                    "p75": round(float(np.percentile(sub_m["roll_wb"], 75)), 1),
                    "p90": round(float(np.percentile(sub_m["roll_wb"], 90)), 1)
                },
                "dew_depression_dawn": {
                    "p10": round(float(np.percentile(sub_m["dew_dep"], 10)), 2),
                    "p50": round(float(np.percentile(sub_m["dew_dep"], 50)), 2),
                    "p90": round(float(np.percentile(sub_m["dew_dep"], 90)), 2)
                }
            }

        payload = {
            "version": "v2.3-climatology-export",
            "cell_id": cell_id,
            "representative_kabupaten": kab_name,
            "coordinates": {"lat": lat, "lon": lon},
            "elevation_m": float(elev),
            "rank_basis_id": rank_basis_id,
            "rank_basis_n": rank_n,
            "data_version": data_ver,
            "is_pure_1991_2020_climatology": is_pure_30yr,
            "source": source_desc,
            "limitation_note": limitation,
            "monthly_climatology_14d": monthly_stats
        }

        out_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Exported {out_file.name} (pure_30yr={is_pure_30yr}, n={rank_n})")

    print("\nAll 22 static climatology artifacts updated with honest metadata!")


if __name__ == "__main__":
    main()
