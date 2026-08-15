from __future__ import annotations

import hashlib
import json
from pathlib import Path


def test_study2_s1b_final_decision_contract() -> None:
    decision_path = Path(
        "examples/study2_fat_production_planning/s1b_final_decision.yml"
    )
    record = json.loads(
        Path(
            "examples/study2_fat_production_planning/"
            "s1b_final_decision.sha256.json"
        ).read_text(encoding="utf-8")
    )
    result = json.loads(
        Path("outputs_v3/study2/STUDY2_S1B_FINAL_DECISION.json")
        .read_text(encoding="utf-8")
    )
    gate = json.loads(
        Path("outputs_v3/study2/STUDY2_S1B_AUDIT_GATE.json")
        .read_text(encoding="utf-8")
    )

    observed = hashlib.sha256(decision_path.read_bytes()).hexdigest()
    assert observed == record["decision_sha256"]
    assert observed == (
        "b2a89a389ea24508c40a1ea4d08577c0"
        "393fce170129557c708487866ac6a09b"
    )

    assert record["outcome_results_inspected_before_final_decision"] is False
    assert record["candidate_mapping_accepted"] is False
    assert record["size_based_diagnostics_enabled"] is False

    text = decision_path.read_text(encoding="utf-8")
    assert 'd9_official_value_label_gate: "FAIL"' in text
    assert (
        's1b_candidate_mapping: "REJECTED_FOR_THIS_STUDY2_ANALYSIS"'
        in text
    )
    assert 'all_study2_size_based_diagnostics: "DISABLED"' in text
    assert 'outcomes_inspected_before_final_decision: false' in text

    assert result["status"] == "COMPLETE_MAPPING_REJECTED"
    assert result["final_decision"]["candidate_mapping_status"] == "REJECTED"
    assert result["final_decision"]["size_diagnostics"] == "DISABLED"
    assert result["outcomes_inspected"] is False

    assert gate["status"] == "COMPLETE_MAPPING_REJECTED"
    assert gate["candidate_mapping_status"] == "REJECTED"
    assert gate["d9_status"] == "FAIL"
    assert gate["size_diagnostics"] == "DISABLED"
    assert gate["outcome_analysis_gate"] == "NO-GO"
    assert gate["submission_gate"] == "NO-GO"
    assert gate["outcome_fields_inspected"] == []
