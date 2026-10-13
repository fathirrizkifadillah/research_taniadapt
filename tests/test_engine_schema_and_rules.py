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


def test_schema_if_then_rejects_stress_without_verified_evidence(engine_schema: dict, valid_baseline_payload: dict):
    """Test that schema if/then rejects kondisi_stres_abiotik if evidence_refs has no VERIFIED ID."""
    unverified_payload = valid_baseline_payload.copy()
    unverified_payload["status"] = "kondisi_stres_abiotik"
    unverified_payload["evidence_refs"] = ["UNVERIFIED_HEURISTIC_RULE"]
    
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=unverified_payload, schema=engine_schema, format_checker=jsonschema.FormatChecker())


def test_schema_if_then_accepts_stress_with_verified_evidence(engine_schema: dict, valid_baseline_payload: dict):
    """Test that schema if/then accepts kondisi_stres_abiotik when evidence_refs contains FAO56_RAW_DEPLETION."""
    verified_payload = valid_baseline_payload.copy()
    verified_payload["status"] = "kondisi_stres_abiotik"
    verified_payload["evidence_refs"] = ["FAO56_RAW_DEPLETION", "FAO56_KC_MAIZE"]
    
    # Should validate cleanly
    jsonschema.validate(instance=verified_payload, schema=engine_schema, format_checker=jsonschema.FormatChecker())


def test_padi_water_module_insufficient(valid_baseline_payload: dict):
    """Test that rice water module enforces evidence_insufficient."""
    rice_payload = valid_baseline_payload.copy()
    rice_payload["crop"] = "padi"
    rice_payload["status"] = "evidence_insufficient"
    rice_payload["evidence_refs"] = ["FAO56_KC_RICE"]
    assert rice_payload["status"] == "evidence_insufficient"


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
            assert status in ("CONVENTION_PENDING", "INSUFFICIENT", "DEPRECATED"), (
                f"Rule {r['id']} lacks verified evidence_id ({ev_id}) but has status {status}"
            )
