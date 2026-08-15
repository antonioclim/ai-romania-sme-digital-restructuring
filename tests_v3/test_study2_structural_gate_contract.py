import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def test_study2_structural_gate_contract() -> None:
    gate = load_json("outputs_v3/study2/STUDY2_STRUCTURAL_GATE.json")

    assert gate["phase"] == "IM-R6B"
    assert gate["gate"] == "GO_TO_PREANALYSIS_HARMONISATION_FREEZE"
    assert gate["analysis_gate"] == "NO-GO"
    assert gate["submission_gate"] == "NO-GO"

    assert gate["privacy"]["network_upload_performed"] is False
    assert gate["privacy"]["microdata_rows_in_report"] is False
    assert gate["privacy"]["state_specific_counts_in_report"] is False
    assert gate["privacy"]["odsa_results_in_report"] is False

    assert gate["source"]["dataset_reference"] == "WLD_2019-2023_FAT_v01_M"
    assert gate["source"]["dataset_doi"] == "10.48529/assd-3j65"

    assert gate["file"]["name"] == "fat0_raw_data_qje.csv"
    assert gate["file"]["size_bytes"] == 19_633_172
    assert gate["file"]["crc32"] == "4418a02b"

    assert gate["csv_structure"]["data_row_count"] == 21_055
    assert gate["csv_structure"]["column_count"] == 723
    assert gate["csv_structure"]["inconsistent_row_width_count"] == 0
    assert gate["csv_structure"]["duplicate_header_names"] == []
    assert gate["csv_structure"]["empty_header_positions"] == []

    assert gate["field_presence"]["country"] is True
    assert gate["field_presence"]["e1"] is True
    assert gate["field_presence"]["base_wt"] is True
    assert gate["field_presence"]["direct_b9b"] is False
    assert gate["field_presence"]["complete_onehot_ib9b1_to_ib9b5"] is True
    assert gate["field_presence"]["ib9b6_other"] is False

    assert gate["mapping"]["mapping_attempted_count"] == 20_069
    assert gate["mapping"]["mapping_failure_count"] == 0
    assert gate["mapping"]["mapping_failure_share"] == 0.0
    assert gate["mapping"]["primary_eligible_denominator"] == 20_069
    assert gate["mapping"]["all_zero_or_structurally_unresolved_count"] == 986
    assert gate["mapping"]["state_specific_counts_disclosed"] is False

    assert gate["descriptors"]["source_stratum_label_count"] == 16
    assert gate["descriptors"]["documented_country_count"] == 15
    assert gate["descriptors"]["employment_numeric_valid_count"] == 13_399
    assert gate["descriptors"]["employment_missing_count"] == 7_656
    assert gate["descriptors"]["weight_positive_numeric_count"] == 21_054
    assert gate["descriptors"]["weight_missing_count"] == 1

    assert all(
        status in {"PASS", "PASS_WITH_SEMANTIC_RELABEL"}
        for status in gate["gate_results"].values()
    )


def test_study2_analysis_remains_blocked() -> None:
    acquisition = load_json("outputs_v3/study2/STUDY2_ACQUISITION_GATE.json")

    assert acquisition["status"] == "ACQUISITION_AND_STRUCTURAL_GATE_VERIFIED"
    assert acquisition["analysis_gate"] == "NO-GO"
    assert acquisition["submission_gate"] == "NO-GO"
    assert acquisition["outcome_results_inspected"] is False
    assert acquisition["next_phase"] == "IM-R6C"
