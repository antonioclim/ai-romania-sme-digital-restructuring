from __future__ import annotations

import hashlib
import json
from pathlib import Path


def test_study2_public_result_contract() -> None:
    summary_path = Path(
        "outputs_v3/study2/STUDY2_PUBLIC_RESULT_SUMMARY.json"
    )
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    contract_path = Path(
        "examples/study2_fat_production_planning/"
        "public_result_contract.yml"
    )
    record = json.loads(
        Path(
            "examples/study2_fat_production_planning/"
            "public_result_contract.sha256.json"
        ).read_text(encoding="utf-8")
    )

    assert hashlib.sha256(summary_path.read_bytes()).hexdigest() == (
        "f656b1049d5e21e9a950ddb6bdcfe748ce06671e84d72aa979f1b58599d1aad3"
    )
    assert hashlib.sha256(contract_path.read_bytes()).hexdigest() == (
        "bb9fd7f65b9323c76c7362a4d4c39a24500d1ac1e97ee90b0dcda93c4a6ca018"
    )
    assert record["public_summary_sha256"] == "f656b1049d5e21e9a950ddb6bdcfe748ce06671e84d72aa979f1b58599d1aad3"
    assert record["public_result_contract_sha256"] == "bb9fd7f65b9323c76c7362a4d4c39a24500d1ac1e97ee90b0dcda93c4a6ca018"

    assert summary["status"] == "AUDITED_PUBLIC_AGGREGATE_SUMMARY"
    assert summary["interpretation_status"]["technical_result_validated"] is True
    assert summary["public_disclosure_boundary"][
        "full_internal_report_publication"
    ] == "PROHIBITED"

    forbidden_top_level = {
        "source_stratum_results",
        "execution_audit",
        "aggregate_payload_fingerprint",
    }
    assert forbidden_top_level.isdisjoint(summary)

    serialised = json.dumps(summary, sort_keys=True)
    for forbidden in (
        '"left_ranking"',
        '"right_ranking"',
        '"positive_n"',
        '"negative_n"',
        '"mapped_n"',
        '"firmid"',
    ):
        assert forbidden not in serialised

    ordering = summary["ordering_diagnostics"]
    for weighting in ordering.values():
        for comparison in weighting.values():
            assert "left_ranking" not in comparison
            assert "right_ranking" not in comparison

    assert summary["posthoc_hostile_audit_sensitivities"][
        "conservative_unweighted_unresolved_assignment"
    ]["broad_lower_exceeds_strict_upper_source_strata"] == 16
    assert summary["posthoc_hostile_audit_sensitivities"][
        "conservative_unweighted_unresolved_assignment"
    ]["broad_lower_exceeds_middle_upper_source_strata"] == 16
