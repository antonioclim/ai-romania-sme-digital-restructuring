"""Run the manuscript-grade factorial ODSA simulation study.

The study distinguishes formal invariants from contingent sensitivity. All
outputs are synthetic and contain no human-participant data.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
from collections import OrderedDict, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from odsa.analysis import (
    association_diagnostics,
    definition_level,
    group_rate_diagnostics,
    ranking_reversal,
)
from odsa.models import ODSAValidationError, OutcomeDefinition, StateSpace
from odsa.properties import coarsen_counts, identifiability_register


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "simulations" / "design.yml"
FINE_STATES = ("active_use", "deployed", "testing", "planning", "no_engagement")
GROUPS = ("Group A", "Group B", "Group C")


def load_design(path: str | Path) -> dict[str, Any]:
    """Load and minimally validate the simulation design."""

    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("simulation design must be a YAML mapping")
    if tuple(data["states"]) != FINE_STATES:
        raise ValueError(f"design states must be {FINE_STATES}")
    if tuple(data["groups"]) != GROUPS:
        raise ValueError(f"design groups must be {GROUPS}")
    if not math.isclose(sum(float(data["base_probabilities"][s]) for s in FINE_STATES), 1.0):
        raise ValueError("base probabilities must sum to one")
    return data


def enumerate_design_cells(design: dict[str, Any]) -> list[dict[str, Any]]:
    """Enumerate the complete factorial in stable order."""

    factors = design["factorial"]
    names = list(factors)
    cells: list[dict[str, Any]] = []
    for index, values in enumerate(itertools.product(*(factors[name] for name in names)), start=1):
        cell = dict(zip(names, values, strict=True))
        cell["cell_id"] = f"C{index:04d}"
        cell["gradient_relation"] = _gradient_relation(
            str(cell["active_gradient"]), str(cell["added_state_gradient"])
        )
        cells.append(cell)
    return cells


def _gradient_relation(active: str, added: str) -> str:
    if active == "flat" and added == "flat":
        return "both_flat"
    if added == "middle_concentrated":
        return "middle_concentrated"
    if active == "flat" or added == "flat":
        return "one_flat"
    if active == added:
        return "aligned"
    return "opposed"


def _group_probabilities(design: dict[str, Any], cell: dict[str, Any]) -> dict[str, np.ndarray]:
    base = np.array([float(design["base_probabilities"][s]) for s in FINE_STATES])
    patterns = design["gradient_patterns"]
    active_pattern = np.array(patterns[str(cell["active_gradient"])], dtype=float)
    added_pattern = np.array(patterns[str(cell["added_state_gradient"])], dtype=float)
    active_strength = float(design["active_shift_strength"])
    added_strength = float(design["added_state_shift_strength"])
    weights = np.array(
        [
            float(design["added_state_weights"]["deployed"]),
            float(design["added_state_weights"]["testing"]),
            float(design["added_state_weights"]["planning"]),
        ]
    )
    if not math.isclose(float(weights.sum()), 1.0):
        raise ValueError("added-state weights must sum to one")

    probabilities: dict[str, np.ndarray] = {}
    for group_index, group in enumerate(GROUPS):
        current = base.copy()
        active_shift = active_strength * active_pattern[group_index]
        added_shift = added_strength * added_pattern[group_index]
        current[0] += active_shift
        current[1:4] += added_shift * weights
        current[4] -= active_shift + added_shift
        if (current <= 0).any() or not math.isclose(float(current.sum()), 1.0, abs_tol=1e-12):
            raise ValueError(f"invalid probability vector for {cell['cell_id']} and {group}: {current}")
        probabilities[group] = current
    return probabilities


def _group_sizes(design: dict[str, Any], cell: dict[str, Any]) -> dict[str, int]:
    nominal = int(cell["sample_size_per_group"])
    multipliers = design["group_size_multipliers"][str(cell["group_balance"])]
    sizes = {
        group: max(20, int(round(nominal * float(multiplier))))
        for group, multiplier in zip(GROUPS, multipliers, strict=True)
    }
    return sizes


def _misclassification_matrix(rate: float) -> np.ndarray:
    if rate < 0 or rate >= 1:
        raise ValueError("misclassification rate must be in [0, 1)")
    size = len(FINE_STATES)
    matrix = np.zeros((size, size), dtype=float)
    for index in range(size):
        matrix[index, index] = 1.0 - rate
        if index == 0:
            matrix[index, 1] = rate
        elif index == size - 1:
            matrix[index, size - 2] = rate
        else:
            matrix[index, index - 1] = rate / 2.0
            matrix[index, index + 1] = rate / 2.0
    return matrix


def _simulate_latent_counts(
    probabilities: dict[str, np.ndarray],
    sizes: dict[str, int],
    rng: np.random.Generator,
) -> dict[str, OrderedDict[str, int]]:
    counts: dict[str, OrderedDict[str, int]] = {}
    for group in GROUPS:
        observed = rng.multinomial(sizes[group], probabilities[group])
        counts[group] = OrderedDict(
            (state, int(value)) for state, value in zip(FINE_STATES, observed, strict=True)
        )
    return counts


def _apply_misclassification(
    latent_counts: dict[str, OrderedDict[str, int]],
    rate: float,
    rng: np.random.Generator,
) -> dict[str, OrderedDict[str, int]]:
    matrix = _misclassification_matrix(rate)
    output: dict[str, OrderedDict[str, int]] = {}
    for group in GROUPS:
        observed = np.zeros(len(FINE_STATES), dtype=int)
        for true_index, state in enumerate(FINE_STATES):
            split = rng.multinomial(int(latent_counts[group][state]), matrix[true_index])
            observed += split
        output[group] = OrderedDict(
            (state, int(value)) for state, value in zip(FINE_STATES, observed, strict=True)
        )
    return output


def _coarsen_group_counts(
    fine_counts: dict[str, OrderedDict[str, int]],
    mapping: dict[str, str],
) -> dict[str, OrderedDict[str, int]]:
    fine_space = StateSpace(FINE_STATES)
    return {
        group: coarsen_counts(fine_space, counts, mapping)
        for group, counts in fine_counts.items()
    }


def _aggregate_group_counts(
    group_counts: dict[str, OrderedDict[str, int]],
) -> OrderedDict[str, int]:
    states = list(next(iter(group_counts.values())))
    return OrderedDict(
        (state, sum(int(group_counts[group][state]) for group in GROUPS))
        for state in states
    )


def _definition_pair(
    design: dict[str, Any], coarsening: str
) -> tuple[StateSpace, OutcomeDefinition, OutcomeDefinition]:
    registered = design["analysis_definitions"][coarsening]
    mapping = design["coarsening_maps"][coarsening]
    observed_states = list(dict.fromkeys(mapping[state] for state in FINE_STATES))
    state_space = StateSpace(observed_states)
    active = OutcomeDefinition("active_use", registered["active_use"])
    broad = OutcomeDefinition("broad_engagement", registered["broad_engagement"])
    return state_space, active, broad


def _fine_definition_pair() -> tuple[StateSpace, OutcomeDefinition, OutcomeDefinition]:
    return (
        StateSpace(FINE_STATES),
        OutcomeDefinition("active_use", ["active_use"]),
        OutcomeDefinition(
            "broad_engagement", ["active_use", "deployed", "testing", "planning"]
        ),
    )


def _all_fine_definitions(design: dict[str, Any]) -> list[OutcomeDefinition]:
    return [
        OutcomeDefinition(name, states)
        for name, states in design["latent_definitions"].items()
    ]


def _safe_association(
    state_space: StateSpace,
    group_counts: dict[str, OrderedDict[str, int]],
    definition: OutcomeDefinition,
) -> float:
    try:
        return float(
            association_diagnostics(state_space, group_counts, definition)["cramers_v"]
        )
    except ODSAValidationError:
        return float("nan")


def _safe_rank_reversal(
    state_space: StateSpace,
    group_counts_left: dict[str, OrderedDict[str, int]],
    left: OutcomeDefinition,
    group_counts_right: dict[str, OrderedDict[str, int]],
    right: OutcomeDefinition,
) -> bool | None:
    try:
        left_rows = group_rate_diagnostics(state_space, group_counts_left, left)
        right_rows = group_rate_diagnostics(state_space, group_counts_right, right)
        return bool(ranking_reversal(left_rows, right_rows))
    except ODSAValidationError:
        return None


def _retain_for_definition(
    group_counts: dict[str, OrderedDict[str, int]],
    retention: dict[str, float],
    rng: np.random.Generator,
) -> dict[str, OrderedDict[str, int]]:
    retained: dict[str, OrderedDict[str, int]] = {}
    for group, counts in group_counts.items():
        row: OrderedDict[str, int] = OrderedDict()
        for state, count in counts.items():
            probability = float(retention[state])
            if probability <= 0 or probability > 1:
                raise ValueError(f"invalid retention probability for {state}: {probability}")
            row[state] = int(rng.binomial(int(count), probability))
        if sum(row.values()) <= 0:
            raise ValueError("definition-specific retention removed an entire group")
        retained[group] = row
    return retained


def _definition_level_from_groups(
    state_space: StateSpace,
    group_counts: dict[str, OrderedDict[str, int]],
    definition: OutcomeDefinition,
) -> float:
    totals = _aggregate_group_counts(group_counts)
    return float(definition_level(state_space, totals, definition)["level"])


def simulate_replication(
    design: dict[str, Any],
    cell: dict[str, Any],
    replication: int,
    replication_seed: int,
) -> dict[str, Any]:
    rng = np.random.default_rng(replication_seed)
    probabilities = _group_probabilities(design, cell)
    sizes = _group_sizes(design, cell)
    latent_group_counts = _simulate_latent_counts(probabilities, sizes, rng)
    misclassified = _apply_misclassification(
        latent_group_counts, float(cell["misclassification_rate"]), rng
    )

    coarsening = str(cell["coarsening"])
    mapping = {
        str(key): str(value)
        for key, value in design["coarsening_maps"][coarsening].items()
    }
    observed_group_counts = _coarsen_group_counts(misclassified, mapping)

    latent_space, latent_active, latent_broad = _fine_definition_pair()
    observed_space, observed_active, observed_broad = _definition_pair(design, coarsening)

    latent_active_level = _definition_level_from_groups(
        latent_space, latent_group_counts, latent_active
    )
    latent_broad_level = _definition_level_from_groups(
        latent_space, latent_group_counts, latent_broad
    )
    observed_active_level = _definition_level_from_groups(
        observed_space, observed_group_counts, observed_active
    )
    observed_broad_level = _definition_level_from_groups(
        observed_space, observed_group_counts, observed_broad
    )

    latent_active_v = _safe_association(latent_space, latent_group_counts, latent_active)
    latent_broad_v = _safe_association(latent_space, latent_group_counts, latent_broad)
    observed_active_v = _safe_association(
        observed_space, observed_group_counts, observed_active
    )
    observed_broad_v = _safe_association(
        observed_space, observed_group_counts, observed_broad
    )

    latent_rank_reversal = _safe_rank_reversal(
        latent_space,
        latent_group_counts,
        latent_active,
        latent_group_counts,
        latent_broad,
    )
    observed_rank_reversal = _safe_rank_reversal(
        observed_space,
        observed_group_counts,
        observed_active,
        observed_group_counts,
        observed_broad,
    )

    denominator_regime = str(cell["denominator_regime"])
    if denominator_regime == "common":
        active_report_counts = observed_group_counts
        broad_report_counts = observed_group_counts
    else:
        retention = design["definition_dependent_retention"]
        active_report_counts = _retain_for_definition(
            observed_group_counts, retention["active_use"], rng
        )
        broad_report_counts = _retain_for_definition(
            observed_group_counts, retention["broad_engagement"], rng
        )

    reported_active_level = _definition_level_from_groups(
        observed_space, active_report_counts, observed_active
    )
    reported_broad_level = _definition_level_from_groups(
        observed_space, broad_report_counts, observed_broad
    )
    reported_active_v = _safe_association(
        observed_space, active_report_counts, observed_active
    )
    reported_broad_v = _safe_association(
        observed_space, broad_report_counts, observed_broad
    )
    reported_rank_reversal = _safe_rank_reversal(
        observed_space,
        active_report_counts,
        observed_active,
        broad_report_counts,
        observed_broad,
    )

    identifiable = identifiability_register(_all_fine_definitions(design), mapping)
    identifiable_names = sorted(
        row["definition"] for row in identifiable if bool(row["identifiable"])
    )

    return {
        **cell,
        "replication": replication,
        "replication_seed": replication_seed,
        "total_n": sum(sizes.values()),
        "latent_active_level": latent_active_level,
        "latent_broad_level": latent_broad_level,
        "observed_active_level": observed_active_level,
        "observed_broad_level": observed_broad_level,
        "reported_active_level": reported_active_level,
        "reported_broad_level": reported_broad_level,
        "active_level_bias": observed_active_level - latent_active_level,
        "broad_level_bias": observed_broad_level - latent_broad_level,
        "latent_active_v": latent_active_v,
        "latent_broad_v": latent_broad_v,
        "observed_active_v": observed_active_v,
        "observed_broad_v": observed_broad_v,
        "reported_active_v": reported_active_v,
        "reported_broad_v": reported_broad_v,
        "latent_delta_v_broad_minus_active": latent_broad_v - latent_active_v,
        "observed_delta_v_broad_minus_active": observed_broad_v - observed_active_v,
        "reported_delta_v_broad_minus_active": reported_broad_v - reported_active_v,
        "latent_rank_reversal": latent_rank_reversal,
        "observed_rank_reversal": observed_rank_reversal,
        "reported_rank_reversal": reported_rank_reversal,
        "rank_reversal_measurement_disagreement": (
            None
            if latent_rank_reversal is None or observed_rank_reversal is None
            else latent_rank_reversal != observed_rank_reversal
        ),
        "common_denominator_monotonicity_violation": (
            observed_broad_level + 1e-15 < observed_active_level
        ),
        "apparent_monotonicity_violation": (
            reported_broad_level + 1e-15 < reported_active_level
        ),
        "identifiable_definition_count": len(identifiable_names),
        "identifiable_definitions": "|".join(identifiable_names),
    }


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _finite(values: list[Any]) -> np.ndarray:
    array = np.asarray([float(value) for value in values], dtype=float)
    return array[np.isfinite(array)]


def _boolean_share(values: list[Any]) -> float | None:
    usable = [bool(value) for value in values if value is not None]
    return None if not usable else sum(usable) / len(usable)


def summarise_cells(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["cell_id"])].append(row)

    summaries: list[dict[str, Any]] = []
    for cell_id in sorted(grouped):
        group = grouped[cell_id]
        first = group[0]
        delta = _finite([row["observed_delta_v_broad_minus_active"] for row in group])
        active_bias = _finite([row["active_level_bias"] for row in group])
        broad_bias = _finite([row["broad_level_bias"] for row in group])
        summary = {
            key: first[key]
            for key in (
                "cell_id",
                "sample_size_per_group",
                "active_gradient",
                "added_state_gradient",
                "gradient_relation",
                "group_balance",
                "misclassification_rate",
                "coarsening",
                "denominator_regime",
            )
        }
        summary.update(
            {
                "replications": len(group),
                "mean_latent_active_level": float(
                    np.mean([row["latent_active_level"] for row in group])
                ),
                "mean_latent_broad_level": float(
                    np.mean([row["latent_broad_level"] for row in group])
                ),
                "mean_observed_active_level": float(
                    np.mean([row["observed_active_level"] for row in group])
                ),
                "mean_observed_broad_level": float(
                    np.mean([row["observed_broad_level"] for row in group])
                ),
                "mean_active_level_bias": float(active_bias.mean()),
                "mean_broad_level_bias": float(broad_bias.mean()),
                "mean_delta_v": float(delta.mean()),
                "median_delta_v": float(np.median(delta)),
                "q05_delta_v": float(np.quantile(delta, 0.05)),
                "q95_delta_v": float(np.quantile(delta, 0.95)),
                "broad_association_stronger_share": float(np.mean(delta > 1e-12)),
                "broad_association_weaker_share": float(np.mean(delta < -1e-12)),
                "observed_rank_reversal_share": _boolean_share(
                    [row["observed_rank_reversal"] for row in group]
                ),
                "reported_rank_reversal_share": _boolean_share(
                    [row["reported_rank_reversal"] for row in group]
                ),
                "measurement_rank_disagreement_share": _boolean_share(
                    [row["rank_reversal_measurement_disagreement"] for row in group]
                ),
                "apparent_monotonicity_violation_share": _boolean_share(
                    [row["apparent_monotonicity_violation"] for row in group]
                ),
                "common_monotonicity_violation_count": sum(
                    bool(row["common_denominator_monotonicity_violation"])
                    for row in group
                ),
                "mean_identifiable_definition_count": float(
                    np.mean([row["identifiable_definition_count"] for row in group])
                ),
            }
        )
        summaries.append(summary)
    return summaries


def build_global_summary(
    design: dict[str, Any],
    cells: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    replications: int,
    seed: int,
) -> dict[str, Any]:
    delta = _finite([row["observed_delta_v_broad_minus_active"] for row in rows])
    common_violations = sum(
        bool(row["common_denominator_monotonicity_violation"]) for row in rows
    )
    rank_reversals = sum(row["observed_rank_reversal"] is True for row in rows)
    apparent_violations = sum(
        row["denominator_regime"] == "definition_dependent"
        and bool(row["apparent_monotonicity_violation"])
        for row in rows
    )
    collapsed_counts = {
        int(row["identifiable_definition_count"])
        for row in rows
        if row["coarsening"] == "project_collapsed"
    }
    none_counts = {
        int(row["identifiable_definition_count"])
        for row in rows
        if row["coarsening"] == "none"
    }
    expected_collapsed = int(
        design["gates"]["expected_identifiable_definitions_after_project_collapse"]
    )

    gates = {
        "common_denominator_monotonicity": common_violations == 0,
        "association_strengthens_somewhere": bool((delta > 1e-12).any()),
        "association_weakens_somewhere": bool((delta < -1e-12).any()),
        "rank_reversal_observed": rank_reversals > 0,
        "definition_dependent_apparent_violation_observed": apparent_violations > 0,
        "coarsening_identifiability_matches_theory": (
            collapsed_counts == {expected_collapsed}
            and none_counts == {len(design["latent_definitions"])}
        ),
    }
    return {
        "status": "PASS" if all(gates.values()) else "FAIL",
        "design_name": design["design_name"],
        "design_cells": len(cells),
        "replications_per_cell": replications,
        "total_replications": len(rows),
        "seed": seed,
        "common_denominator_monotonicity_violations": common_violations,
        "positive_observed_delta_v_count": int((delta > 1e-12).sum()),
        "negative_observed_delta_v_count": int((delta < -1e-12).sum()),
        "observed_rank_reversal_count": rank_reversals,
        "definition_dependent_apparent_violation_count": apparent_violations,
        "identifiable_counts_without_coarsening": sorted(none_counts),
        "identifiable_counts_after_project_collapse": sorted(collapsed_counts),
        "gates": gates,
    }


def run_study(
    design: dict[str, Any],
    replications: int,
    seed: int,
    output: Path,
    max_cells: int | None = None,
) -> dict[str, Any]:
    if replications <= 0:
        raise ValueError("replications must be positive")
    cells = enumerate_design_cells(design)
    if max_cells is not None:
        if max_cells <= 0:
            raise ValueError("max_cells must be positive")
        cells = cells[:max_cells]

    master_rng = np.random.default_rng(seed)
    rows: list[dict[str, Any]] = []
    for cell in cells:
        for replication in range(1, replications + 1):
            replication_seed = int(master_rng.integers(0, np.iinfo(np.uint32).max))
            rows.append(
                simulate_replication(
                    design, cell, replication, replication_seed
                )
            )

    cell_summaries = summarise_cells(rows)
    global_summary = build_global_summary(
        design, cells, rows, replications, seed
    )

    output.mkdir(parents=True, exist_ok=True)
    _write_csv(output / "simulation_design_cells.csv", cells)
    _write_csv(output / "simulation_replication_metrics.csv", rows)
    _write_csv(output / "simulation_cell_summary.csv", cell_summaries)
    (output / "simulation_study_summary.json").write_text(
        json.dumps(global_summary, indent=2) + "\n", encoding="utf-8"
    )
    return global_summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", default=str(DEFAULT_DESIGN))
    parser.add_argument("--replications", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument(
        "--output", default=str(ROOT / "outputs_v3" / "simulation_study")
    )
    parser.add_argument("--max-cells", type=int)
    args = parser.parse_args()

    design = load_design(args.design)
    replications = (
        int(args.replications)
        if args.replications is not None
        else int(design["default_replications_per_cell"])
    )
    seed = int(args.seed) if args.seed is not None else int(design["seed"])
    summary = run_study(
        design,
        replications=replications,
        seed=seed,
        output=Path(args.output),
        max_cells=args.max_cells,
    )
    print(json.dumps(summary, indent=2))
    if summary["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
