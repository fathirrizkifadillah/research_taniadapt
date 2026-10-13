"""Generate golden test vectors from Python FAO-56 pipeline for Vitest parity testing."""
from __future__ import annotations

import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "mechanistic"))

from fao56 import (
    daily_et0,
    validate_fao56_example18,
    calculate_dynamic_kc,
    calculate_taw_raw,
    evaluate_fao56_water_stress,
    CROP_PARAMS_TABLE12_22
)

OUT_FILE = PROJECT_ROOT / "tests" / "golden_engine_vectors.json"


def main():
    # 1. ET0 Example 18
    ex18_val = validate_fao56_example18()
    
    # 2. Daily ET0 tropical test vectors
    # Day 1: Subang rainy season
    et0_subang_rainy = daily_et0(
        tmax_c=31.5, tmin_c=23.2, dewpoint_c=22.8, wind_10m_ms=2.1,
        solar_radiation_mj_m2_day=18.5, elevation_m=25.0,
        latitude_deg=-6.5, day_of_year=45
    )
    # Day 2: Subang dry season (El Nino)
    et0_subang_dry = daily_et0(
        tmax_c=34.8, tmin_c=22.0, dewpoint_c=19.5, wind_10m_ms=3.8,
        solar_radiation_mj_m2_day=23.4, elevation_m=25.0,
        latitude_deg=-6.5, day_of_year=240
    )
    # Day 3: Lembang highland
    et0_lembang = daily_et0(
        tmax_c=24.5, tmin_c=15.2, dewpoint_c=14.8, wind_10m_ms=1.8,
        solar_radiation_mj_m2_day=17.0, elevation_m=1250.0,
        latitude_deg=-6.8, day_of_year=180
    )

    # 3. Dynamic Kc vectors across stages
    kc_vectors = []
    crops = ["jagung", "kedelai", "tomat", "padi"]
    daps = [5, 15, 25, 45, 65, 80, 100, 120]
    for c in crops:
        for d in daps:
            kc_val = calculate_dynamic_kc(c, d)
            kc_vectors.append({
                "crop": c,
                "dap": d,
                "kc": round(kc_val, 4)
            })

    # 4. TAW and RAW across soils and crops
    water_balance_vectors = []
    for c in ["jagung", "kedelai", "tomat"]:
        for dap in [20, 60, 90]:
            for soil in ["loam", "sandy_loam", "clay"]:
                wb = calculate_taw_raw(c, dap, soil)
                # Test stress at various Dr
                eval_safe = evaluate_fao56_water_stress(c, dap, depletion_dr_mm=wb["raw_mm"] * 0.5, soil_type=soil)
                eval_stress = evaluate_fao56_water_stress(c, dap, depletion_dr_mm=wb["raw_mm"] + 5.0, soil_type=soil)
                water_balance_vectors.append({
                    "crop": c,
                    "dap": dap,
                    "soil": soil,
                    "taw_mm": wb["taw_mm"],
                    "raw_mm": wb["raw_mm"],
                    "root_depth_m": wb["root_depth_m"],
                    "eval_safe_status": eval_safe["status"],
                    "eval_stress_status": eval_stress["status"]
                })

    payload = {
        "generator": "scripts/mechanistic/fao56.py",
        "reference": "FAO Irrigation and Drainage Paper 56",
        "et0_example18": {
            "expected_mm_day": 3.88,
            "calculated_mm_day": round(ex18_val, 4),
            "tolerance": 0.03
        },
        "et0_tropical_samples": [
            {
                "label": "subang_rainy",
                "inputs": {
                    "tmax_c": 31.5, "tmin_c": 23.2, "dewpoint_c": 22.8, "wind_10m_ms": 2.1,
                    "solar_radiation_mj_m2_day": 18.5, "elevation_m": 25.0,
                    "latitude_deg": -6.5, "day_of_year": 45
                },
                "expected_et0": round(et0_subang_rainy, 4)
            },
            {
                "label": "subang_dry",
                "inputs": {
                    "tmax_c": 34.8, "tmin_c": 22.0, "dewpoint_c": 19.5, "wind_10m_ms": 3.8,
                    "solar_radiation_mj_m2_day": 23.4, "elevation_m": 25.0,
                    "latitude_deg": -6.5, "day_of_year": 240
                },
                "expected_et0": round(et0_subang_dry, 4)
            },
            {
                "label": "lembang_highland",
                "inputs": {
                    "tmax_c": 24.5, "tmin_c": 15.2, "dewpoint_c": 14.8, "wind_10m_ms": 1.8,
                    "solar_radiation_mj_m2_day": 17.0, "elevation_m": 1250.0,
                    "latitude_deg": -6.8, "day_of_year": 180
                },
                "expected_et0": round(et0_lembang, 4)
            }
        ],
        "kc_vectors": kc_vectors,
        "water_balance_vectors": water_balance_vectors
    }

    OUT_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Generated {OUT_FILE}")


if __name__ == "__main__":
    main()
