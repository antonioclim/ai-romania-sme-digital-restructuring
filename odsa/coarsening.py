"""Coarsening and recoverability diagnostics for ODSA.

A coarsening map sends each fine-grained observed state to one reported state.
A definition is recoverable after coarsening only when membership is constant
within every fibre of that map. This implements the information-loss boundary
used by ODSA rather than silently reconstructing distinctions that are no
longer present in the observed data.
"""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Mapping
from typing import Any

from .models import ODSAValidationError, OutcomeDefinition, StateSpace


def validate_coarsening(
    state_space: StateSpace,
    mapping: Mapping[str, str],
) -> OrderedDict[str, str]:
    """Validate and normalise a fine-state to reported-state mapping."""

    expected = set(state_space.states)
    supplied = set(mapping)
    missing = sorted(expected - supplied)
    extra = sorted(supplied - expected)
    if missing or extra:
        raise ODSAValidationError(
            f"coarsening map must cover the state space exactly; "
            f"missing={missing}, extra={extra}"
        )

    normalised: OrderedDict[str, str] = OrderedDict()
    for state in state_space.states:
        coarse = str(mapping[state]).strip()
        if not coarse:
            raise ODSAValidationError(
                f"coarsening target for state {state!r} must not be empty"
            )
        normalised[str(state)] = coarse
    return normalised


def coarsened_state_space(
    state_space: StateSpace,
    mapping: Mapping[str, str],
    *,
    label: str | None = None,
) -> StateSpace:
    """Return the reported state space induced by a coarsening map."""

    normalised = validate_coarsening(state_space, mapping)
    reported_states = list(dict.fromkeys(normalised.values()))
    return StateSpace(
        reported_states,
        label=label or f"Coarsened {state_space.label}",
    )


def coarsen_counts(
    state_space: StateSpace,
    counts: Mapping[str, int],
    mapping: Mapping[str, str],
) -> OrderedDict[str, int]:
    """Aggregate fine-state counts into reported-state counts."""

    state_space.validate_counts(counts)
    normalised = validate_coarsening(state_space, mapping)
    result: OrderedDict[str, int] = OrderedDict()
    for state in state_space.states:
        target = normalised[state]
        result[target] = result.get(target, 0) + int(counts[state])
    return result


def coarsen_group_state_counts(
    state_space: StateSpace,
    group_state_counts: Mapping[str, Mapping[str, int]],
    mapping: Mapping[str, str],
) -> OrderedDict[str, OrderedDict[str, int]]:
    """Apply the same coarsening map to every group table."""

    if not group_state_counts:
        raise ODSAValidationError("group-state counts must not be empty")
    result: OrderedDict[str, OrderedDict[str, int]] = OrderedDict()
    for group, counts in group_state_counts.items():
        name = str(group).strip()
        if not name:
            raise ODSAValidationError("group names must not be empty")
        result[name] = coarsen_counts(state_space, counts, mapping)
    return result


def definition_recoverability(
    state_space: StateSpace,
    definition: OutcomeDefinition,
    mapping: Mapping[str, str],
) -> dict[str, Any]:
    """Audit whether a fine-state definition survives a coarsening map.

    Membership must be constant within each reported-state fibre. When a fibre
    contains both positive and negative fine states, the definition cannot be
    recovered without an additional assumption or external information.
    """

    definition.validate(state_space)
    normalised = validate_coarsening(state_space, mapping)
    positive = set(definition.positive_states)

    fibres: OrderedDict[str, list[str]] = OrderedDict()
    for state in state_space.states:
        fibres.setdefault(normalised[state], []).append(state)

    ambiguous: list[dict[str, Any]] = []
    coarse_positive: list[str] = []
    for coarse_state, fine_states in fibres.items():
        memberships = {state in positive for state in fine_states}
        if len(memberships) > 1:
            ambiguous.append(
                {
                    "reported_state": coarse_state,
                    "fine_states": list(fine_states),
                    "positive_fine_states": [
                        state for state in fine_states if state in positive
                    ],
                    "negative_fine_states": [
                        state for state in fine_states if state not in positive
                    ],
                }
            )
        elif True in memberships:
            coarse_positive.append(coarse_state)

    return {
        "definition": definition.name,
        "recoverable": not ambiguous,
        "reported_positive_states": coarse_positive if not ambiguous else [],
        "ambiguous_reported_states": ambiguous,
    }


def recover_coarse_definition(
    state_space: StateSpace,
    definition: OutcomeDefinition,
    mapping: Mapping[str, str],
) -> OutcomeDefinition:
    """Return the exact reported-state definition or raise if it is lost."""

    audit = definition_recoverability(state_space, definition, mapping)
    if not audit["recoverable"]:
        names = [
            item["reported_state"]
            for item in audit["ambiguous_reported_states"]
        ]
        raise ODSAValidationError(
            f"definition {definition.name!r} is not recoverable after "
            f"coarsening; ambiguous reported states={names}"
        )
    return OutcomeDefinition(
        name=definition.name,
        positive_states=audit["reported_positive_states"],
        label=definition.label,
        intended_question=definition.intended_question,
    )


def coarsening_is_injective(
    state_space: StateSpace,
    mapping: Mapping[str, str],
) -> bool:
    """Return whether the map preserves every fine-state distinction."""

    normalised = validate_coarsening(state_space, mapping)
    return len(set(normalised.values())) == len(normalised)
