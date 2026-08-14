"""Controlled factorial simulation for the manuscript-final ODSA protocol.

The ``ci`` mode is a deterministic mechanics check. It is deliberately small
and must not be reported as the final simulation study. The ``full`` mode is a
candidate execution plan whose design remains subject to a later freeze and
hostile statistical audit.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from itertools import product
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from odsa.analysis import (
    association_diagnostics,
    definition_level,
    group_rate_diagnostics,
    pairwise_order_disagreement,
)
from odsa.models import ODSAValidationError, OutcomeDefinition, StateSpace


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "simulations" / "manuscript_protocol.yml"
DEFAULT_OUTPUT = ROOT / "outputs_v3" / "factorial_protocol"


def _as_probability_vector(
    values: Any,
    *,
    label: str,
    length: int,
) -> np.ndarray:
    vector = np.asarray(values, dtype=float)
    if vector.shape != (length,):
        raise ValueError(f"{label} must contain exactly {length} values")
    if not np.isfinite(vector).all() or (vector < 0).any() or (vector > 1).any():
        raise ValueError(f"{label} must contain finite probabilities in [0, 1]")
    return vector


def _validate_row_stochastic(
    matrix: Any,
    *,
    label: str,
    size: int,
) -> np.ndarray:
    array = np.asarray(matrix, dtype=float)
    if array.shape != (size, size):
        raise ValueError(f"{label} must be a {size} x {size} matrix")
    if not np.isfinite(array).all() or (array < 0).any() or (array > 1).any():
        raise ValueError(f"{label} must contain finite probabilities in [0, 1]")
    if not np.allclose(array.sum(axis=1), 1.0, atol=1e-12):
        raise ValueError(f"every row in {label} must sum to one")
    return array


def load_design(path: str | Path) -> dict[str, Any]:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("simulation protocol must be a YAML mapping")
    return payload


def validate_design(design: dict[str, Any]) -> dict[str, Any]:
    states = [str(value) for value in design["states"]]
    groups = [str(value) for value in design["groups"]]
    if len(states) < 3 or len(set(states)) != len(states):
        raise ValueError("the protocol requires at least three unique states")
    if len(groups) < 2 or len(set(groups)) != len(groups):
        raise ValueError("the protocol requires at least two unique groups")

    definitions = design["definitions"]
    for name, positive_states in definitions.items():
        if not positive_states:
            raise ValueError(f"definition {name!r} is empty")
        unknown = set(map(str, positive_states)) - set(states)
        if unknown:
            raise ValueError(
                f"definition {name!r} contains unknown states: {sorted(unknown)}"
            )

    primary = design["primary_contrast"]
    if primary["left"] not in definitions or primary["right"] not in definitions:
        raise ValueError("primary contrast refers to an unregistered definition")
    left_states = set(definitions[primary["left"]])
    right_states = set(definitions[primary["right"]])
    expected_relation = str(primary.get("expected_relation", "")).strip()
    actual_relation = (
        "equal"
        if left_states == right_states
        else "strict_subset"
        if left_states < right_states
        else "strict_superset"
        if left_states > right_states
        else "disjoint"
        if left_states.isdisjoint(right_states)
        else "overlap"
    )
    if expected_relation and actual_relation != expected_relation:
        raise ValueError(
            "primary contrast relation mismatch: "
            f"expected {expected_relation!r}, obtained {actual_relation!r}"
        )

    for name, multipliers in design["allocation_profiles"].items():
        vector = np.asarray(multipliers, dtype=float)
        if (
            vector.shape != (len(groups),)
            or not np.isfinite(vector).all()
            or (vector <= 0).any()
        ):
            raise ValueError(
                f"allocation profile {name!r} must contain positive group multipliers"
            )

    for name, spec in design["misclassification_profiles"].items():
        _validate_row_stochastic(
            spec["matrix"],
            label=f"misclassification profile {name!r}",
            size=len(states),
        )

    for name, spec in design["missingness_profiles"].items():
        _as_probability_vector(
            spec["state_probabilities"],
            label=f"missingness profile {name!r}",
            length=len(states),
        )

    for name, spec in design["scenarios"].items():
        probabilities = spec["probabilities"]
        if set(probabilities) != set(groups):
            raise ValueError(
                f"scenario {name!r} must specify exactly the registered groups"
            )
        for group in groups:
            vector = _as_probability_vector(
                probabilities[group],
                label=f"scenario {name!r}, group {group!r}",
                length=len(states),
            )
            if not math.isclose(float(vector.sum()), 1.0, abs_tol=1e-12):
                raise ValueError(
                    f"scenario {name!r}, group {group!r} must sum to one"
                )

    execution = design["execution"]
    for mode in ("full", "ci"):
        if int(execution[f"{mode}_replications_per_cell"]) <= 0:
            raise ValueError(f"{mode} replications must be positive")
        for size in execution[f"{mode}_sample_sizes_per_group"]:
            if int(size) <= 1:
                raise ValueError(f"{mode} sample sizes must exceed one")
        for profile in execution[f"{mode}_allocation_profiles"]:
            if profile not in design["allocation_profiles"]:
                raise ValueError(
                    f"unknown {mode} allocation profile {profile!r}"
                )
        for profile in execution[f"{mode}_misclassification_profiles"]:
            if profile not in design["misclassification_profiles"]:
                raise ValueError(
                    f"unknown {mode} misclassification profile {profile!r}"
                )
        for profile in execution[f"{mode}_missingness_profiles"]:
            if profile not in design["missingness_profiles"]:
                raise ValueError(
                    f"unknown {mode} missingness profile {profile!r}"
                )
        for scenario in execution[f"{mode}_scenarios"]:
            if scenario not in design["scenarios"]:
                raise ValueError(f"unknown {mode} scenario {scenario!r}")

    return {
        "status": "PASS",
        "schema_version": str(design["schema_version"]),
        "states": states,
        "groups": groups,
        "definition_count": len(definitions),
        "scenario_count": len(design["scenarios"]),
        "misclassification_profile_count": len(
            design["misclassification_profiles"]
        ),
        "missingness_profile_count": len(design["missingness_profiles"]),
    }


def _observed_counts(
    true_counts: np.ndarray,
    missingness: np.ndarray,
    misclassification: np.ndarray,
    rng: np.random.Generator,
) -> tuple[np.ndarray, int]:
    observed = np.zeros_like(true_counts)
    missing_total = 0
    for state_index, count in enumerate(true_counts):
        retained = int(
            rng.binomial(int(count), 1.0 - float(missingness[state_index]))
        )
        missing_total += int(count) - retained
        if retained:
            observed += rng.multinomial(
                retained,
                misclassification[state_index],
            )
    return observed, missing_total


def _as_group_mapping(
    groups: list[str],
    states: list[str],
    matrix: np.ndarray,
) -> dict[str, dict[str, int]]:
    return {
        group: {
            state: int(matrix[group_index, state_index])
            for state_index, state in enumerate(states)
        }
        for group_index, group in enumerate(groups)
    }


def _overall_mapping(
    states: list[str],
    matrix: np.ndarray,
) -> dict[str, int]:
    totals = matrix.sum(axis=0)
    return {state: int(totals[index]) for index, state in enumerate(states)}


def _definition_probabilities(
    group_probabilities: np.ndarray,
    definition: OutcomeDefinition,
    state_index: dict[str, int],
) -> np.ndarray:
    columns = [state_index[state] for state in definition.positive_states]
    return group_probabilities[:, columns].sum(axis=1)


def _population_level(
    group_weights: np.ndarray,
    positive_probabilities: np.ndarray,
) -> float:
    return float(np.dot(group_weights, positive_probabilities))


def _population_cramers_v(
    group_weights: np.ndarray,
    positive_probabilities: np.ndarray,
) -> float:
    """Return the population Cramér's V for group by binary outcome.

    The calculation operates on the joint probability table. It therefore does
    not depend on an arbitrary total sample size.
    """

    joint = np.column_stack(
        (
            group_weights * positive_probabilities,
            group_weights * (1.0 - positive_probabilities),
        )
    )
    row_margins = joint.sum(axis=1, keepdims=True)
    column_margins = joint.sum(axis=0, keepdims=True)
    expected = row_margins @ column_margins
    if (expected <= 0).any():
        return float("nan")
    phi2 = float(np.sum((joint - expected) ** 2 / expected))
    denominator = min(joint.shape[0] - 1, joint.shape[1] - 1)
    return math.sqrt(phi2 / denominator)


def _rates_from_probabilities(
    groups: list[str],
    positive_probabilities: np.ndarray,
    definition: OutcomeDefinition,
) -> list[dict[str, Any]]:
    return [
        {
            "definition": definition.name,
            "group": group,
            "rate": float(positive_probabilities[index]),
        }
        for index, group in enumerate(groups)
    ]


def _safe_level(
    state_space: StateSpace,
    counts: dict[str, int],
    definition: OutcomeDefinition,
) -> float:
    try:
        return float(definition_level(state_space, counts, definition)["level"])
    except (ODSAValidationError, ValueError, FloatingPointError):
        return float("nan")


def _safe_association(
    state_space: StateSpace,
    group_counts: dict[str, dict[str, int]],
    definition: OutcomeDefinition,
) -> float:
    try:
        return float(
            association_diagnostics(
                state_space,
                group_counts,
                definition,
            )["cramers_v"]
        )
    except (ODSAValidationError, ValueError, FloatingPointError):
        return float("nan")


def _safe_pairwise(
    state_space: StateSpace,
    group_counts: dict[str, dict[str, int]],
    left: OutcomeDefinition,
    right: OutcomeDefinition,
) -> dict[str, float]:
    try:
        left_rows = group_rate_diagnostics(
            state_space,
            group_counts,
            left,
        )
        right_rows = group_rate_diagnostics(
            state_space,
            group_counts,
            right,
        )
        result = pairwise_order_disagreement(left_rows, right_rows)
        return {
            "pairwise_disagreement_share": float(
                result["disagreement_share"]
            ),
            "strict_rank_reversal_share": float(
                result["strict_reversal_share"]
            ),
        }
    except (ODSAValidationError, ValueError, FloatingPointError):
        return {
            "pairwise_disagreement_share": float("nan"),
            "strict_rank_reversal_share": float("nan"),
        }


def _order_error(
    population_rows: list[dict[str, Any]],
    observed_rows: list[dict[str, Any]],
) -> float:
    try:
        return float(
            pairwise_order_disagreement(
                population_rows,
                observed_rows,
            )["disagreement_share"]
        )
    except (ODSAValidationError, ValueError, FloatingPointError):
        return float("nan")


def _quantile(values: list[float], q: float) -> float:
    array = np.asarray(
        [value for value in values if math.isfinite(value)],
        dtype=float,
    )
    return float(np.quantile(array, q)) if array.size else float("nan")


def _mean(values: list[float]) -> float:
    array = np.asarray(
        [value for value in values if math.isfinite(value)],
        dtype=float,
    )
    return float(array.mean()) if array.size else float("nan")


def _sd(values: list[float]) -> float:
    array = np.asarray(
        [value for value in values if math.isfinite(value)],
        dtype=float,
    )
    if array.size > 1:
        return float(array.std(ddof=1))
    if array.size == 1:
        return 0.0
    return float("nan")


def _event_summary(values: list[float]) -> tuple[float, float, int]:
    finite = np.asarray(
        [value for value in values if math.isfinite(value)],
        dtype=float,
    )
    if not finite.size:
        return float("nan"), float("nan"), 0
    proportion = float(finite.mean())
    mcse = math.sqrt(proportion * (1.0 - proportion) / finite.size)
    return proportion, mcse, int(finite.size)


def _cell_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    numeric = [
        "delta_level_broad_minus_active",
        "delta_cramers_v_broad_minus_active",
        "cross_definition_pairwise_disagreement_share",
        "cross_definition_strict_reversal_share",
        "added_state_share_of_right_positive",
        "project_share_of_broad_positive",
        "active_level_sampling_error",
        "broad_level_sampling_error",
        "active_level_observation_error",
        "broad_level_observation_error",
        "active_level_total_error",
        "broad_level_total_error",
        "active_association_sampling_error",
        "broad_association_sampling_error",
        "active_association_observation_error",
        "broad_association_observation_error",
        "active_association_total_error",
        "broad_association_total_error",
        "active_order_error_share",
        "broad_order_error_share",
        "missing_share",
    ]
    summary: dict[str, Any] = {
        key: rows[0][key]
        for key in (
            "mode",
            "scenario",
            "sample_size_per_group",
            "allocation_profile",
            "misclassification_profile",
            "missingness_profile",
        )
    }
    summary["replications"] = len(rows)
    for metric in numeric:
        values = [float(row[metric]) for row in rows]
        finite = [value for value in values if math.isfinite(value)]
        summary[f"defined_{metric}"] = len(finite)
        summary[f"undefined_{metric}"] = len(values) - len(finite)
        summary[f"mean_{metric}"] = _mean(values)
        summary[f"sd_{metric}"] = _sd(values)
        summary[f"q05_{metric}"] = _quantile(values, 0.05)
        summary[f"median_{metric}"] = _quantile(values, 0.50)
        summary[f"q95_{metric}"] = _quantile(values, 0.95)

    event_definitions = {
        "broad_association_stronger": [
            float(row["delta_cramers_v_broad_minus_active"] > 0)
            if math.isfinite(
                float(row["delta_cramers_v_broad_minus_active"])
            )
            else float("nan")
            for row in rows
        ],
        "any_cross_definition_pairwise_disagreement": [
            float(row["cross_definition_pairwise_disagreement_share"] > 0)
            if math.isfinite(
                float(row["cross_definition_pairwise_disagreement_share"])
            )
            else float("nan")
            for row in rows
        ],
        "any_cross_definition_strict_reversal": [
            float(row["cross_definition_strict_reversal_share"] > 0)
            if math.isfinite(
                float(row["cross_definition_strict_reversal_share"])
            )
            else float("nan")
            for row in rows
        ],
    }
    for event, values in event_definitions.items():
        estimate, mcse, defined = _event_summary(values)
        summary[f"probability_{event}"] = estimate
        summary[f"mcse_{event}"] = mcse
        summary[f"defined_{event}"] = defined

    return summary


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_protocol(
    design: dict[str, Any],
    *,
    mode: str,
    output: str | Path,
    replications_override: int | None = None,
    max_cells: int | None = None,
) -> dict[str, Any]:
    design_audit = validate_design(design)
    if mode not in {"ci", "full"}:
        raise ValueError("mode must be 'ci' or 'full'")
    execution = design["execution"]
    replications = int(
        replications_override
        if replications_override is not None
        else execution[f"{mode}_replications_per_cell"]
    )
    if replications <= 0:
        raise ValueError("replications must be positive")

    states = [str(value) for value in design["states"]]
    groups = [str(value) for value in design["groups"]]
    state_index = {state: index for index, state in enumerate(states)}
    state_space = StateSpace(states)
    definitions = {
        name: OutcomeDefinition(name, positive_states)
        for name, positive_states in design["definitions"].items()
    }
    left = definitions[design["primary_contrast"]["left"]]
    right = definitions[design["primary_contrast"]["right"]]

    cells = list(
        product(
            execution[f"{mode}_scenarios"],
            execution[f"{mode}_sample_sizes_per_group"],
            execution[f"{mode}_allocation_profiles"],
            execution[f"{mode}_misclassification_profiles"],
            execution[f"{mode}_missingness_profiles"],
        )
    )
    if max_cells is not None:
        if max_cells <= 0:
            raise ValueError("max_cells must be positive")
        cells = cells[:max_cells]

    replicate_rows: list[dict[str, Any]] = []
    rows_by_cell: dict[int, list[dict[str, Any]]] = defaultdict(list)
    base_seed = int(design["seed"])

    for cell_index, (
        scenario_name,
        sample_size,
        allocation_name,
        misclassification_name,
        missingness_name,
    ) in enumerate(cells):
        allocation = np.asarray(
            design["allocation_profiles"][allocation_name],
            dtype=float,
        )
        misclassification = _validate_row_stochastic(
            design["misclassification_profiles"][
                misclassification_name
            ]["matrix"],
            label=misclassification_name,
            size=len(states),
        )
        missingness = _as_probability_vector(
            design["missingness_profiles"][
                missingness_name
            ]["state_probabilities"],
            label=missingness_name,
            length=len(states),
        )
        scenario = design["scenarios"][scenario_name]["probabilities"]
        group_probabilities = np.asarray(
            [scenario[group] for group in groups],
            dtype=float,
        )
        group_ns = np.maximum(
            2,
            np.rint(float(sample_size) * allocation).astype(int),
        )
        group_weights = group_ns / group_ns.sum()

        population_left_probabilities = _definition_probabilities(
            group_probabilities,
            left,
            state_index,
        )
        population_right_probabilities = _definition_probabilities(
            group_probabilities,
            right,
            state_index,
        )
        population_left_level = _population_level(
            group_weights,
            population_left_probabilities,
        )
        population_right_level = _population_level(
            group_weights,
            population_right_probabilities,
        )
        population_left_v = _population_cramers_v(
            group_weights,
            population_left_probabilities,
        )
        population_right_v = _population_cramers_v(
            group_weights,
            population_right_probabilities,
        )
        population_left_rows = _rates_from_probabilities(
            groups,
            population_left_probabilities,
            left,
        )
        population_right_rows = _rates_from_probabilities(
            groups,
            population_right_probabilities,
            right,
        )
        population_cross_order = pairwise_order_disagreement(
            population_left_rows,
            population_right_rows,
        )

        rng = np.random.default_rng(
            np.random.SeedSequence([base_seed, cell_index])
        )

        for replication in range(1, replications + 1):
            true_matrix = np.vstack(
                [
                    rng.multinomial(
                        int(group_ns[group_index]),
                        group_probabilities[group_index],
                    )
                    for group_index in range(len(groups))
                ]
            )
            observed_matrix = np.zeros_like(true_matrix)
            missing_total = 0
            for group_index in range(len(groups)):
                observed, missing = _observed_counts(
                    true_matrix[group_index],
                    missingness,
                    misclassification,
                    rng,
                )
                observed_matrix[group_index] = observed
                missing_total += missing

            true_group_counts = _as_group_mapping(
                groups,
                states,
                true_matrix,
            )
            observed_group_counts = _as_group_mapping(
                groups,
                states,
                observed_matrix,
            )
            true_overall = _overall_mapping(states, true_matrix)
            observed_overall = _overall_mapping(states, observed_matrix)

            sampled_left_level = _safe_level(
                state_space,
                true_overall,
                left,
            )
            sampled_right_level = _safe_level(
                state_space,
                true_overall,
                right,
            )
            observed_left_level = _safe_level(
                state_space,
                observed_overall,
                left,
            )
            observed_right_level = _safe_level(
                state_space,
                observed_overall,
                right,
            )

            sampled_left_v = _safe_association(
                state_space,
                true_group_counts,
                left,
            )
            sampled_right_v = _safe_association(
                state_space,
                true_group_counts,
                right,
            )
            observed_left_v = _safe_association(
                state_space,
                observed_group_counts,
                left,
            )
            observed_right_v = _safe_association(
                state_space,
                observed_group_counts,
                right,
            )

            observed_cross_order = _safe_pairwise(
                state_space,
                observed_group_counts,
                left,
                right,
            )
            try:
                observed_left_rows = group_rate_diagnostics(
                    state_space,
                    observed_group_counts,
                    left,
                )
                observed_right_rows = group_rate_diagnostics(
                    state_space,
                    observed_group_counts,
                    right,
                )
                active_order_error = _order_error(
                    population_left_rows,
                    observed_left_rows,
                )
                broad_order_error = _order_error(
                    population_right_rows,
                    observed_right_rows,
                )
            except ODSAValidationError:
                active_order_error = float("nan")
                broad_order_error = float("nan")

            right_positive = int(
                sum(
                    observed_overall.get(state, 0)
                    for state in right.positive_states
                )
            )
            added_states = set(right.positive_states) - set(left.positive_states)
            added_positive = int(
                sum(observed_overall.get(state, 0) for state in added_states)
            )
            added_state_share = (
                added_positive / right_positive
                if right_positive
                else float("nan")
            )
            project_share = (
                int(observed_overall.get("project_stage", 0)) / right_positive
                if right_positive and "project_stage" in right.positive_states
                else float("nan")
            )
            true_total = int(true_matrix.sum())

            row = {
                "mode": mode,
                "cell_index": cell_index + 1,
                "replication": replication,
                "scenario": scenario_name,
                "sample_size_per_group": int(sample_size),
                "allocation_profile": allocation_name,
                "misclassification_profile": misclassification_name,
                "missingness_profile": missingness_name,
                **{
                    f"group_n_{group}": int(group_ns[index])
                    for index, group in enumerate(groups)
                },
                "total_true_n": true_total,
                "total_observed_n": int(observed_matrix.sum()),
                "missing_n": int(missing_total),
                "missing_share": missing_total / true_total,
                "population_active_level": population_left_level,
                "population_broad_level": population_right_level,
                "sampled_true_active_level": sampled_left_level,
                "sampled_true_broad_level": sampled_right_level,
                "observed_active_level": observed_left_level,
                "observed_broad_level": observed_right_level,
                "delta_level_broad_minus_active": (
                    observed_right_level - observed_left_level
                ),
                "active_level_sampling_error": (
                    sampled_left_level - population_left_level
                ),
                "broad_level_sampling_error": (
                    sampled_right_level - population_right_level
                ),
                "active_level_observation_error": (
                    observed_left_level - sampled_left_level
                ),
                "broad_level_observation_error": (
                    observed_right_level - sampled_right_level
                ),
                "active_level_total_error": (
                    observed_left_level - population_left_level
                ),
                "broad_level_total_error": (
                    observed_right_level - population_right_level
                ),
                "population_active_cramers_v": population_left_v,
                "population_broad_cramers_v": population_right_v,
                "sampled_true_active_cramers_v": sampled_left_v,
                "sampled_true_broad_cramers_v": sampled_right_v,
                "observed_active_cramers_v": observed_left_v,
                "observed_broad_cramers_v": observed_right_v,
                "delta_cramers_v_broad_minus_active": (
                    observed_right_v - observed_left_v
                ),
                "active_association_sampling_error": (
                    sampled_left_v - population_left_v
                ),
                "broad_association_sampling_error": (
                    sampled_right_v - population_right_v
                ),
                "active_association_observation_error": (
                    observed_left_v - sampled_left_v
                ),
                "broad_association_observation_error": (
                    observed_right_v - sampled_right_v
                ),
                "active_association_total_error": (
                    observed_left_v - population_left_v
                ),
                "broad_association_total_error": (
                    observed_right_v - population_right_v
                ),
                "population_cross_definition_pairwise_disagreement_share": float(
                    population_cross_order["disagreement_share"]
                ),
                "population_cross_definition_strict_reversal_share": float(
                    population_cross_order["strict_reversal_share"]
                ),
                "cross_definition_pairwise_disagreement_share": observed_cross_order[
                    "pairwise_disagreement_share"
                ],
                "cross_definition_strict_reversal_share": observed_cross_order[
                    "strict_rank_reversal_share"
                ],
                "active_order_error_share": active_order_error,
                "broad_order_error_share": broad_order_error,
                "added_state_share_of_right_positive": added_state_share,
                "project_share_of_broad_positive": project_share,
            }
            replicate_rows.append(row)
            rows_by_cell[cell_index].append(row)

    summary_rows = [
        _cell_summary(rows_by_cell[index])
        for index in sorted(rows_by_cell)
    ]
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_path / "factorial_replicates.csv",
        replicate_rows,
    )
    _write_csv(
        output_path / "factorial_cell_summary.csv",
        summary_rows,
    )
    (output_path / "protocol_snapshot.json").write_text(
        json.dumps(design, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    undefined_associations = sum(
        1
        for row in replicate_rows
        if not math.isfinite(float(row["observed_active_cramers_v"]))
        or not math.isfinite(float(row["observed_broad_cramers_v"]))
    )
    run_audit = {
        **design_audit,
        "mode": mode,
        "role": (
            "continuous-integration mechanics check"
            if mode == "ci"
            else "candidate full factorial execution"
        ),
        "seed": base_seed,
        "cell_count": len(cells),
        "replications_per_cell": replications,
        "replicate_row_count": len(replicate_rows),
        "summary_row_count": len(summary_rows),
        "undefined_observed_association_rows": undefined_associations,
        "manuscript_evidence": (
            False
            if mode == "ci"
            else "pending design freeze and hostile audit"
        ),
    }
    (output_path / "protocol_run_audit.json").write_text(
        json.dumps(run_audit, indent=2) + "\n",
        encoding="utf-8",
    )
    return run_audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--design",
        default=str(DEFAULT_DESIGN),
        help="YAML simulation protocol",
    )
    parser.add_argument(
        "--mode",
        choices=("ci", "full"),
        default="ci",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
    )
    parser.add_argument(
        "--replications",
        type=int,
        default=None,
        help="Testing override; do not use for manuscript reporting",
    )
    parser.add_argument(
        "--max-cells",
        type=int,
        default=None,
        help="Testing override; do not use for manuscript reporting",
    )
    args = parser.parse_args()

    design = load_design(args.design)
    audit = run_protocol(
        design,
        mode=args.mode,
        output=args.output,
        replications_override=args.replications,
        max_cells=args.max_cells,
    )
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
