"""Core diagnostics for Outcome-Definition Sensitivity Analysis."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from math import sqrt
from typing import Any

import numpy as np
from scipy.stats import chi2_contingency

from .models import ODSAValidationError, OutcomeDefinition, StateSpace


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
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
        * sqrt(proportion * (1.0 - proportion) / total + z * z / (4.0 * total * total))
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
    positive_total = int(sum(int(counts[state]) for state in definition.positive_states))
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


def cramers_v(table: Sequence[Sequence[int]]) -> dict[str, Any]:
    """Compute Pearson chi-square and bias-unadjusted Cramér's V."""

    array = np.asarray(table, dtype=int)
    if array.ndim != 2 or min(array.shape) < 2:
        raise ODSAValidationError("association table must be at least 2 x 2")
    if (array < 0).any():
        raise ODSAValidationError("association table must not contain negative counts")
    total = int(array.sum())
    if total <= 0:
        raise ODSAValidationError("association table must have a positive total")
    if (array.sum(axis=0) == 0).any() or (array.sum(axis=1) == 0).any():
        raise ODSAValidationError("association table must not contain empty margins")
    chi_square, p_value, degrees_freedom, expected = chi2_contingency(array, correction=False)
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
        numerator = int(sum(int(counts[state]) for state in definition.positive_states))
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


def ranking_signature(rows: Sequence[Mapping[str, Any]]) -> tuple[str, ...]:
    """Return a stable descending group ranking with lexical tie-breaking."""

    return tuple(
        str(row["group"])
        for row in sorted(rows, key=lambda row: (-float(row["rate"]), str(row["group"])))
    )


def ranking_reversal(
    left_rows: Sequence[Mapping[str, Any]],
    right_rows: Sequence[Mapping[str, Any]],
) -> bool:
    """Report whether two definitions imply different group orderings."""

    left_groups = {str(row["group"]) for row in left_rows}
    right_groups = {str(row["group"]) for row in right_rows}
    if left_groups != right_groups:
        raise ODSAValidationError("rankings must refer to the same groups")
    return ranking_signature(left_rows) != ranking_signature(right_rows)
