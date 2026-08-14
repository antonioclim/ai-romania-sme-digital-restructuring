from __future__ import annotations

import math

from odsa.analysis import (
    association_diagnostics,
    definition_level,
    definition_relation,
    group_rate_diagnostics,
    ranking_reversal,
)
from odsa.claims import audit_claims
from odsa.models import Claim, OutcomeDefinition, StateSpace


SPACE = StateSpace(["active", "project", "other"])
ACTIVE = OutcomeDefinition("active", ["active"])
PROJECT = OutcomeDefinition("project", ["project"])
BROAD = OutcomeDefinition("broad", ["active", "project"])


def test_nested_level_monotonicity() -> None:
    counts = {"active": 11, "project": 7, "other": 22}
    active = definition_level(SPACE, counts, ACTIVE)
    broad = definition_level(SPACE, counts, BROAD)
    assert broad["numerator"] == active["numerator"] + counts["project"]
    assert broad["level"] >= active["level"]


def test_definition_relations() -> None:
    assert definition_relation(ACTIVE, BROAD) == "strict_subset"
    assert definition_relation(BROAD, ACTIVE) == "strict_superset"
    assert definition_relation(ACTIVE, PROJECT) == "disjoint"
    assert definition_relation(ACTIVE, ACTIVE) == "equal"


def test_claim_admissibility_blocks_silent_narrowing() -> None:
    claims = [
        Claim("active_claim", ["active"], "The case reports active use."),
        Claim(
            "broad_claim",
            ["active", "project"],
            "The case reports active use or project-stage engagement.",
        ),
    ]
    rows = audit_claims(SPACE, [ACTIVE, BROAD], claims)
    index = {(row["definition"], row["claim"]): row for row in rows}
    assert index[("active", "active_claim")]["admissible"] is True
    assert index[("broad", "active_claim")]["admissible"] is False
    assert index[("broad", "broad_claim")]["admissible"] is True


def test_association_is_not_monotone_under_broadening() -> None:
    counts = {
        "A": {"active": 20, "project": 1, "other": 19},
        "B": {"active": 5, "project": 25, "other": 10},
        "C": {"active": 10, "project": 5, "other": 25},
    }
    active = association_diagnostics(SPACE, counts, ACTIVE)
    broad = association_diagnostics(SPACE, counts, BROAD)
    assert not math.isclose(active["cramers_v"], broad["cramers_v"])


def test_ranking_reversal_detection() -> None:
    counts = {
        "A": {"active": 20, "project": 0, "other": 20},
        "B": {"active": 10, "project": 25, "other": 5},
        "C": {"active": 15, "project": 0, "other": 25},
    }
    active_rates = group_rate_diagnostics(SPACE, counts, ACTIVE)
    broad_rates = group_rate_diagnostics(SPACE, counts, BROAD)
    assert ranking_reversal(active_rates, broad_rates) is True
