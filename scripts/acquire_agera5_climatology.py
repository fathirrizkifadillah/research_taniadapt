"""Acquire the AgERA5 baseline, one calendar year and one unique cell per request.

Credentials are read only by cdsapi from its configured secure location. This script
never prints configuration, tokens, request headers, or credential values.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cdsapi
import pandas as pd

from project_paths import PROJECT_ROOT

GRID = PROJECT_ROOT / "reports" / "dataset_audit" / "a8_spatial_grid_cells_audit.csv"
OUT = PROJECT_ROOT / "data" / "raw" / "DS01_agera5_climatology_1991_2020"
LOG = PROJECT_ROOT / "reports" / "logs" / "agera5_climatology_acquisition.json"
DATASET = "sis-agrometeorological-indicators-timeseries"
VARIABLES = [
    "10m_wind_speed_24_hour_mean", "2m_dewpoint_temperature_24_hour_mean",
    "2m_relative_humidity_at_06_00", "2m_relative_humidity_at_09_00",
    "2m_relative_humidity_at_12_00", "2m_relative_humidity_at_15_00",
    "2m_relative_humidity_at_18_00", "2m_temperature_24_hour_maximum",
    "2m_temperature_24_hour_mean", "2m_temperature_24_hour_minimum",
    "derived_2m_relative_humidity_24_hour_maximum",
    "derived_2m_relative_humidity_24_hour_minimum", "precipitation_flux",
    "reference_evapotranspiration", "solar_radiation_flux",
    "vapour_pressure_24_hour_mean", "vapour_pressure_deficit_at_maximum_temperature",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1991)
    parser.add_argument("--end", type=int, default=2020)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    cells = pd.read_csv(GRID).drop_duplicates("agera5_cell_id").copy()
    OUT.mkdir(parents=True, exist_ok=True)
    log = {"dataset": DATASET, "cells": int(len(cells)), "years": [args.start, args.end],
           "quota_check": "CANNOT_ACCESS_PERSONAL_QUOTA_VIA_CDSAPI", "requests": []}
    try:
        client = cdsapi.Client(quiet=True, timeout=120, progress=False)
        # CDS status exposes service status. It does not expose a personal quota API.
        status = client.status()
        log["service_status_check"] = "OK" if isinstance(status, dict) else "UNEXPECTED_RESPONSE"
    except Exception as exc:
        log["service_status_check"] = "FAILED"
        log["status_error_type"] = type(exc).__name__
        LOG.parent.mkdir(parents=True, exist_ok=True)
        LOG.write_text(json.dumps(log, indent=2), encoding="utf-8")
        print("CDS status check failed; see acquisition log. No credential data was written.")
        return
    if args.check_only:
        LOG.write_text(json.dumps(log, indent=2), encoding="utf-8")
        print("CDS service reachable. Personal quota is not exposed by this client API.")
        return

    for _, cell in cells.iterrows():
        cell_key = f"lat{cell.agera5_grid_lat:+.1f}_lon{cell.agera5_grid_lon:+.1f}".replace("+", "p").replace("-", "m")
        for year in range(args.start, args.end + 1):
            target = OUT / f"agera5_{cell_key}_{year}.csv"
            entry = {"cell_id": cell.agera5_cell_id, "year": year, "target": str(target.relative_to(PROJECT_ROOT))}
            if target.exists() and target.stat().st_size > 1000:
                entry["status"] = "EXISTS"
                log["requests"].append(entry)
                continue
            try:
                # An epsilon box requests the audited nearest grid point while keeping
                # north/west/south/east ordering explicit for the CDS request.
                lat, lon = float(cell.agera5_grid_lat), float(cell.agera5_grid_lon)
                client.retrieve(DATASET, {
                    "variable": VARIABLES, "data_format": "csv",
                    "date": f"{year}-01-01/{year}-12-31",
                    "area": [lat + 0.0001, lon - 0.0001, lat - 0.0001, lon + 0.0001],
                }, str(target))
                entry["status"] = "DOWNLOADED" if target.exists() else "NO_FILE"
            except Exception as exc:
                entry["status"] = "FAILED"
                entry["error_type"] = type(exc).__name__
                # Exception text can contain server/request detail. Keep only its type.
            log["requests"].append(entry)
            LOG.write_text(json.dumps(log, indent=2), encoding="utf-8")
    LOG.write_text(json.dumps(log, indent=2), encoding="utf-8")
    counts = pd.Series([x["status"] for x in log["requests"]]).value_counts().to_dict()
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main()
