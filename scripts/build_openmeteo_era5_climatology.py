"""Build unified 2000-2020 (21-year) ERA5 climatology from Open-Meteo Historical Archive API.

For all 27 Kabupaten/Kota in Jawa Barat:
- Fetches daily ERA5 precipitation, temperature, and dewpoint for 2000-2020 (21 years = 7,671 days).
- Computes monthly 14-day rolling percentiles (P10, P25, P50, P75, P90).
- Saves per-region JSON to data/export/openmeteo_era5_2000_2020_{slug}.json.
- Records CC BY 4.0 license and commercial terms in reports/results/15_openmeteo_climatology_summary.json.
"""
from __future__ import annotations

import json
import time
import urllib.request
import urllib.error
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOOKUP_CSV = PROJECT_ROOT / "data" / "processed" / "lookup_kab_cell_elev.csv"
OUT_DIR = PROJECT_ROOT / "data" / "export"
OUT_SUMMARY = PROJECT_ROOT / "reports" / "results" / "15_openmeteo_climatology_summary.json"


def fetch_openmeteo_21yr(lat: float, lon: float) -> pd.DataFrame:
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat:.4f}&longitude={lon:.4f}&"
        f"start_date=2000-01-01&end_date=2020-12-31&"
        f"daily=precipitation_sum,temperature_2m_mean,temperature_2m_min,dewpoint_2m_mean&"
        f"timezone=Asia%2FJakarta"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "TaniAdapt-Research-Climatology/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
            d = data.get("daily", {})
            df = pd.DataFrame({
                "valid_date": pd.to_datetime(d.get("time", [])),
                "precip": d.get("precipitation_sum", []),
                "tmean": d.get("temperature_2m_mean", []),
                "tmin": d.get("temperature_2m_min", []),
                "dew": d.get("dewpoint_2m_mean", [])
            })
            return df
        except Exception as e:
            time.sleep(1.5 * (attempt + 1))
    return pd.DataFrame()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df_lookup = pd.read_csv(LOOKUP_CSV)
    
    print(f"Processing 2000-2020 Open-Meteo ERA5 Climatology for {len(df_lookup)} kab/kota...")
    summaries = []

    for idx, row in df_lookup.iterrows():
        name = row["nama_kabupaten_kota"]
        slug = name.lower().replace("kabupaten ", "kab_").replace("kota ", "kota_").replace(" ", "_")
        lat = row["centroid_lat"]
        lon = row["centroid_lon"]
        elev = row["dem_elevation_m"]
        
        out_file = OUT_DIR / f"openmeteo_era5_2000_2020_{slug}.json"
        if out_file.exists():
            print(f"[{idx+1}/{len(df_lookup)}] Already exists: {out_file.name}")
            summaries.append({"kabupaten": name, "file": out_file.name, "status": "OK"})
            continue
        
        # Rate limit respect
        time.sleep(2.0)
        df_cell = fetch_openmeteo_21yr(lat, lon)
        if df_cell.empty:
            print(f"Failed to fetch {name}")
            continue

        df_cell["month"] = df_cell["valid_date"].dt.month
        # Rolling 14-day precipitation
        roll_p = df_cell["precip"].rolling(14, min_periods=1).sum().values
        # Climatic water balance proxy (P - ET0_mean_3.88)
        roll_wb = (df_cell["precip"] - 3.88).rolling(14, min_periods=1).sum().values
        dew_dep = df_cell["tmin"] - df_cell["dew"]

        df_cell["roll_p"] = roll_p
        df_cell["roll_wb"] = roll_wb
        df_cell["dew_dep"] = dew_dep

        monthly_stats = {}
        for m_idx in range(1, 13):
            sub_m = df_cell[df_cell["month"] == m_idx]
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
            "version": "v1.0-openmeteo-era5-2000-2020",
            "kabupaten_kota": name,
            "coordinates": {"lat": round(lat, 4), "lon": round(lon, 4)},
            "elevation_m": float(elev),
            "period": "2000-2020 (21 Years, N=7.671 days)",
            "source": "Open-Meteo Historical Archive API (ERA5 reanalysis model)",
            "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
            "monthly_climatology_14d": monthly_stats
        }

        out_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        summaries.append({"kabupaten": name, "file": out_file.name, "status": "OK"})
        print(f"[{idx+1}/{len(df_lookup)}] Exported {out_file.name}")

    summary_doc = {
        "status": "COMPLETED",
        "description": "21-Year ERA5 Baseline Climatology (2000-2020) for all 27 Kab/Kota Jawa Barat",
        "total_regions": len(summaries),
        "source": "Open-Meteo Historical Weather API (ERA5 model)",
        "period": "2000-2020 (7.671 days per location)",
        "license": {
            "non_commercial": "CC BY 4.0 with attribution 'Weather data by Open-Meteo.com'",
            "commercial": "Requires paid commercial license from Open-Meteo GmbH"
        },
        "regions": summaries
    }

    OUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    OUT_SUMMARY.write_text(json.dumps(summary_doc, indent=2), encoding="utf-8")
    print(f"Summary written to {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
