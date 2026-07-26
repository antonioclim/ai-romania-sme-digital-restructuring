from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_public_data_tree_is_aggregate_only():
    files = [p for p in (ROOT / "data").rglob("*") if p.is_file()]
    assert files
    assert all("aggregate" in p.parts for p in files)
    assert not any("respondent" in p.name.lower() or "responses" in p.name.lower() for p in files)


def test_key_counts():
    table = pd.read_csv(ROOT / "outputs/tables/table_2_core_estimates.csv").set_index("indicator")
    assert int(table.loc["Active AI use", "n"]) == 54
    assert int(table.loc["Project-stage category (planning, testing or deployment)", "n"]) == 51
    assert int(table.loc["Active use or project-stage engagement", "n"]) == 105
    assert int(table.loc["At least one workforce-preparation measure", "n"]) == 134
    assert int(table.loc["Workforce preparation excluding overlap with “no specific measures”", "n"]) == 121


def test_four_question_linked_associations():
    table = pd.read_csv(ROOT / "outputs/tables/table_s8_exploratory_association_tests.csv").set_index("test_id")
    assert list(table.index) == ["T1", "T2", "T3", "T4"]
    assert float(table.loc["T1", "cramers_v"]) == 0.134
    assert float(table.loc["T2", "cramers_v"]) == 0.350
    assert float(table.loc["T3", "cramers_v"]) == 0.428
    assert float(table.loc["T4", "cramers_v"]) == 0.503


def test_figures_and_validation_report():
    assert len(list((ROOT / "outputs/figures").glob("*.png"))) == 3
    report = json.loads((ROOT / "outputs/reports/aggregate_validation.json").read_text(encoding="utf-8"))
    assert report["status"] == "PASS"
    assert report["respondent_level_data_present"] is False
    assert report["association_statistics_recomputed_from_contingency_counts"] is True


def test_analysis_contract_input_list_is_exact():
    contract = json.loads((ROOT / "metadata/analysis_contract.json").read_text(encoding="utf-8"))
    actual = sorted(p.name for p in (ROOT / "data/aggregate").glob("*.csv"))
    assert contract["required_aggregate_inputs"] == actual
    assert contract["claim_count"] == len(pd.read_csv(ROOT / "metadata/claim_evidence_ledger.csv"))


def test_claim_ledger_matches_current_scope():
    ledger = pd.read_csv(ROOT / "metadata/claim_evidence_ledger.csv")
    joined = " ".join(ledger.astype(str).fillna("").to_numpy().ravel()).lower()
    assert not any(str(x).lower().startswith("rc") for x in ledger["claim_id"])
    assert "large-organisation comparator" not in joined
    assert "project-stage category" in joined
    assert "cramér’s v=0.350" in joined or "cramér's v=0.350" in joined


def test_claim_ledger_outputs_exist():
    ledger = pd.read_csv(ROOT / "metadata/claim_evidence_ledger.csv")
    for name in ledger["canonical_output"].dropna().astype(str):
        if not name or name in {"analysis_contract.json", "case_flow_and_missingness.csv"}:
            continue
        assert (ROOT / "outputs/tables" / name).exists(), name
