"""Core diagnostics for Outcome-Definition Sensitivity Analysis."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from itertools import combinations
from math import sqrt
from typing import Any

import numpy as np
from scipy.stats import chi2_contingency

from .models import ODSAValidationError, OutcomeDefinition, StateSpace


def wilson_interval(
    successes: int,
    total: int,
    z: float = 1.959963984540054,
) -> tuple[float, float]:
    """Return a Wilson score interval on the 0–1 scale."""

    successes = int(successes)
    total = int(total)
    if total <= 0:
        raise ODSAValidationError("total must be positive")
    if successes < 0 or successes > total:
        raise ODSAValidationError("successes must fall between zero and total")
    proportion = successes / total
    denominator = 1.0 + z * z / total
    centre = (proportion + z * z / (2.0 * total)) / denominator
    half_width = (
        z
        * sqrt(
            proportion * (1.0 - proportion) / total
            + z * z / (4.0 * total * total)
        )
        / denominator
    )
    return centre - half_width, centre + half_width


def _validate_definition(
    state_space: StateSpace,
    definition: OutcomeDefinition,
    counts: Mapping[str, int],
) -> None:
    state_space.validate_counts(counts)
    definition.validate(state_space)


def definition_level(
    state_space: StateSpace,
    counts: Mapping[str, int],
    definition: OutcomeDefinition,
) -> dict[str, Any]:
    """Compute the level, numerator, denominator and Wilson interval."""

    _validate_definition(state_space, definition, counts)
    denominator = int(sum(int(value) for value in counts.values()))
    if denominator <= 0:
        raise ODSAValidationError("state counts must have a positive total")
    numerator = int(sum(int(counts[state]) for state in definition.positive_states))
    low, high = wilson_interval(numerator, denominator)
    return {
        "definition": definition.name,
        "label": definition.label,
        "numerator": numerator,
        "denominator": denominator,
        "level": numerator / denominator,
        "ci95_low": low,
        "ci95_high": high,
    }


def definition_composition(
    state_space: StateSpace,
    counts: Mapping[str, int],
    definition: OutcomeDefinition,
) -> list[dict[str, Any]]:
    """Decompose a positive class into its contributing observed states."""

    _validate_definition(state_space, definition, counts)
    positive_total = int(
        sum(int(counts[state]) for state in definition.positive_states)
    )
    if positive_total <= 0:
        return [
            {
                "definition": definition.name,
                "state": state,
                "count": int(counts[state]),
                "share_of_positive": None,
            }
            for state in sorted(definition.positive_states)
        ]
    return [
        {
            "definition": definition.name,
            "state": state,
            "count": int(counts[state]),
            "share_of_positive": int(counts[state]) / positive_total,
        }
        for state in sorted(definition.positive_states)
    ]


def definition_relation(left: OutcomeDefinition, right: OutcomeDefinition) -> str:
    """Classify the set relation between two registered definitions."""

    a = set(left.positive_states)
    b = set(right.positive_states)
    if a == b:
        return "equal"
    if a < b:
        return "strict_subset"
    if a > b:
        return "strict_superset"
    if a.isdisjoint(b):
        return "disjoint"
    return "overlap"


def definition_difference(
    left: OutcomeDefinition,
    right: OutcomeDefinition,
) -> dict[str, Any]:
    """Return an exact set decomposition for two outcome definitions."""

    left_states = set(left.positive_states)
    right_states = set(right.positive_states)
    return {
        "left_definition": left.name,
        "right_definition": right.name,
        "relation": definition_relation(left, right),
        "shared_positive_states": sorted(left_states & right_states),
        "left_only_states": sorted(left_states - right_states),
        "right_only_states": sorted(right_states - left_states),
    }


def definition_level_contrast(
    state_space: StateSpace,
    counts: Mapping[str, int],
    left: OutcomeDefinition,
    right: OutcomeDefinition,
) -> dict[str, Any]:
    r"""Decompose the right-minus-left level contrast by symmetric difference.

    For any two definitions, nested or not,

    ``L(right) - L(left) = P(right \ left) - P(left \ right)``.

    The identity is exact under a common denominator. It is not a sampling or
    causal claim.
    """

    _validate_definition(state_space, left, counts)
    right.validate(state_space)
    denominator = int(sum(int(value) for value in counts.values()))
    if denominator <= 0:
        raise ODSAValidationError("state counts must have a positive total")

    left_states = set(left.positive_states)
    right_states = set(right.positive_states)
    left_n = int(sum(int(counts[state]) for state in left_states))
    right_n = int(sum(int(counts[state]) for state in right_states))
    left_only_n = int(
        sum(int(counts[state]) for state in left_states - right_states)
    )
    right_only_n = int(
        sum(int(counts[state]) for state in right_states - left_states)
    )
    delta_n = right_n - left_n
    decomposed_delta_n = right_only_n - left_only_n
    if delta_n != decomposed_delta_n:
        raise AssertionError("symmetric-difference level identity failed")

    return {
        **definition_difference(left, right),
        "denominator": denominator,
        "left_n": left_n,
        "right_n": right_n,
        "left_level": left_n / denominator,
        "right_level": right_n / denominator,
        "delta_n_right_minus_left": delta_n,
        "delta_level_right_minus_left": delta_n / denominator,
        "left_only_n": left_only_n,
        "right_only_n": right_only_n,
        "left_only_mass": left_only_n / denominator,
        "right_only_mass": right_only_n / denominator,
        "decomposition_residual": 0.0,
    }


def composition_vector(
    state_space: StateSpace,
    counts: Mapping[str, int],
    definition: OutcomeDefinition,
) -> dict[str, float]:
    """Return positive-class composition over the full registered state space."""

    _validate_definition(state_space, definition, counts)
    positive_total = int(
        sum(int(counts[state]) for state in definition.positive_states)
    )
    if positive_total <= 0:
        raise ODSAValidationError(
            f"definition {definition.name!r} has no positive observations; "
            "composition is undefined"
        )
    return {
        state: (
            int(counts[state]) / positive_total
            if state in definition.positive_states
            else 0.0
        )
        for state in sorted(state_space.states)
    }


def composition_total_variation(
    state_space: StateSpace,
    counts: Mapping[str, int],
    left: OutcomeDefinition,
    right: OutcomeDefinition,
) -> dict[str, Any]:
    """Compare positive-state compositions using total variation distance.

    The result is a descriptive diagnostic on the 0–1 scale, not a validity
    score and not a thresholded test. Disjoint definitions have distance one
    by construction when both positive classes are non-empty.
    """

    left_vector = composition_vector(state_space, counts, left)
    right_vector = composition_vector(state_space, counts, right)
    distance = 0.5 * sum(
        abs(left_vector[state] - right_vector[state])
        for state in sorted(state_space.states)
    )
    return {
        "left_definition": left.name,
        "right_definition": right.name,
        "total_variation_distance": float(distance),
        "left_composition": left_vector,
        "right_composition": right_vector,
    }


def cramers_v(table: Sequence[Sequence[int]]) -> dict[str, Any]:
    """Compute Pearson chi-square and bias-unadjusted Cramér's V."""

    array = np.asarray(table, dtype=int)
    if array.ndim != 2 or min(array.shape) < 2:
        raise ODSAValidationError("association table must be at least 2 x 2")
    if (array < 0).any():
        raise ODSAValidationError(
            "association table must not contain negative counts"
        )
    total = int(array.sum())
    if total <= 0:
        raise ODSAValidationError("association table must have a positive total")
    if (array.sum(axis=0) == 0).any() or (array.sum(axis=1) == 0).any():
        raise ODSAValidationError(
            "association table must not contain empty margins"
        )
    chi_square, p_value, degrees_freedom, expected = chi2_contingency(
        array,
        correction=False,
    )
    denominator = min(array.shape[0] - 1, array.shape[1] - 1)
    value = sqrt(float(chi_square) / (total * denominator))
    return {
        "n": total,
        "chi_square": float(chi_square),
        "degrees_freedom": int(degrees_freedom),
        "p_value": float(p_value),
        "cramers_v": float(value),
        "minimum_expected_count": float(expected.min()),
        "all_expected_at_least_5": bool((expected >= 5).all()),
    }


def _validate_group_state_counts(
    state_space: StateSpace,
    group_state_counts: Mapping[str, Mapping[str, int]],
) -> None:
    if len(group_state_counts) < 2:
        raise ODSAValidationError("at least two groups are required")
    for group, counts in group_state_counts.items():
        if not str(group).strip():
            raise ODSAValidationError("group names must not be empty")
        state_space.validate_counts(counts)
        if sum(int(value) for value in counts.values()) <= 0:
            raise ODSAValidationError(f"group {group!r} has no observations")


def group_rate_diagnostics(
    state_space: StateSpace,
    group_state_counts: Mapping[str, Mapping[str, int]],
    definition: OutcomeDefinition,
) -> list[dict[str, Any]]:
    """Compute definition-specific positive rates for every group."""

    definition.validate(state_space)
    _validate_group_state_counts(state_space, group_state_counts)
    rows: list[dict[str, Any]] = []
    for group, counts in group_state_counts.items():
        denominator = int(sum(int(value) for value in counts.values()))
        numerator = int(
            sum(int(counts[state]) for state in definition.positive_states)
        )
        low, high = wilson_interval(numerator, denominator)
        rows.append(
            {
                "definition": definition.name,
                "group": group,
                "numerator": numerator,
                "denominator": denominator,
                "rate": numerator / denominator,
                "ci95_low": low,
                "ci95_high": high,
            }
        )
    return rows


def association_diagnostics(
    state_space: StateSpace,
    group_state_counts: Mapping[str, Mapping[str, int]],
    definition: OutcomeDefinition,
) -> dict[str, Any]:
    """Compute association between group membership and a binary definition."""

    rates = group_rate_diagnostics(state_space, group_state_counts, definition)
    table = [
        [row["numerator"], row["denominator"] - row["numerator"]]
        for row in rates
    ]
    result = cramers_v(table)
    result.update(
        {
            "definition": definition.name,
            "label": definition.label,
            "groups": [row["group"] for row in rates],
        }
    )
    return result


def association_contrast(
    state_space: StateSpace,
    group_state_counts: Mapping[str, Mapping[str, int]],
    left: OutcomeDefinition,
    right: OutcomeDefinition,
) -> dict[str, Any]:
    """Report the right-minus-left contrast in a prespecified association measure."""

    left_result = association_diagnostics(
        state_space,
        group_state_counts,
        left,
    )
    right_result = association_diagnostics(
        state_space,
        group_state_counts,
        right,
    )
    return {
        "left_definition": left.name,
        "right_definition": right.name,
        "left_cramers_v": left_result["cramers_v"],
        "right_cramers_v": right_result["cramers_v"],
        "delta_cramers_v_right_minus_left": (
            right_result["cramers_v"] - left_result["cramers_v"]
        ),
        "left_minimum_expected_count": left_result["minimum_expected_count"],
        "right_minimum_expected_count": right_result[
            "minimum_expected_count"
        ],
    }


def ranking_signature(rows: Sequence[Mapping[str, Any]]) -> tuple[str, ...]:
    """Return a stable descending group ranking with lexical tie-breaking."""

    return tuple(
        str(row["group"])
        for row in sorted(
            rows,
            key=lambda row: (-float(row["rate"]), str(row["group"])),
        )
    )


def ranking_reversal(
    left_rows: Sequence[Mapping[str, Any]],
    right_rows: Sequence[Mapping[str, Any]],
) -> bool:
    """Report whether two definitions imply different complete group orderings."""

    left_groups = {str(row["group"]) for row in left_rows}
    right_groups = {str(row["group"]) for row in right_rows}
    if left_groups != right_groups:
        raise ODSAValidationError("rankings must refer to the same groups")
    return ranking_signature(left_rows) != ranking_signature(right_rows)


def _rate_sign(left: float, right: float, tolerance: float) -> int:
    difference = float(left) - float(right)
    if abs(difference) <= tolerance:
        return 0
    return 1 if difference > 0 else -1


def pairwise_order_disagreement(
    left_rows: Sequence[Mapping[str, Any]],
    right_rows: Sequence[Mapping[str, Any]],
    *,
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Quantify pairwise subgroup-order instability without arbitrary tie-breaking."""

    if tolerance < 0:
        raise ODSAValidationError("tolerance must be non-negative")
    left = {str(row["group"]): float(row["rate"]) for row in left_rows}
    right = {str(row["group"]): float(row["rate"]) for row in right_rows}
    if set(left) != set(right):
        raise ODSAValidationError("rankings must refer to the same groups")
    if len(left) < 2:
        raise ODSAValidationError("at least two groups are required")

    pair_rows: list[dict[str, Any]] = []
    strict_reversals = 0
    tie_changes = 0
    concordant = 0
    for first, second in combinations(sorted(left), 2):
        left_sign = _rate_sign(left[first], left[second], tolerance)
        right_sign = _rate_sign(right[first], right[second], tolerance)
        if left_sign == right_sign:
            status = "concordant"
            concordant += 1
        elif left_sign == 0 or right_sign == 0:
            status = "tie_change"
            tie_changes += 1
        else:
            status = "strict_reversal"
            strict_reversals += 1
        pair_rows.append(
            {
                "first_group": first,
                "second_group": second,
                "left_sign": left_sign,
                "right_sign": right_sign,
                "status": status,
            }
        )

    total_pairs = len(pair_rows)
    disagreements = strict_reversals + tie_changes
    return {
        "total_pairs": total_pairs,
        "concordant_pairs": concordant,
        "strict_reversal_pairs": strict_reversals,
        "tie_change_pairs": tie_changes,
        "disagreement_pairs": disagreements,
        "strict_reversal_share": strict_reversals / total_pairs,
        "disagreement_share": disagreements / total_pairs,
        "pair_details": pair_rows,
    }
