"""Conservative claim-admissibility audit for ODSA."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .models import Claim, OutcomeDefinition, StateSpace


def audit_claims(
    state_space: StateSpace,
    definitions: Iterable[OutcomeDefinition],
    claims: Iterable[Claim],
) -> list[dict[str, Any]]:
    """Evaluate every definition–claim pair.

    A pair passes only when all states counted as positive by the definition are
    compatible with the wording of the claim.  The audit does not certify that
    the source instrument validly measures the claim; it only blocks semantic
    narrowing that is already visible from the registered state mapping.
    """

    definitions = list(definitions)
    claims = list(claims)
    for definition in definitions:
        definition.validate(state_space)
    for claim in claims:
        claim.validate(state_space)

    rows: list[dict[str, Any]] = []
    for definition in definitions:
        for claim in claims:
            incompatible = sorted(
                set(definition.positive_states) - set(claim.allowed_positive_states)
            )
            admissible = not incompatible
            rows.append(
                {
                    "definition": definition.name,
                    "claim": claim.name,
                    "claim_wording": claim.wording,
                    "admissible": admissible,
                    "incompatible_positive_states": incompatible,
                    "reason": (
                        "All positive states are compatible with the claim wording."
                        if admissible
                        else "The definition includes positive states that do not meet the claim wording."
                    ),
                }
            )
    return rows
