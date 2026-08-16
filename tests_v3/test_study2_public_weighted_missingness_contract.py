from __future__ import annotations

import hashlib
import json
from pathlib import Path


def test_study2_public_weighted_missingness_contract() -> None:
    summary_path = Path(
        "outputs_v3/study2/"
        "STUDY2_PUBLIC_WEIGHTED_MISSINGNESS_SUMMARY.json"
    )
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    contract_path = Path(
        "examples/study2_fat_production_planning/"
        "public_weighted_missingness_contract.yml"
    )
    record_path = Path(
        "examples/study2_fat_production_planning/"
        "public_weighted_missingness_contract.sha256.json"
    )
    record = json.loads(record_path.read_text(encoding="utf-8"))

    assert hashlib.sha256(summary_path.read_bytes()).hexdigest() == (
        "a78301a4d75adbb462bd7d9a596eefac8a5c6ef81d1fff99c254f32de08c845c"
    )
    assert hashlib.sha256(contract_path.read_bytes()).hexdigest() == (
        "4dd2e4540d3e8609beb4e4929bf6dc9a27a87f920d35517e2004a254faa8c4c4"
    )
    assert record["public_summary_sha256"] == "a78301a4d75adbb462bd7d9a596eefac8a5c6ef81d1fff99c254f32de08c845c"
    assert record["public_contract_sha256"] == "4dd2e4540d3e8609beb4e4929bf6dc9a27a87f920d35517e2004a254faa8c4c4"

    assert summary["status"] == (
        "AUDITED_HARDENED_PUBLIC_WEIGHTED_MISSINGNESS_SUMMARY"
    )
    assert summary["decision"]["technical_weighted_missingness_sensitivity"] == "GO"
    assert summary["decision"]["manuscript_integration"] == "GO_WITH_CONDITIONS"
    assert summary["decision"]["submission"] == "NO_GO"

    forbidden_top_level = {
        "source_stratum_weighted_sensitivity",
        "gates",
        "execution_audit",
    }
    assert forbidden_top_level.isdisjoint(summary)

    serialised = json.dumps(summary, sort_keys=True)
    for forbidden in (
        '"source_label"',
        '"positive_weight"',
        '"denominator_weight"',
        '"unresolved_weight"',
        '"mapped_n"',
        '"firmid"',
    ):
        assert forbidden not in serialised

    robust = summary["robust_separation"]
    assert robust["specialised_to_digitally_enabled"][
        "robust_separation_strata"
    ] == 15
    assert robust["integrated_to_digitally_enabled"][
        "robust_separation_strata"
    ] == 13
    assert robust["integrated_to_specialised"][
        "robust_separation_strata"
    ] == 9

    assert summary["claim_boundary"][
        "marginal_extrema_jointly_attainable_across_definitions"
    ] is False
    assert summary["public_disclosure_boundary"][
        "full_internal_im_r7c_report_publication"
    ] == "PROHIBITED"
