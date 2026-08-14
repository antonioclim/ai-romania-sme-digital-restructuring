"""Outcome-Definition Sensitivity Analysis.

The public API intentionally exposes a compact set of validated primitives.
ODSA is non-scalar: it does not collapse level, composition, association,
recoverability and claim admissibility into one score.
"""

from .analysis import (
    association_diagnostics,
    definition_composition,
    definition_level,
    definition_relation,
    group_rate_diagnostics,
    ranking_reversal,
    ranking_signature,
    wilson_interval,
)
from .claims import audit_claims
from .coarsening import (
    coarsen_counts,
    coarsen_group_state_counts,
    coarsened_state_space,
    coarsening_is_injective,
    definition_recoverability,
    recover_coarse_definition,
)
from .models import Claim, ODSAValidationError, OutcomeDefinition, StateSpace
from .simulation import (
    COARSENING_MAPS,
    DEFINITIONS,
    FINE_STATE_SPACE,
    SimulationScenario,
    build_scenarios,
    misclassification_matrix,
    normalised_rank_distance,
    simulate_replicate,
)

__all__ = [
    "COARSENING_MAPS",
    "Claim",
    "DEFINITIONS",
    "FINE_STATE_SPACE",
    "ODSAValidationError",
    "OutcomeDefinition",
    "SimulationScenario",
    "StateSpace",
    "association_diagnostics",
    "audit_claims",
    "build_scenarios",
    "coarsen_counts",
    "coarsen_group_state_counts",
    "coarsened_state_space",
    "coarsening_is_injective",
    "definition_composition",
    "definition_level",
    "definition_recoverability",
    "definition_relation",
    "group_rate_diagnostics",
    "misclassification_matrix",
    "normalised_rank_distance",
    "ranking_reversal",
    "ranking_signature",
    "recover_coarse_definition",
    "simulate_replicate",
    "wilson_interval",
]

__version__ = "3.0.0rc1"
