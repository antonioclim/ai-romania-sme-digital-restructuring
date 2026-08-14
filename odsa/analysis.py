"""Core diagnostics for Outcome-Definition Sensitivity Analysis."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from math import comb, isfinite, sqrt
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


def _rate_mapping(rows: Sequence[Mapping[str, Any]]) -> dict[str, float]:
    mapping: dict[str, float] = {}
    for row in rows:
        group = str(row["group"])
        if group in mapping:
            raise ODSAValidationError(f"duplicate group in rate rows: {group!r}")
        value = float(row["rate"])
        if not isfinite(value):
            raise ODSAValidationError("group rates must be finite")
        mapping[group] = value
    if len(mapping) < 2:
        raise ODSAValidationError("at least two groups are required for ranking diagnostics")
    return mapping


def ranking_signature(rows: Sequence[Mapping[str, Any]]) -> tuple[str, ...]:
    """Return a stable descending display order with lexical tie-breaking.

    The signature is intended for deterministic presentation. Substantive
    reversal detection uses :func:`pairwise_ranking_diagnostics`, which treats
    ties explicitly rather than allowing lexical tie-breaking to create a
    spurious reversal.
    """

    _rate_mapping(rows)
    return tuple(
        str(row["group"])
        for row in sorted(rows, key=lambda row: (-float(row["rate"]), str(row["group"])))
    )


def pairwise_ranking_diagnostics(
    left_rows: Sequence[Mapping[str, Any]],
    right_rows: Sequence[Mapping[str, Any]],
    *,
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Compare two group-rate orderings while handling ties explicitly.

    A strict reversal requires a pair of groups to be ordered in opposite
    directions under the two definitions. A tie appearing or disappearing is
    reported separately and is not, by itself, labelled a strict reversal.
    """

    if tolerance < 0:
        raise ODSAValidationError("ranking tolerance must be non-negative")
    left = _rate_mapping(left_rows)
    right = _rate_mapping(right_rows)
    if set(left) != set(right):
        raise ODSAValidationError("rankings must refer to the same groups")

    groups = sorted(left)
    total_pairs = comb(len(groups), 2)
    concordant = 0
    discordant = 0
    tied_both = 0
    tied_left_only = 0
    tied_right_only = 0

    def sign(value: float) -> int:
        if abs(value) <= tolerance:
            return 0
        return 1 if value > 0 else -1

    for index, first in enumerate(groups):
        for second in groups[index + 1 :]:
            left_sign = sign(left[first] - left[second])
            right_sign = sign(right[first] - right[second])
            if left_sign == 0 and right_sign == 0:
                tied_both += 1
            elif left_sign == 0:
                tied_left_only += 1
            elif right_sign == 0:
                tied_right_only += 1
            elif left_sign == right_sign:
                concordant += 1
            else:
                discordant += 1

    comparable_pairs = concordant + discordant
    normalised_discordance = (
        discordant / comparable_pairs if comparable_pairs else 0.0
    )
    tie_change_pairs = tied_left_only + tied_right_only
    return {
        "group_count": len(groups),
        "total_pairs": total_pairs,
        "comparable_pairs": comparable_pairs,
        "concordant_pairs": concordant,
        "discordant_pairs": discordant,
        "tied_under_both": tied_both,
        "tied_left_only": tied_left_only,
        "tied_right_only": tied_right_only,
        "tie_change_pairs": tie_change_pairs,
        "tie_change_share": tie_change_pairs / total_pairs,
        "strict_ranking_reversal": discordant > 0,
        "normalised_discordance": normalised_discordance,
    }


def ranking_reversal(
    left_rows: Sequence[Mapping[str, Any]],
    right_rows: Sequence[Mapping[str, Any]],
    *,
    tolerance: float = 1e-12,
) -> bool:
    """Report whether at least one group pair reverses strictly."""

    return bool(
        pairwise_ranking_diagnostics(
            left_rows,
            right_rows,
            tolerance=tolerance,
        )["strict_ranking_reversal"]
    )
