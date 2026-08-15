from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
FREEZE_PATH = ROOT / "docs_v3" / "STUDY2_SELECTION_FREEZE.json"
REGISTER_PATH = ROOT / "docs_v3" / "STUDY2_CANDIDATE_REGISTER.csv"
REGISTRY_PATH = (
    ROOT
    / "examples"
    / "study2_fat_production_planning"
    / "selection_registry.yml"
)
DEFINITIONS_PATH = (
    ROOT
    / "examples"
    / "study2_fat_production_planning"
    / "definitions.yml"
)
GATE_PATH = ROOT / "outputs_v3" / "study2" / "STUDY2_SELECTION_GATE.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_study2_selection_files_match_freeze() -> None:
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    assert (
        freeze["status"]
        == "FROZEN_BEFORE_MICRODATA_ACQUISITION_AND_OUTCOME_INSPECTION"
    )
    assert freeze["selected_candidate_id"] == "fat_production_planning"
    assert freeze["selected_dataset_reference"] == "WLD_2019-2023_FAT_v01_M"
    assert freeze["selected_dataset_doi"] == "10.48529/assd-3j65"
    assert freeze["outcome_results_inspected"] is False
    assert freeze["microdata_acquired"] is False
    assert freeze["replication_executed"] is False

    for relative_path, expected in freeze["files"].items():
        path = ROOT / relative_path
        assert path.exists(), relative_path
        assert _sha256(path) == expected, relative_path


def test_candidate_scoring_and_reserve_order_are_locked() -> None:
    with REGISTER_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 5
    selected = [row for row in rows if row["decision"] == "SELECTED_CONDITIONAL"]
    assert len(selected) == 1
    assert selected[0]["candidate_id"] == "fat_production_planning"
    assert int(selected[0]["total_score"]) == 20
    assert selected[0]["automatic_exclusion"] == "FALSE"

    excluded = {
        row["candidate_id"]
        for row in rows
        if row["automatic_exclusion"] == "TRUE"
    }
    assert excluded == {"flash_eurobarometer_486", "us_census_btos_ai"}

    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    assert freeze["reserve_order"] == [
        "us_census_abs_2018_technology",
        "eurostat_digital_intensity",
    ]


def test_locked_definitions_are_nested_and_semantically_bounded() -> None:
    payload = yaml.safe_load(DEFINITIONS_PATH.read_text(encoding="utf-8"))
    assert payload["status"] == "FROZEN_BEFORE_OUTCOME_INSPECTION"

    definitions = payload["definitions"]
    integrated = set(definitions["integrated_planning"]["positive_states"])
    specialised = set(definitions["specialised_planning"]["positive_states"])
    digital = set(
        definitions["digitally_enabled_planning"]["positive_states"]
    )

    assert integrated == {"erp"}
    assert integrated < specialised < digital
    assert "handwritten_processes" not in digital
    assert "other" not in payload["primary_denominator_states"]

    assert "all_positive_establishments_use_erp" in definitions[
        "specialised_planning"
    ]["does_not_support"]
    assert "integrated_planning_architecture" in definitions[
        "digitally_enabled_planning"
    ]["does_not_support"]


def test_selection_registry_blocks_result_based_switching() -> None:
    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    assert (
        registry["protocol_status"]
        == "FROZEN_BEFORE_MICRODATA_ACQUISITION"
    )
    assert registry["outcome_results_inspected"] is False
    assert registry["microdata_acquired"] is False
    assert registry["selected_candidate"]["documented_cases"] == 21055
    assert registry["weighting_policy"]["forbidden"] == (
        "naive_pooled_world_prevalence"
    )

    gate_ids = {
        row["id"] for row in registry["structural_acquisition_gate"]
    }
    assert gate_ids == {f"G{index}" for index in range(1, 11)}

    assert registry["reserve_order"] == [
        "us_census_abs_2018_technology",
        "eurostat_digital_intensity",
    ]


def test_im_r5_gate_does_not_claim_a_completed_replication() -> None:
    gate = json.loads(GATE_PATH.read_text(encoding="utf-8"))
    assert gate["gate"] == "GO_CONDITIONAL"
    assert gate["submission_gate"] == "NO-GO"
    assert gate["selection_frozen"] is True
    assert gate["selection_precedes_microdata_acquisition"] is True
    assert gate["selection_precedes_outcome_inspection"] is True
    assert gate["microdata_acquired"] is False
    assert gate["study2_results_generated"] is False
    assert gate["replication_status"] == "NOT_STARTED"
    assert gate["structural_acquisition_gate"] == "PENDING"
