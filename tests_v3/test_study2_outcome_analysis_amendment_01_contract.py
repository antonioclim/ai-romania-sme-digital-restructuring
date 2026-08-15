from __future__ import annotations

import hashlib
import json
from pathlib import Path


def test_study2_outcome_analysis_amendment_01_contract() -> None:
    amendment_path = Path(
        "examples/study2_fat_production_planning/"
        "outcome_analysis_implementation_amendment_01.yml"
    )
    record = json.loads(
        Path(
            "examples/study2_fat_production_planning/"
            "outcome_analysis_implementation_amendment_01.sha256.json"
        ).read_text(encoding="utf-8")
    )
    gate = json.loads(
        Path("outputs_v3/study2/STUDY2_OUTCOME_ANALYSIS_GATE.json")
        .read_text(encoding="utf-8")
    )
    quarantine = json.loads(
        Path(
            "outputs_v3/study2/"
            "STUDY2_IM_R7A_FAILED_RUN_QUARANTINE.json"
        ).read_text(encoding="utf-8")
    )

    observed = hashlib.sha256(amendment_path.read_bytes()).hexdigest()
    assert observed == record["amendment_sha256"]
    assert observed == "03244a3761052b294ab122999ff061b8f5932b4332b2ad7bd713e5f2f255e1ef"
    assert record["prior_outcome_analysis_freeze_sha256"] == (
        "2491149bcc41596d8dbb9e509ee731447da70100de380d909daf45a4c46603be"
    )
    assert record["definitions_file_sha256"] == (
        "100d7a17cf415aa5faad4a3ec55787e224d29b04fe1ba9ee357db9647ecc77fa"
    )
    assert record["analytical_definitions_changed"] is False
    assert record["denominator_membership_rule_changed"] is False
    assert record["weighting_policy_changed"] is False
    assert record["estimands_changed"] is False
    assert record["thresholds_changed"] is False
    assert record["suppression_rules_changed"] is False
    assert record["result_interpretation_permitted"] is False

    assert quarantine["status"] == "QUARANTINED_FAILED_EXECUTION"
    assert quarantine["report_sha256"] == (
        "c2331d544a131d414736aa049ba13fbce723b56c3889030ef2fb069ea9c777ae"
    )
    assert quarantine["interpretation_or_release_permitted"] is False
    assert quarantine["corrective_rerun_required"] is True

    assert gate["status"] == "CORRECTIVE_RERUN_OPEN"
    assert gate["result_interpretation_gate"] == "NO-GO"
    assert gate["submission_gate"] == "NO-GO"
    assert gate["analytical_changes_permitted"] == []
    assert gate["expected_aggregate_payload_fingerprint_sha256"] == (
        "b18fa495616d28bcb315634c6247e2c8c94aa10724759e82cabed19a03251fe0"
    )
