from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from simulations.run_factorial_protocol import (
    _population_cramers_v,
    load_design,
    run_protocol,
    validate_design,
)


ROOT = Path(__file__).resolve().parents[1]
DESIGN_PATH = ROOT / "simulations" / "manuscript_protocol.yml"


def test_protocol_design_validates() -> None:
    design = load_design(DESIGN_PATH)
    audit = validate_design(design)
    assert audit["status"] == "PASS"
    assert audit["schema_version"] == "1.1"
    assert audit["scenario_count"] == 6


def test_controlled_scenario_mechanisms_are_exact() -> None:
    design = load_design(DESIGN_PATH)

    project_only = design["scenarios"]["project_only_gradient"]["probabilities"]
    active_rates = [project_only[group][0] for group in design["groups"]]
    broad_rates = [sum(project_only[group][:2]) for group in design["groups"]]
    assert active_rates == [0.20, 0.20, 0.20]
    assert broad_rates == [0.25, 0.45, 0.65]

    compensating = design["scenarios"]["compensating_gradient"]["probabilities"]
    assert [sum(compensating[group][:2]) for group in design["groups"]] == [
        0.50,
        0.50,
        0.50,
    ]

    reversal = design["scenarios"]["rank_reversal"]["probabilities"]
    assert [reversal[group][0] for group in design["groups"]] == [
        0.40,
        0.25,
        0.10,
    ]
    assert [sum(reversal[group][:2]) for group in design["groups"]] == [
        0.45,
        0.55,
        0.70,
    ]


def test_population_cramers_v_is_zero_for_equal_rates() -> None:
    import numpy as np

    value = _population_cramers_v(
        np.array([1 / 3, 1 / 3, 1 / 3]),
        np.array([0.4, 0.4, 0.4]),
    )
    assert math.isclose(value, 0.0, abs_tol=1e-12)


def test_ci_protocol_is_deterministic_and_separates_truth_layers(
    tmp_path: Path,
) -> None:
    design = load_design(DESIGN_PATH)
    first = tmp_path / "first"
    second = tmp_path / "second"
    audit_first = run_protocol(
        design,
        mode="ci",
        output=first,
        replications_override=3,
        max_cells=2,
    )
    audit_second = run_protocol(
        design,
        mode="ci",
        output=second,
        replications_override=3,
        max_cells=2,
    )
    assert audit_first == audit_second
    assert (first / "factorial_replicates.csv").read_bytes() == (
        second / "factorial_replicates.csv"
    ).read_bytes()
    assert (first / "factorial_cell_summary.csv").read_bytes() == (
        second / "factorial_cell_summary.csv"
    ).read_bytes()

    run_audit = json.loads(
        (first / "protocol_run_audit.json").read_text(encoding="utf-8")
    )
    assert run_audit["role"] == "continuous-integration mechanics check"
    assert run_audit["manuscript_evidence"] is False
    assert run_audit["replicate_row_count"] == 6

    with (first / "factorial_replicates.csv").open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert {
        "population_active_level",
        "sampled_true_active_level",
        "observed_active_level",
        "active_level_sampling_error",
        "active_level_observation_error",
        "active_level_total_error",
    }.issubset(rows[0])
