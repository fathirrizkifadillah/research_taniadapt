"""Create the conservative mechanistic-parameter registry for TaniAdapt."""
from __future__ import annotations

import json
from pathlib import Path

from fao56 import validate_fao56_example18

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "results" / "12_mechanistic_params.json"


def main() -> None:
    example18 = validate_fao56_example18()
    result = {
        "status": "PARTIAL_READY",
        "scope": "Reference ET0 and verified Kc only; no crop stress, yield, or disease prediction.",
        "katam": {
            "status": "CANNOT_ACCESS",
            "finding": "Official Kementan repository pages for Katam and SI-Katam are open, but no current machine-downloadable Jabar kecamatan calendar was obtained in this run.",
            "available_documentation": [
                "https://repository.pertanian.go.id/items/fc16d362-f359-4d8a-960d-a05261362348/full",
                "https://repository.pertanian.go.id/items/98a55545-8dfc-4580-87ee-6480bc67e53f/full",
            ],
            "license": "UNVERIFIED",
            "engine_use": "No planting calendar inferred; crop phase is evidence_insufficient."
        },
        "et0": {
            "evidence_id": "FAO56_ET0_PM",
            "method": "FAO-56 Penman–Monteith daily implementation",
            "inputs": ["Tmax", "Tmin", "dewpoint", "10m wind converted to 2m", "solar radiation", "elevation", "latitude", "day of year"],
            "daily_soil_heat_flux": 0,
            "validation": {"source": "FAO-56 Example 18, Chapter 4", "expected_mm_day": 3.88, "computed_mm_day": round(example18, 3), "status": "PASS"},
            "agera5_note": "AgERA5 already includes a ReferenceET_PenmanMonteith_FAO56 field. The independent implementation is retained for traceability and comparison, not silently substituted."
        },
        "kc_parameters": [
            {"crop": "padi", "evidence_id": "FAO56_KC_RICE", "kc_ini": 1.05, "kc_mid": 1.20, "kc_end": [0.90, 0.60], "source_page": "FAO-56 Table 12, p. 110"},
            {"crop": "jagung", "evidence_id": "FAO56_KC_MAIZE", "kc_ini": 0.30, "kc_mid": 1.20, "kc_end": [0.60, 0.35], "source_page": "FAO-56 Table 12, p. 110"},
            {"crop": "kedelai", "evidence_id": "FAO56_KC_SOY", "kc_ini": 0.40, "kc_mid": 1.15, "kc_end": 0.50, "source_page": "FAO-56 Table 12, p. 110"},
            {"crop": "tomat", "evidence_id": "FAO56_KC_TOMATO", "kc_ini": 0.60, "kc_mid": 1.15, "kc_end": [0.70, 0.90], "source_page": "FAO-56 Table 12, p. 110"},
        ],
        "gdd": {"status": "evidence_insufficient", "reason": "No crop- and phase-specific base-temperature record is VERIFIED in evidence_registry.csv; no base temperature is inserted."}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
