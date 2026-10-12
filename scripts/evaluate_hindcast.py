"""Evaluate preregistered hindcast climate indicators across West Java cells."""
from __future__ import annotations

import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd

from project_paths import PROJECT_ROOT

DATA_DIR = PROJECT_ROOT / "data" / "raw" / "DS01_agera5"
OUT_JSON = PROJECT_ROOT / "reports" / "results" / "13_hindcast_validation.json"


def evaluate_cell_hindcast(df: pd.DataFrame) -> dict:
    df["dt"] = pd.to_datetime(df["valid_time"])
    df = df.sort_values("dt").reset_index(drop=True)

    # 1. Rolling 14-day precip
    precip = df["Precipitation_Flux"].values
    rolling_14d_precip = pd.Series(precip).rolling(14, min_periods=1).sum().values

    # 2. P - ET0
    et0 = df["ReferenceET_PenmanMonteith_FAO56"].values
    rolling_14d_water_balance = pd.Series(precip - et0).rolling(14, min_periods=1).sum().values

    # 3. CDD: consecutive days with precip < 1.0 mm
    dry_day = (precip < 1.0).astype(int)
    cdd = np.zeros(len(df), dtype=int)
    current_run = 0
    for i, d in enumerate(dry_day):
        if d == 1:
            current_run += 1
        else:
            current_run = 0
        cdd[i] = current_run

    df["rolling_14d_precip"] = rolling_14d_precip
    df["rolling_14d_water_bal"] = rolling_14d_water_balance
    df["cdd"] = cdd

    # Background distributions over 2015-2024
    p75_rolling_precip = np.percentile(rolling_14d_precip, 75)
    p25_rolling_precip = np.percentile(rolling_14d_precip, 25)
    p75_cdd = np.percentile(cdd, 75)
    p25_cdd = np.percentile(cdd, 25)
    p25_wb = np.percentile(rolling_14d_water_balance, 25)
    p75_wb = np.percentile(rolling_14d_water_balance, 75)

    # Event 1: HC_2016_WET (Oct-Dec 2016)
    sub_2016 = df[(df["dt"].dt.year == 2016) & (df["dt"].dt.month.isin([10, 11, 12]))]
    wet_hit = (
        (sub_2016["rolling_14d_precip"].mean() > p75_rolling_precip) or
        (sub_2016["rolling_14d_water_bal"].mean() > p75_wb) or
        (sub_2016["cdd"].mean() < p25_cdd)
    )

    # Event 2: HC_2019_DRY (Jun-Oct 2019)
    sub_2019 = df[(df["dt"].dt.year == 2019) & (df["dt"].dt.month.isin([6, 7, 8, 9, 10]))]
    dry_2019_hit = (
        (sub_2019["cdd"].max() > p75_cdd) and
        (sub_2019["rolling_14d_precip"].mean() < p25_rolling_precip)
    )

    # Event 3: HC_2023_DRY (Jun-Nov 2023)
    sub_2023 = df[(df["dt"].dt.year == 2023) & (df["dt"].dt.month.isin([6, 7, 8, 9, 10, 11]))]
    dry_2023_hit = (
        (sub_2023["cdd"].max() > p75_cdd) and
        (sub_2023["rolling_14d_precip"].mean() < p25_rolling_precip)
    )

    return {
        "HC_2016_WET": "HIT" if wet_hit else "MISS",
        "HC_2019_DRY": "HIT" if dry_2019_hit else "MISS",
        "HC_2023_DRY": "HIT" if dry_2023_hit else "MISS",
    }


def main() -> None:
    files = sorted(list(DATA_DIR.glob("agera5_kab_*.csv")))
    if not files:
        print("No kab files found.")
        return

    results = []
    hits = {"HC_2016_WET": 0, "HC_2019_DRY": 0, "HC_2023_DRY": 0}

    for f in files:
        name = f.stem.replace("agera5_kab_", "").replace("_2015_2024", "")
        df = pd.read_csv(f)
        eval_res = evaluate_cell_hindcast(df)
        results.append({"kab": name, **eval_res})
        for k in hits:
            if eval_res[k] == "HIT":
                hits[k] += 1

    total_units = len(results)
    summary = {
        "status": "COMPLETED",
        "reference_plan": "docs/hindcast_plan.md",
        "preregistered_commit": "c515e27",
        "total_units_evaluated": total_units,
        "event_results": {
            "HC_2016_WET": {
                "hits": hits["HC_2016_WET"],
                "misses": total_units - hits["HC_2016_WET"],
                "hit_rate_pct": round(hits["HC_2016_WET"] / total_units * 100, 1),
            },
            "HC_2019_DRY": {
                "hits": hits["HC_2019_DRY"],
                "misses": total_units - hits["HC_2019_DRY"],
                "hit_rate_pct": round(hits["HC_2019_DRY"] / total_units * 100, 1),
            },
            "HC_2023_DRY": {
                "hits": hits["HC_2023_DRY"],
                "misses": total_units - hits["HC_2023_DRY"],
                "hit_rate_pct": round(hits["HC_2023_DRY"] / total_units * 100, 1),
            },
        },
        "per_unit_results": results,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote hindcast validation results to {OUT_JSON}")
    print(f"Summary: {summary['event_results']}")


if __name__ == "__main__":
    main()
