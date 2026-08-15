from __future__ import annotations

import hashlib
import json
from pathlib import Path


def test_study2_preanalysis_freeze_contract() -> None:
    freeze_path = Path(
        "examples/study2_fat_production_planning/preanalysis_freeze.yml"
    )
    record = json.loads(
        Path(
            "examples/study2_fat_production_planning/"
            "preanalysis_freeze.sha256.json"
        ).read_text(encoding="utf-8")
    )
    gate = json.loads(
        Path("outputs_v3/study2/STUDY2_PREANALYSIS_GATE.json")
        .read_text(encoding="utf-8")
    )

    assert hashlib.sha256(freeze_path.read_bytes()).hexdigest() == record[
        "freeze_sha256"
    ]
    assert record["freeze_sha256"] == (
        "8c8743a5c4757f6eb8f56fc3dda91fc89d82bcb506847fe35efd4e448e3ab727"
    )
    assert record["outcome_results_inspected_before_freeze"] is False

    text = freeze_path.read_text(encoding="utf-8")
    assert 'primary_candidate: "s7"' in text
    assert 'secondary_complete_case_field: "e1"' in text
    assert 'validation_only_field: "s1b"' in text
    assert 'primary_india_merge: false' in text
    assert 'pooled_world_estimate: false' in text
    assert 'outcome_analysis_permitted: false' in text

    # The original freeze remains immutable even after its deterministic local
    # audit has been completed. The gate may advance from PENDING to the
    # recorded failure state, but it must never open outcome analysis.
    assert gate["status"] in {
        "PENDING_LOCAL_NON_OUTCOME_AUDIT",
        "COMPLETE_WITH_FROZEN_DESCRIPTOR_FAILURE",
    }
    assert gate["outcome_analysis_gate"] == "NO-GO"
    assert gate["submission_gate"] == "NO-GO"
    assert gate["preanalysis_freeze_sha256"] == record["freeze_sha256"]

    if gate["status"] == "PENDING_LOCAL_NON_OUTCOME_AUDIT":
        assert gate["fields_permitted_for_local_audit"] == [
            "country",
            "s1b",
            "s7",
            "e1",
            "base_wt",
        ]
        assert gate["outcome_fields_permitted"] == []
    else:
        assert gate["fields_read"] == [
            "country",
            "s1b",
            "s7",
            "e1",
            "base_wt",
        ]
        assert gate["outcome_fields_read"] == []
        assert gate["descriptor_decision"]["s7_primary_numeric_descriptor"] == "DISABLED"
        assert gate["descriptor_decision"]["s7_threshold_relaxation"] == "PROHIBITED"
        assert gate["next_phase"] == "IM-R6D"
