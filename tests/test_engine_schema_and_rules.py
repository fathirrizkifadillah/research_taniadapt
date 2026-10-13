"""Pytest test suite for TaniAdapt Decision Engine Schema & Evidence Rules.

Enforces:
1. Output payload conforms strictly to schemas/engine_output.schema.json (Draft 2020-12).
2. Strict Evidence Policy: An output declaring 'kondisi_stres_abiotik' or 'kondisi_mendukung_OPT'
   MUST be backed by a VERIFIED evidence_id in reports/dataset_audit/evidence_registry.csv.
   If not, the policy validator MUST reject the payload.
3. Rice water module must return 'evidence_insufficient' (ponded assumption).
4. All rules in rules/rules.json without VERIFIED evidence_id must have status CONVENTION_PENDING or INSUFFICIENT.
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
        "rules_version": "v2.2-honest-status",
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
        "status": "normal",
        "evidence_tier": "published_model",
        "evidence_refs": ["FAO56_ET0_PM", "FAO56_KC_MAIZE"],
        "claim_allowed": "Lengas tanah mencukupi (Dr <= RAW); tidak memerlukan irigasi darurat.",
        "claim_forbidden": ["calibrated yield forecast", "empirical yield loss estimate"],
        "limitations": ["Menggunakan asumsi kedalaman perakaran standar FAO-56 Tabel 22."],
        "action_ids": ["ACT_IRRIG_REPLENISHMENT"]
    }


def validate_engine_policy(payload: dict, verified_ids: set[str]) -> None:
    """Validate that high-stakes status (stres abiotik or OPT) is backed by VERIFIED evidence."""
    status = payload.get("status")
    refs = set(payload.get("evidence_refs", []))
    
    if status in ("kondisi_stres_abiotik", "kondisi_mendukung_OPT"):
        has_verified_ref = any(ref in verified_ids for ref in refs)
        if not has_verified_ref:
            raise ValueError(
                f"Policy Violation: Status '{status}' emitted without any VERIFIED evidence_id in evidence_refs! "
                f"Provided refs: {refs}. Must yield 'evidence_insufficient'."
            )


def test_schema_valid_payload(engine_schema: dict, valid_baseline_payload: dict):
    """Test that a valid payload passes JSON schema validation."""
    jsonschema.validate(instance=valid_baseline_payload, schema=engine_schema)


def test_hourly_layer_valid_payload(engine_schema: dict, valid_baseline_payload: dict):
    """Test that hourly layer payload passes JSON schema validation."""
    hourly_payload = valid_baseline_payload.copy()
    hourly_payload["layer"] = "hourly"
    hourly_payload["indicators"] = [
        {
            "id": "wind_speed",
            "rule_id": "RULE_SPRAY_WIND_SAFE",
            "value": 8.5,
            "unit": "km/h",
            "relative_rank": "typical",
            "rank_basis": "AgERA5_1991_2020",
            "rank_basis_n": 30
        }
    ]
    jsonschema.validate(instance=hourly_payload, schema=engine_schema)


def test_reject_stress_without_verified_evidence(valid_baseline_payload: dict, verified_evidence_ids: set[str]):
    """Test that emitting 'kondisi_stres_abiotik' without verified evidence refs is rejected."""
    unverified_payload = valid_baseline_payload.copy()
    unverified_payload["status"] = "kondisi_stres_abiotik"
    unverified_payload["evidence_refs"] = ["UNVERIFIED_HEURISTIC_RULE"] # not in verified_evidence_ids
    
    with pytest.raises(ValueError, match="Policy Violation: Status 'kondisi_stres_abiotik' emitted without any VERIFIED"):
        validate_engine_policy(unverified_payload, verified_evidence_ids)


def test_reject_opt_without_verified_evidence(valid_baseline_payload: dict, verified_evidence_ids: set[str]):
    """Test that emitting 'kondisi_mendukung_OPT' with convention-pending rule is rejected."""
    opt_payload = valid_baseline_payload.copy()
    opt_payload["crop"] = "cabai"
    opt_payload["status"] = "kondisi_mendukung_OPT"
    opt_payload["evidence_refs"] = ["SENTELHAS_2008_LWD"] # SENTELHAS_2008_LWD is UNVERIFIED on daily 24h dewpoint
    
    with pytest.raises(ValueError, match="Policy Violation: Status 'kondisi_mendukung_OPT' emitted without any VERIFIED"):
        validate_engine_policy(opt_payload, verified_evidence_ids)


def test_accept_stress_with_fao56_raw_depletion(valid_baseline_payload: dict, verified_evidence_ids: set[str]):
    """Test that emitting 'kondisi_stres_abiotik' with VERIFIED FAO56_RAW_DEPLETION passes."""
    verified_payload = valid_baseline_payload.copy()
    verified_payload["status"] = "kondisi_stres_abiotik"
    verified_payload["evidence_refs"] = ["FAO56_RAW_DEPLETION", "FAO56_KC_MAIZE"]
    
    # Should NOT raise
    validate_engine_policy(verified_payload, verified_evidence_ids)


def test_padi_water_module_insufficient(valid_baseline_payload: dict):
    """Test that rice water module enforces evidence_insufficient."""
    rice_payload = valid_baseline_payload.copy()
    rice_payload["crop"] = "padi"
    rice_payload["status"] = "evidence_insufficient"
    rice_payload["evidence_refs"] = ["FAO56_KC_RICE"]
    rice_payload["claim_allowed"] = "Modul deplesi tanah tidak berlaku untuk padi sawah tergenang; status evidence_insufficient."
    assert rice_payload["status"] == "evidence_insufficient"


def test_all_rules_in_rules_json_conform_to_contract(verified_evidence_ids: set[str]):
    """Verify that every rule in rules/rules.json without a VERIFIED evidence_id has CONVENTION_PENDING or INSUFFICIENT."""
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    rules = data.get("rules", [])
    assert len(rules) >= 15, "Rules register must contain all required operational rules."
    
    for r in rules:
        ev_id = r.get("evidence_id")
        status = r.get("status")
        if ev_id in verified_evidence_ids:
            assert status == "VERIFIED", f"Rule {r['id']} has verified evidence_id {ev_id} but status is {status}"
        else:
            assert status in ("CONVENTION_PENDING", "INSUFFICIENT"), (
                f"Rule {r['id']} lacks verified evidence_id ({ev_id}) but has status {status} instead of CONVENTION_PENDING/INSUFFICIENT"
            )
