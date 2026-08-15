from __future__ import annotations

import hashlib
import json
from pathlib import Path


def test_study2_outcome_analysis_freeze_contract() -> None:
    freeze_path = Path(
        "examples/study2_fat_production_planning/"
        "outcome_analysis_freeze.yml"
    )
    record = json.loads(
        Path(
            "examples/study2_fat_production_planning/"
            "outcome_analysis_freeze.sha256.json"
        ).read_text(encoding="utf-8")
    )
    gate = json.loads(
        Path("outputs_v3/study2/STUDY2_OUTCOME_ANALYSIS_GATE.json")
        .read_text(encoding="utf-8")
    )

    observed = hashlib.sha256(freeze_path.read_bytes()).hexdigest()
    assert observed == record["freeze_sha256"]
    assert observed == (
        "2491149bcc41596d8dbb9e509ee73144"
        "7da70100de380d909daf45a4c46603be"
    )
    assert record["definitions_file_sha256"] == (
        "100d7a17cf415aa5faad4a3ec55787e"
        "224d29b04fe1ba9ee357db9647ecc77fa"
    )
    assert record["outcome_results_inspected_before_freeze"] is False
    assert record["size_based_diagnostics_enabled"] is False
    assert record["candidate_definitions_changed"] is False

    text = freeze_path.read_text(encoding="utf-8")
    assert 'status: "FROZEN_BEFORE_STUDY2_OUTCOME_EXECUTION"' in text
    assert 'pooled_global_prevalence: false' in text
    assert 'size_based_association: "DISABLED"' in text
    assert 'p_values: false' in text
    assert 'confidence_intervals: false' in text
    assert 'ib9b6_available: false' in text
    assert 'result_interpretation_permitted_after_local_run: false' in text

    # The scientific freeze remains authoritative even though the live gate
    # has advanced to a corrective implementation rerun after a failed E4.
    assert gate["status"] in {
        "FROZEN_LOCAL_EXECUTION_OPEN",
        "CORRECTIVE_RERUN_OPEN",
    }
    assert gate["result_interpretation_gate"] == "NO-GO"
    assert gate["submission_gate"] == "NO-GO"
    assert gate["size_fields_permitted"] == []
    assert gate["association_outputs_permitted"] == []
    assert gate["pooled_global_estimate_permitted"] is False
    assert gate["source_microdata_must_remain_local"] is True
    assert gate["outcome_analysis_freeze_sha256"] == observed
