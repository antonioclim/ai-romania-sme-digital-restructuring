from __future__ import annotations

import hashlib
import json
from pathlib import Path


def test_study2_s1b_audit_freeze_contract() -> None:
    freeze_path = Path(
        "examples/study2_fat_production_planning/s1b_audit_freeze.yml"
    )
    record = json.loads(
        Path(
            "examples/study2_fat_production_planning/"
            "s1b_audit_freeze.sha256.json"
        ).read_text(encoding="utf-8")
    )
    gate = json.loads(
        Path("outputs_v3/study2/STUDY2_S1B_AUDIT_GATE.json")
        .read_text(encoding="utf-8")
    )

    observed = hashlib.sha256(freeze_path.read_bytes()).hexdigest()
    assert observed == record["freeze_sha256"]
    assert observed == (
        "1e1169c2e8e85428fa28c48d3f792795"
        "dce09d52c153173b2a0af3a0c21daa88"
    )

    assert record["outcome_results_inspected_before_freeze"] is False
    assert record["candidate_mapping_accepted"] is False

    text = freeze_path.read_text(encoding="utf-8")
    assert 'status: "PENDING_OFFICIAL_DICTIONARY_CONFIRMATION"' in text
    assert 'numeric_worker_count_interpretation: false' in text
    assert 'current_size_interpretation: false' in text
    assert 'official_value_labels_required: true' in text
    assert (
        'failure_action: "Disable all Study 2 size-based diagnostics."'
        in text
    )

    assert gate["status"] == "DOCUMENTATION_AND_LOCAL_AUDIT_OPEN"
    assert gate["outcome_analysis_gate"] == "NO-GO"
    assert gate["submission_gate"] == "NO-GO"
    assert gate["candidate_mapping_status"] == "NOT_ACCEPTED"
    assert gate["outcome_fields_permitted"] == []
    assert gate["s1b_audit_freeze_sha256"] == record["freeze_sha256"]
