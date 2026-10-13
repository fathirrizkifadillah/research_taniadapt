"""Create the conservative mechanistic-parameter registry for TaniAdapt."""
from __future__ import annotations

import json
from pathlib import Path

from fao56 import (
    validate_fao56_example18,
    SOIL_TEXTURE_TABLE19,
    CROP_STAGES_TABLE11,
    CROP_PARAMS_TABLE12_22
)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "results" / "12_mechanistic_params.json"


def main() -> None:
    example18 = validate_fao56_example18()
    result = {
        "status": "MECHANISTIC_FRAMEWORK_VERIFIED",
        "scope": "Reference ET0, verified Kc stages, and FAO-56 root zone depletion (RAW = p * TAW); no empirical yield or unverified disease prediction.",
        "katam": {
            "status": "CANNOT_ACCESS",
            "finding": "Official Kementan repository pages for Katam and SI-Katam are open, but no current machine-downloadable Jabar kecamatan calendar was obtained in this run.",
            "available_documentation": [
                "https://repository.pertanian.go.id/items/fc16d362-f359-4d8a-960d-a05261362348/full",
                "https://repository.pertanian.go.id/items/98a55545-8dfc-4580-87ee-6480bc67e53f/full",
            ],
            "license": "UNVERIFIED",
            "engine_use": "No planting calendar inferred from katam; crop planting date is taken directly from user farm input."
        },
        "et0": {
            "evidence_id": "FAO56_ET0_PM",
            "method": "FAO-56 Penman-Monteith daily implementation",
            "citation_page": "FAO-56 Chapter 4, Eq. 6, p. 65",
            "inputs": ["Tmax", "Tmin", "dewpoint", "10m wind converted to 2m", "solar radiation", "elevation", "latitude", "day of year"],
            "daily_soil_heat_flux": 0,
            "validation": {
                "source": "FAO-56 Example 18, Chapter 4",
                "expected_mm_day": 3.88,
                "computed_mm_day": round(example18, 3),
                "status": "PASS"
            },
            "agera5_note": "AgERA5 already includes a ReferenceET_PenmanMonteith_FAO56 field. The independent implementation is retained for traceability and comparison, not silently substituted."
        },
        "crop_development_stages_table11": {
            "citation_page": "FAO-56 Chapter 6, Table 11, pp. 104-108",
            "stages_days": CROP_STAGES_TABLE11
        },
        "crop_coefficients_table12": {
            "citation_page": "FAO-56 Chapter 6, Table 12, pp. 109-114",
            "kc_parameters": [
                {"crop": "padi", "evidence_id": "FAO56_KC_RICE", "kc_ini": 1.05, "kc_mid": 1.20, "kc_end_table_range": [0.90, 0.60], "kc_end_adopted": 0.60, "assumption": "0.60 sawah dikeringkan pra-panen (atau 0.90 jika masih tergenang)", "source_page": "FAO-56 Table 12, p. 110"},
                {"crop": "jagung", "evidence_id": "FAO56_KC_MAIZE", "kc_ini": 0.30, "kc_mid": 1.20, "kc_end_table_range": [0.60, 0.35], "kc_end_adopted": 0.35, "assumption": "0.35 panen biji kering di batang (atau 0.60 jika panen basah)", "source_page": "FAO-56 Table 12, p. 110"},
                {"crop": "kedelai", "evidence_id": "FAO56_KC_SOY", "kc_ini": 0.40, "kc_mid": 1.15, "kc_end_table_range": [0.50, 0.50], "kc_end_adopted": 0.50, "assumption": "0.50 nilai tunggal panen polong kering", "source_page": "FAO-56 Table 12, p. 110"},
                {"crop": "tomat", "evidence_id": "FAO56_KC_TOMATO", "kc_ini": 0.60, "kc_mid": 1.15, "kc_end_table_range": [0.70, 0.90], "kc_end_adopted": 0.80, "assumption": "0.80 tomat segar (0.70 jika tomat olahan)", "source_page": "FAO-56 Table 12, p. 110"}
            ]
        },
        "soil_water_depletion_table19_22": {
            "evidence_id": "FAO56_RAW_DEPLETION",
            "method": "RAW = p * TAW, where TAW = 1000 * (theta_FC - theta_WP) * Zr",
            "citation_pages": "FAO-56 Chapter 8: Table 19 (p. 165) for soil moisture limits; Table 22 (pp. 167-168) for rooting depth Zr and depletion factor p.",
            "status": "VERIFIED",
            "soil_textures": SOIL_TEXTURE_TABLE19,
            "crop_root_depletion_factors": {
                "jagung": {"zr_range_m": [0.3, 1.2], "p": 0.55, "status": "VERIFIED"},
                "kedelai": {"zr_range_m": [0.3, 1.0], "p": 0.50, "status": "VERIFIED"},
                "tomat": {"zr_range_m": [0.25, 1.0], "p": 0.40, "status": "VERIFIED"},
                "padi": {"zr_range_m": [0.5, 1.0], "p": 0.20, "status": "evidence_insufficient", "reason": "Kc padi mengasumsikan sawah tergenang; deplesi RAW tidak berlaku."}
            }
        },
        "gdd": {
            "status": "evidence_insufficient",
            "reason": "No crop- and phase-specific base-temperature record is VERIFIED in evidence_registry.csv; no speculative base temperature is inserted into the engine."
        }
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
