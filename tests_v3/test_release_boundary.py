from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_version_3_public_inputs_are_aggregate_only() -> None:
    example_files = [
        path
        for path in (ROOT / "examples" / "romanian_ai_engagement").rglob("*")
        if path.is_file()
    ]
    assert example_files
    forbidden_names = {
        "responses.csv",
        "respondents.csv",
        "raw_export.csv",
        "analysis_dataset.csv",
        "analysis_dataset_constructed.csv",
    }
    assert not any(path.name.lower() in forbidden_names for path in example_files)


def test_no_private_version_3_directories_are_committed() -> None:
    forbidden_directories = {
        "private",
        "controlled",
        "restricted",
        "respondent_level",
        "raw_exports",
    }
    v3_paths = [ROOT / "odsa", ROOT / "examples", ROOT / "simulations", ROOT / "docs_v3"]
    for base in v3_paths:
        for path in base.rglob("*"):
            assert not forbidden_directories.intersection(part.lower() for part in path.parts)


def test_study1_contains_only_low_dimensional_counts() -> None:
    study = ROOT / "examples" / "romanian_ai_engagement"
    allowed = {
        "registry.yml",
        "state_counts.csv",
        "group_state_counts.csv",
    }
    assert {path.name for path in study.iterdir() if path.is_file()} == allowed
