from __future__ import annotations

import math

from odsa.analysis import (
    association_contrast,
    composition_total_variation,
    definition_level_contrast,
    group_rate_diagnostics,
    pairwise_order_disagreement,
)
from odsa.claims import audit_claims
from odsa.models import Claim, OutcomeDefinition, StateSpace


SPACE = StateSpace(["active", "project", "other"])
ACTIVE = OutcomeDefinition("active", ["active"])
PROJECT = OutcomeDefinition("project", ["project"])
BROAD = OutcomeDefinition("broad", ["active", "project"])


def test_symmetric_difference_identity_for_nested_definitions() -> None:
    counts = {"active": 54, "project": 51, "other": 67}
    contrast = definition_level_contrast(SPACE, counts, ACTIVE, BROAD)
    assert contrast["relation"] == "strict_subset"
    assert contrast["left_only_n"] == 0
    assert contrast["right_only_n"] == 51
    assert contrast["delta_n_right_minus_left"] == 51
    assert math.isclose(contrast["delta_level_right_minus_left"], 51 / 172)


def test_symmetric_difference_identity_for_non_nested_definitions() -> None:
    counts = {"active": 17, "project": 11, "other": 22}
    contrast = definition_level_contrast(SPACE, counts, ACTIVE, PROJECT)
    assert contrast["relation"] == "disjoint"
    assert contrast["left_only_n"] == 17
    assert contrast["right_only_n"] == 11
    assert contrast["delta_n_right_minus_left"] == -6


def test_association_can_increase_under_nested_broadening() -> None:
    counts = {
        "G1": {"active": 10, "project": 0, "other": 90},
        "G2": {"active": 10, "project": 80, "other": 10},
    }
    contrast = association_contrast(SPACE, counts, ACTIVE, BROAD)
    assert math.isclose(contrast["left_cramers_v"], 0.0, abs_tol=1e-12)
    assert contrast["right_cramers_v"] > 0.7
    assert contrast["delta_cramers_v_right_minus_left"] > 0


def test_association_can_decrease_under_nested_broadening() -> None:
    counts = {
        "G1": {"active": 90, "project": 0, "other": 10},
        "G2": {"active": 10, "project": 80, "other": 10},
    }
    contrast = association_contrast(SPACE, counts, ACTIVE, BROAD)
    assert contrast["left_cramers_v"] > 0.7
    assert math.isclose(contrast["right_cramers_v"], 0.0, abs_tol=1e-12)
    assert contrast["delta_cramers_v_right_minus_left"] < 0


def test_pairwise_order_diagnostic_detects_strict_reversal() -> None:
    counts = {
        "G1": {"active": 60, "project": 0, "other": 40},
        "G2": {"active": 50, "project": 50, "other": 0},
    }
    active_rows = group_rate_diagnostics(SPACE, counts, ACTIVE)
    broad_rows = group_rate_diagnostics(SPACE, counts, BROAD)
    result = pairwise_order_disagreement(active_rows, broad_rows)
    assert result["total_pairs"] == 1
    assert result["strict_reversal_pairs"] == 1
    assert result["disagreement_share"] == 1.0


def test_pairwise_order_diagnostic_separates_tie_change() -> None:
    left_rows = [
        {"group": "A", "rate": 0.4},
        {"group": "B", "rate": 0.4},
    ]
    right_rows = [
        {"group": "A", "rate": 0.5},
        {"group": "B", "rate": 0.4},
    ]
    result = pairwise_order_disagreement(left_rows, right_rows)
    assert result["tie_change_pairs"] == 1
    assert result["strict_reversal_pairs"] == 0


def test_composition_total_variation_is_bounded_and_symmetric() -> None:
    counts = {"active": 54, "project": 51, "other": 67}
    left = composition_total_variation(SPACE, counts, ACTIVE, BROAD)
    right = composition_total_variation(SPACE, counts, BROAD, ACTIVE)
    assert 0.0 <= left["total_variation_distance"] <= 1.0
    assert math.isclose(
        left["total_variation_distance"],
        right["total_variation_distance"],
    )
    assert math.isclose(left["total_variation_distance"], 51 / 105)


def test_claim_admissibility_is_downward_closed() -> None:
    claim = Claim(
        "broad_claim",
        ["active", "project"],
        "The case reports active use or project-stage engagement.",
    )
    rows = audit_claims(SPACE, [BROAD, ACTIVE, PROJECT], [claim])
    assert all(row["admissible"] is True for row in rows)


def test_narrow_claim_does_not_survive_broadening() -> None:
    claim = Claim("active_claim", ["active"], "The case reports active use.")
    rows = audit_claims(SPACE, [ACTIVE, BROAD], [claim])
    by_definition = {row["definition"]: row for row in rows}
    assert by_definition["active"]["admissible"] is True
    assert by_definition["broad"]["admissible"] is False
