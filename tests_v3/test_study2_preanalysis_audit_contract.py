from __future__ import annotations

import json
from pathlib import Path


def test_study2_preanalysis_audit_contract() -> None:
    report = json.loads(
        Path("outputs_v3/study2/STUDY2_PREANALYSIS_AUDIT.json")
        .read_text(encoding="utf-8")
    )
    gate = json.loads(
        Path("outputs_v3/study2/STUDY2_PREANALYSIS_GATE.json")
        .read_text(encoding="utf-8")
    )

    assert report["phase"] == "IM-R6C"
    assert report["network_upload_performed"] is False
    assert report["outcome_fields_read"] == []
    assert report["fields_read"] == [
        "country",
        "s1b",
        "s7",
        "e1",
        "base_wt",
    ]
    assert report["file"]["sha256"] == (
        "f61a2c6e09f4763818ae1d4db8b330e97bffd8bb0824c2d833b79d728152bd17"
    )
    assert report["csv_structure"]["data_row_count"] == 21055
    assert report["csv_structure"]["column_count"] == 723
    assert report["field_summary"]["s7"]["below_five_count"] == 1538
    assert report["frozen_rule_decision"]["preanalysis_gate"] == "NO-GO"
    assert report["frozen_rule_decision"]["primary_size_descriptor"] == "DISABLED"

    statuses = {item["id"]: item["status"] for item in report["gates"]}
    assert statuses["P7"] == "FAIL"
    assert all(
        statuses[key] == "PASS"
        for key in ["P1", "P2", "P3", "P4", "P5", "P6", "P8", "P9", "P10", "P11"]
    )

    assert gate["status"] == "COMPLETE_WITH_FROZEN_DESCRIPTOR_FAILURE"
    assert gate["outcome_analysis_gate"] == "NO-GO"
    assert gate["submission_gate"] == "NO-GO"
    assert gate["descriptor_decision"]["s7_primary_numeric_descriptor"] == "DISABLED"
    assert gate["descriptor_decision"]["s7_threshold_relaxation"] == "PROHIBITED"
    assert gate["descriptor_decision"]["e1_primary_descriptor"] == "PROHIBITED"
    assert gate["descriptor_decision"]["s1b_numeric_worker_count"] == "PROHIBITED"
    assert gate["next_phase"] == "IM-R6D"
    assert gate["next_allowed_command"] == "next"
