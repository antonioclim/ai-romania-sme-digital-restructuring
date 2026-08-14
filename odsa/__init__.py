"""Outcome-Definition Sensitivity Analysis.

The public API intentionally exposes validated, non-scalar diagnostics. ODSA
keeps level, composition, association, subgroup ordering and claim
admissibility separate rather than collapsing them into one score.
"""

from .analysis import (
    association_contrast,
    association_diagnostics,
    composition_total_variation,
    composition_vector,
    definition_composition,
    definition_difference,
    definition_level,
    definition_level_contrast,
    definition_relation,
    group_rate_diagnostics,
    pairwise_order_disagreement,
    ranking_reversal,
    wilson_interval,
)
from .claims import audit_claims
from .models import Claim, OutcomeDefinition, StateSpace

__all__ = [
    "Claim",
    "OutcomeDefinition",
    "StateSpace",
    "association_contrast",
    "association_diagnostics",
    "audit_claims",
    "composition_total_variation",
    "composition_vector",
    "definition_composition",
    "definition_difference",
    "definition_level",
    "definition_level_contrast",
    "definition_relation",
    "group_rate_diagnostics",
    "pairwise_order_disagreement",
    "ranking_reversal",
    "wilson_interval",
]

__version__ = "3.0.0rc1"
