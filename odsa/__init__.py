"""Outcome-Definition Sensitivity Analysis.

The public API intentionally exposes a small set of validated primitives.  The
package is non-scalar: it does not collapse level, composition, association and
claim admissibility into one score.
"""

from .analysis import (
    association_diagnostics,
    definition_composition,
    definition_level,
    definition_relation,
    group_rate_diagnostics,
    wilson_interval,
)
from .claims import audit_claims
from .models import Claim, OutcomeDefinition, StateSpace

__all__ = [
    "Claim",
    "OutcomeDefinition",
    "StateSpace",
    "association_diagnostics",
    "audit_claims",
    "definition_composition",
    "definition_level",
    "definition_relation",
    "group_rate_diagnostics",
    "wilson_interval",
]

__version__ = "3.0.0rc1"
