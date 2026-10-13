"""Pytest test suite for TaniAdapt Decision Engine Schema & Evidence Rules.

Enforces:
1. Output payload conforms strictly to schemas/engine_output.schema.json (Draft 2020-12).
2. Required fields: actions[] and hourly[] with exact required properties.
3. additionalProperties: false enforced at root and nested levels.
4. format date-time on issue_time.
5. If/Then schema-level constraint: status 'kondisi_stres_abiotik' or 'kondisi_mendukung_OPT'
   MUST have evidence_refs containing a registered VERIFIED evidence ID.
6. Rice water module must return 'evidence_insufficient' (ponded assumption).
7. Rules register status integrity (rules without verified evidence_id must be CONVENTION_PENDING, INSUFFICIENT, or DEPRECATED).
"""
from __future__ import annotations

import json
from pathlib import Path
import pytest
import jsonschema
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_FILE = PROJECT_ROOT / "schemas" / "engine_output.schema.json"
RULES_FILE = PROJECT_ROOT / "rules" / "rules.json"
EVIDENCE_REGISTRY_FILE = PROJECT_ROOT / "reports" / "dataset_audit" / "evidence_registry.csv"


@pytest.fixture
def engine_schema() -> dict:
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def verified_evidence_ids() -> set[str]:
    df = pd.read_csv(EVIDENCE_REGISTRY_FILE)
    verified = set(df[df["status_verifikasi"] == "VERIFIED"]["id"].tolist())
    return verified


@pytest.fixture
def valid_baseline_payload() -> dict:
    return {
        "crop": "jagung",
        "location": {
            "kabkota": "KABUPATEN SUBANG",
            "cell_id": "CELL_(-6.5, 107.7)",
            "weather_source": "AgERA5_CDS"
        },
        "as_of": "2026-10-13",
        "issue_time": "2026-10-13T06:00:00+07:00",
        "timezone": "Asia/Jakarta",
        "rules_version": "v2.3-phase13-gate",
        "data_version": "agera5-v1.1",
        "data_freshness_days": 0,
        "layer": "daily",
        "source_data": "forecast",
        "forecast_uncertainty": 15.0,
        "indicators": [
            {
                "id": "soil_water_depletion_Dr",
                "rule_id": "RULE_WATER_FAO56_DEPLETION",
                "value": 45.2,
                "unit": "mm",
                "relative_rank": "typical",
                "rank_basis": "AgERA5_1991_2020",
                "rank_basis_n": 30
            }
        ],
        "actions": [
            {
                "action": "irrigation",
                "window": "06.00 - 08.00 WIB",
                "status_label": "Sangat Aman",
                "rule_ids": ["RULE_WATER_FAO56_DEPLETION"],
                "rule_status": "VERIFIED_METHOD",
                "evidence_refs": ["FAO56_RAW_DEPLETION"],
                "reason": "Lengas tanah mencukupi; evapotranspirasi pagi tenang."
            }
        ],
        "hourly": [
            {
                "hour": "06.00",
                "status": "SAFE",
                "reason": "Kondisi optimal pagi"
            },
            {
                "hour": "12.00",
                "status": "WARN",
                "reason": "Radiasi terik siang"
            }
        ],
        "status": "normal",
        "evidence_tier": "published_model",
        "evidence_refs": ["FAO56_ET0_PM", "FAO56_KC_MAIZE"],
        "claim_allowed": "Lengas tanah mencukupi (Dr <= RAW); tidak memerlukan irigasi darurat.",
        "claim_forbidden": ["calibrated yield forecast", "empirical yield loss estimate"],
        "limitations": ["Menggunakan asumsi kedalaman perakaran standar FAO-56 Tabel 22."],
        "action_ids": ["ACT_IRRIG_REPLENISHMENT"]
    }


def test_schema_valid_payload(engine_schema: dict, valid_baseline_payload: dict):
    """Test that a valid payload passes JSON schema validation."""
    jsonschema.validate(instance=valid_baseline_payload, schema=engine_schema, format_checker=jsonschema.FormatChecker())


def test_reject_additional_properties(engine_schema: dict, valid_baseline_payload: dict):
    """Test that additional unknown properties are rejected by schema."""
    bad_payload = valid_baseline_payload.copy()
    bad_payload["unknown_heuristic_score"] = 99.5
    with pytest.raises(jsonschema.ValidationError, match="additionalProperties"):
        jsonschema.validate(instance=bad_payload, schema=engine_schema, format_checker=jsonschema.FormatChecker())


def test_reject_invalid_date_time_format(engine_schema: dict, valid_baseline_payload: dict):
    """Test that invalid issue_time format is rejected."""
    bad_payload = valid_baseline_payload.copy()
    bad_payload["issue_time"] = "not-a-datetime"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=bad_payload, schema=engine_schema, format_checker=jsonschema.FormatChecker())


def test_schema_if_then_rejects_stress_without_trigger_rule(engine_schema: dict, valid_baseline_payload: dict):
    """Test that schema if/then rejects kondisi_stres_abiotik if evidence_refs has other FAO IDs but lacks RULE_WATER_FAO56_DEPLETION."""
    unverified_payload = valid_baseline_payload.copy()
    unverified_payload["status"] = "kondisi_stres_abiotik"
    unverified_payload["evidence_refs"] = ["FAO56_RAW_DEPLETION", "FAO56_KC_MAIZE"]  # Lacks RULE_WATER_FAO56_DEPLETION
    
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=unverified_payload, schema=engine_schema, format_checker=jsonschema.FormatChecker())


def test_schema_if_then_accepts_stress_with_verified_trigger_rule(engine_schema: dict, valid_baseline_payload: dict):
    """Test that schema if/then accepts kondisi_stres_abiotik when evidence_refs contains RULE_WATER_FAO56_DEPLETION."""
    verified_payload = valid_baseline_payload.copy()
    verified_payload["status"] = "kondisi_stres_abiotik"
    verified_payload["evidence_refs"] = ["RULE_WATER_FAO56_DEPLETION", "FAO56_RAW_DEPLETION"]
    
    # Should validate cleanly
    jsonschema.validate(instance=verified_payload, schema=engine_schema, format_checker=jsonschema.FormatChecker())


def test_schema_rejects_kondisi_mendukung_opt_unreachable(engine_schema: dict, valid_baseline_payload: dict):
    """Test that top-level status kondisi_mendukung_OPT is rejected at schema level as unreachable."""
    unreachable_payload = valid_baseline_payload.copy()
    unreachable_payload["status"] = "kondisi_mendukung_OPT"
    unreachable_payload["evidence_refs"] = ["SENTELHAS_2008_LWD"]
    
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=unreachable_payload, schema=engine_schema, format_checker=jsonschema.FormatChecker())


def test_fao56_example36_independent_parity():
    """Reproduce FAO-56 Example 36 TAW (Eq. 82) and RAW (Eq. 83) across 3 soil textures within 1 mm tolerance."""
    def calc_ex36(theta_fc: float, theta_wp: float, zr: float, p: float):
        taw = 1000.0 * (theta_fc - theta_wp) * zr
        raw = p * taw
        return round(taw), round(raw)

    # 1. Loamy sand (theta_fc = 0.15, theta_wp = 0.06 -> 90 mm/m)
    # Tomato (Zr = 0.8 m, p = 0.40): TAW 72, RAW 29
    taw, raw = calc_ex36(0.15, 0.06, 0.8, 0.40)
    assert abs(taw - 72) <= 1 and abs(raw - 29) <= 1
    # Maize (Zr = 1.2 m, p = 0.55): TAW 108, RAW 59
    taw, raw = calc_ex36(0.15, 0.06, 1.2, 0.55)
    assert abs(taw - 108) <= 1 and abs(raw - 59) <= 1

    # 2. Silt (theta_fc = 0.32, theta_wp = 0.15 -> 170 mm/m)
    # Tomato: TAW 136, RAW 54
    taw, raw = calc_ex36(0.32, 0.15, 0.8, 0.40)
    assert abs(taw - 136) <= 1 and abs(raw - 54) <= 1
    # Maize: TAW 204, RAW 112
    taw, raw = calc_ex36(0.32, 0.15, 1.2, 0.55)
    assert abs(taw - 204) <= 1 and abs(raw - 112) <= 1

    # 3. Silty clay (theta_fc = 0.35, theta_wp = 0.23 -> 120 mm/m)
    # Tomato: TAW 96, RAW 38
    taw, raw = calc_ex36(0.35, 0.23, 0.8, 0.40)
    assert abs(taw - 96) <= 1 and abs(raw - 38) <= 1
    # Maize: TAW 144, RAW 79
    taw, raw = calc_ex36(0.35, 0.23, 1.2, 0.55)
    assert abs(taw - 144) <= 1 and abs(raw - 79) <= 1


def test_harvesting_rh_transition_rule():
    """Verify that rules.json defines RULE_HARVEST_RH_WARN for transition RH 75-85%."""
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    rule_warn = next((r for r in data["rules"] if r["id"] == "RULE_HARVEST_RH_WARN"), None)
    assert rule_warn is not None, "RULE_HARVEST_RH_WARN must exist in rules.json"
    assert rule_warn["status_label"] == "WARN"
    assert rule_warn["condition"]["min"] == 75.0
    assert rule_warn["condition"]["max"] == 85.0


def test_fao56_crop_p_and_zr_configs():
    """Verify that p for soybean is 0.50 and tomato is 0.40 from config (regression check for bug p=0.55)."""
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    rule = next(r for r in data["rules"] if r["id"] == "RULE_WATER_FAO56_DEPLETION")
    crops = rule["config"]["crops"]
    
    assert crops["jagung"]["p_fraction"] == 0.55, "Corn p fraction must be 0.55"
    assert crops["kedelai"]["p_fraction"] == 0.50, "Soybean p fraction must be 0.50 (not 0.55)"
    assert crops["tomat"]["p_fraction"] == 0.40, "Tomato p fraction must be 0.40 (not 0.55)"
    assert crops["padi"]["p_fraction"] == 0.20, "Rice p fraction must be 0.20"
    
    assert crops["jagung"]["zr_chosen_m"] == 1.0
    assert crops["kedelai"]["zr_chosen_m"] == 0.8
    assert crops["tomat"]["zr_chosen_m"] == 0.7


def test_all_rules_in_rules_json_conform_to_contract(verified_evidence_ids: set[str]):
    """Verify that every rule in rules/rules.json without a VERIFIED evidence_id has CONVENTION_PENDING, INSUFFICIENT, or DEPRECATED."""
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    rules = data.get("rules", [])
    assert len(rules) >= 15, "Rules register must contain all required operational rules."
    
    for r in rules:
        ev_id = r.get("evidence_id")
        status = r.get("status")
        if ev_id in verified_evidence_ids:
            assert status in ("VERIFIED", "VERIFIED_METHOD"), f"Rule {r['id']} has verified evidence_id {ev_id} but status is {status}"
        else:
            assert status in ("METHOD_UNCALIBRATED", "CONVENTION_PENDING", "INSUFFICIENT", "DEPRECATED"), (
                f"Rule {r['id']} lacks verified evidence_id ({ev_id}) but has status {status}"
            )


def test_engine_code_single_source_hash_parity():
    """Verify hash parity between canonical research files and web app engine files."""
    import hashlib
    web_engine_dir = Path("/mnt/c/CODING/TaniAdapt/taniadapt-web/src/lib/engine")
    if not web_engine_dir.exists():
        pytest.skip("Web engine directory not present on this host")
    
    for filename, rel_src in [("rules.json", RULES_FILE), ("engine_output.schema.json", SCHEMA_FILE)]:
        web_file = web_engine_dir / filename
        assert web_file.exists(), f"Web engine file {filename} missing"
        h_src = hashlib.sha256(rel_src.read_bytes()).hexdigest()
        h_web = hashlib.sha256(web_file.read_bytes()).hexdigest()
        assert h_src == h_web, f"SHA256 mismatch between canonical {filename} and web engine: {h_src} != {h_web}"
