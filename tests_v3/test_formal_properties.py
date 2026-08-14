"""Executable checks for the formal ODSA propositions."""

from __future__ import annotations

from collections import OrderedDict

import numpy as np

from odsa.analysis import (
    association_diagnostics,
    definition_composition,
    definition_level,
    group_rate_diagnostics,
    ranking_reversal,
)
from odsa.coarsening import (
    coarsen_counts,
    coarsening_is_injective,
    definition_recoverability,
    recover_coarse_definition,
)
from odsa.models import ODSAValidationError, OutcomeDefinition, StateSpace
from odsa.simulation import (
    COARSENING_MAPS,
    DEFINITIONS,
    FINE_STATE_SPACE,
    misclassification_matrix,
)


def test_nested_level_monotonicity_and_difference_identity() -> None:
    state_space = StateSpace(["a", "b", "c"])
    narrow = OutcomeDefinition("narrow", ["a"])
    broad = OutcomeDefinition("broad", ["a", "b"])
    rng = np.random.default_rng(20260814)

    for _ in range(200):
        values = rng.integers(0, 100, size=3)
        if values.sum() == 0:
            values[0] = 1
        counts = OrderedDict(zip(("a", "b", "c"), map(int, values)))
        narrow_result = definition_level(state_space, counts, narrow)
        broad_result = definition_level(state_space, counts, broad)
        assert narrow_result["level"] <= broad_result["level"]
        expected_difference = counts["b"] / sum(counts.values())
        assert abs(
            broad_result["level"]
            - narrow_result["level"]
            - expected_difference
        ) < 1e-12


def test_composition_identity_links_narrow_and_broad_levels() -> None:
    state_space = StateSpace(["a", "b", "c"])
    narrow = OutcomeDefinition("narrow", ["a"])
    broad = OutcomeDefinition("broad", ["a", "b"])
    counts = OrderedDict([("a", 20), ("b", 30), ("c", 50)])

    narrow_level = definition_level(state_space, counts, narrow)["level"]
    broad_level = definition_level(state_space, counts, broad)["level"]
    composition = {
        row["state"]: row["share_of_positive"]
        for row in definition_composition(state_space, counts, broad)
    }
    assert abs(narrow_level / broad_level - composition["a"]) < 1e-12


def test_association_is_not_monotone_under_broadening() -> None:
    state_space = StateSpace(["active", "project", "other"])
    narrow = OutcomeDefinition("active", ["active"])
    broad = OutcomeDefinition("broad", ["active", "project"])

    broad_stronger = OrderedDict(
        [
            (
                "Group 1",
                OrderedDict(
                    [("active", 20), ("project", 0), ("other", 80)]
                ),
            ),
            (
                "Group 2",
                OrderedDict(
                    [("active", 10), ("project", 50), ("other", 40)]
                ),
            ),
        ]
    )
    narrow_v = association_diagnostics(
        state_space,
        broad_stronger,
        narrow,
    )["cramers_v"]
    broad_v = association_diagnostics(
        state_space,
        broad_stronger,
        broad,
    )["cramers_v"]
    assert broad_v > narrow_v

    broad_weaker = OrderedDict(
        [
            (
                "Group 1",
                OrderedDict(
                    [("active", 20), ("project", 40), ("other", 40)]
                ),
            ),
            (
                "Group 2",
                OrderedDict(
                    [("active", 5), ("project", 55), ("other", 40)]
                ),
            ),
        ]
    )
    narrow_v = association_diagnostics(
        state_space,
        broad_weaker,
        narrow,
    )["cramers_v"]
    broad_v = association_diagnostics(
        state_space,
        broad_weaker,
        broad,
    )["cramers_v"]
    assert broad_v < narrow_v
    assert broad_v < 1e-12


def test_nested_definitions_can_reverse_group_ordering() -> None:
    state_space = StateSpace(["active", "project", "other"])
    narrow = OutcomeDefinition("active", ["active"])
    broad = OutcomeDefinition("broad", ["active", "project"])
    counts = OrderedDict(
        [
            (
                "Group 1",
                OrderedDict(
                    [("active", 30), ("project", 0), ("other", 70)]
                ),
            ),
            (
                "Group 2",
                OrderedDict(
                    [("active", 10), ("project", 50), ("other", 40)]
                ),
            ),
        ]
    )
    narrow_rates = group_rate_diagnostics(state_space, counts, narrow)
    broad_rates = group_rate_diagnostics(state_space, counts, broad)
    assert ranking_reversal(narrow_rates, broad_rates)


def test_coarsening_recoverability_matches_membership_constancy() -> None:
    mapping = COARSENING_MAPS["project_collapsed"]

    active_audit = definition_recoverability(
        FINE_STATE_SPACE,
        DEFINITIONS["active_use"],
        mapping,
    )
    implementation_audit = definition_recoverability(
        FINE_STATE_SPACE,
        DEFINITIONS["implementation"],
        mapping,
    )
    broad_audit = definition_recoverability(
        FINE_STATE_SPACE,
        DEFINITIONS["broad_engagement"],
        mapping,
    )

    assert active_audit["recoverable"]
    assert not implementation_audit["recoverable"]
    assert broad_audit["recoverable"]

    active_coarse = recover_coarse_definition(
        FINE_STATE_SPACE,
        DEFINITIONS["active_use"],
        mapping,
    )
    broad_coarse = recover_coarse_definition(
        FINE_STATE_SPACE,
        DEFINITIONS["broad_engagement"],
        mapping,
    )
    assert active_coarse.positive_states == frozenset({"active_use"})
    assert broad_coarse.positive_states == frozenset(
        {"active_use", "project_stage"}
    )


def test_binary_coarsening_destroys_active_use_recoverability() -> None:
    mapping = COARSENING_MAPS["binary_engaged"]
    audit = definition_recoverability(
        FINE_STATE_SPACE,
        DEFINITIONS["active_use"],
        mapping,
    )
    assert not audit["recoverable"]

    try:
        recover_coarse_definition(
            FINE_STATE_SPACE,
            DEFINITIONS["active_use"],
            mapping,
        )
    except ODSAValidationError:
        pass
    else:
        raise AssertionError("non-recoverable definition should raise")


def test_coarsening_preserves_total_count() -> None:
    counts = OrderedDict(
        [
            ("active_use", 10),
            ("deployment", 20),
            ("testing", 30),
            ("planning", 40),
            ("no_engagement", 50),
        ]
    )
    coarse = coarsen_counts(
        FINE_STATE_SPACE,
        counts,
        COARSENING_MAPS["project_collapsed"],
    )
    assert sum(coarse.values()) == sum(counts.values())
    assert coarse["project_stage"] == 90
    assert not coarsening_is_injective(
        FINE_STATE_SPACE,
        COARSENING_MAPS["project_collapsed"],
    )


def test_misclassification_matrices_are_row_stochastic() -> None:
    for kind, rate in (
        ("none", 0.0),
        ("adjacent_symmetric", 0.10),
        ("optimistic_project_to_active", 0.10),
        ("pessimistic_active_to_deployment", 0.10),
    ):
        matrix = misclassification_matrix(kind, rate)
        assert matrix.shape == (5, 5)
        assert np.all(matrix >= 0)
        assert np.allclose(matrix.sum(axis=1), 1.0)
