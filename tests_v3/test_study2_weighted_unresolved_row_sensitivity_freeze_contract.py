from __future__ import annotations

import hashlib
import json
from pathlib import Path


def test_study2_weighted_unresolved_row_sensitivity_freeze_contract() -> None:
    base = Path("examples/study2_fat_production_planning")
    freeze = base / "weighted_unresolved_row_sensitivity_freeze.yml"
    record = json.loads(
        (base / "weighted_unresolved_row_sensitivity_freeze.sha256.json").read_text(encoding="utf-8")
    )
    gate = json.loads(
        Path("outputs_v3/study2/STUDY2_WEIGHTED_UNRESOLVED_ROW_SENSITIVITY_GATE.json").read_text(encoding="utf-8")
    )
    tool = base / "IM_R7C_LOCAL_WEIGHTED_UNRESOLVED_ROW_SENSITIVITY.html"

    assert hashlib.sha256(freeze.read_bytes()).hexdigest() == "b36347ac18c77790a57ae4d1cac3c5917005a31f35030afcf9b68f57f23e09fc"
    assert record["freeze_sha256"] == "b36347ac18c77790a57ae4d1cac3c5917005a31f35030afcf9b68f57f23e09fc"
    assert record["corrected_internal_report_sha256"] == "020902d6242b2f801cc613de0e1dd0e86fc189a6d6d18b4d1ae8b871791820d0"
    assert record["corrected_aggregate_payload_fingerprint_sha256"] == "b18fa495616d28bcb315634c6247e2c8c94aa10724759e82cabed19a03251fe0"
    assert record["analytical_contract_changed"] is False
    assert record["unresolved_weight_mass_previously_inspected"] is False

    assert gate["status"] == "FROZEN_LOCAL_WEIGHTED_UNRESOLVED_SENSITIVITY_EXECUTION_OPEN"
    assert gate["result_interpretation_gate"] == "NO-GO"
    assert gate["manuscript_integration_gate"] == "NO-GO"
    assert gate["submission_gate"] == "NO-GO"
    assert gate["source_microdata_must_remain_local"] is True
    assert gate["full_sensitivity_report_public_release"] is False
    assert gate["permitted_fields"] == [
        "country", "base_wt", "ib9b1", "ib9b2", "ib9b3", "ib9b4", "ib9b5"
    ]

    text = tool.read_text(encoding="utf-8")
    assert "fetch(" not in text
    assert "XMLHttpRequest" not in text
    assert "<script src=" not in text.lower()
    assert 'const READ_FIELDS=["country","base_wt","ib9b1","ib9b2","ib9b3","ib9b4","ib9b5"]' in text
    assert 'gate("M14"' in text
    assert "GO_TO_EXTERNAL_WEIGHTED_MISSINGNESS_AUDIT" in text
    assert "P/(D+U)" in text
    assert "(P+U)/(D+U)" in text
