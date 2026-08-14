"""Formal properties and coarsening diagnostics for ODSA.

The functions in this module implement properties that are independent of any
particular empirical application. They deliberately avoid collapsing the
method's diagnostics into one scalar score.
"""

from __future__ import annotations

from collections import OrderedDict, defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

from .models import ODSAValidationError, OutcomeDefinition, StateSpace


def exact_level_increment(
    state_space: StateSpace,
    counts: Mapping[str, int],
    narrower: OutcomeDefinition,
    broader: OutcomeDefinition,
) -> dict[str, Any]:
    """Return the exact level increment for two nested definitions.

    With a common denominator and ``narrower ⊆ broader``, the increment equals
    the observed mass of the added states divided by the common denominator.
    """

    state_space.validate_counts(counts)
    narrower.validate(state_space)
    broader.validate(state_space)
    narrow_states = set(narrower.positive_states)
    broad_states = set(broader.positive_states)
    if not narrow_states <= broad_states:
        raise ODSAValidationError("narrower must be a subset of broader")

    denominator = int(sum(int(value) for value in counts.values()))
    if denominator <= 0:
        raise ODSAValidationError("state counts must have a positive total")

    added_states = sorted(broad_states - narrow_states)
    added_count = int(sum(int(counts[state]) for state in added_states))
    narrow_count = int(sum(int(counts[state]) for state in narrow_states))
    broad_count = int(sum(int(counts[state]) for state in broad_states))
    increment = added_count / denominator

    return {
        "narrower": narrower.name,
        "broader": broader.name,
        "denominator": denominator,
        "narrow_count": narrow_count,
        "broad_count": broad_count,
        "added_states": added_states,
        "added_count": added_count,
        "narrow_level": narrow_count / denominator,
        "broad_level": broad_count / denominator,
        "increment": increment,
        "identity_holds": broad_count - narrow_count == added_count,
        "monotonicity_holds": broad_count >= narrow_count,
    }


def coarsen_counts(
    state_space: StateSpace,
    counts: Mapping[str, int],
    mapping: Mapping[str, str],
) -> OrderedDict[str, int]:
    """Aggregate fine-state counts through a complete many-to-one mapping."""

    state_space.validate_counts(counts)
    state_keys = set(state_space.states)
    mapping_keys = set(mapping)
    if mapping_keys != state_keys:
        missing = sorted(state_keys - mapping_keys)
        extra = sorted(mapping_keys - state_keys)
        raise ODSAValidationError(
            f"coarsening mapping must cover exactly the state space; missing={missing}, extra={extra}"
        )

    coarsened: OrderedDict[str, int] = OrderedDict()
    for state in sorted(state_keys):
        observed = str(mapping[state]).strip()
        if not observed:
            raise ODSAValidationError("coarsened state labels must not be empty")
        coarsened.setdefault(observed, 0)
        coarsened[observed] += int(counts[state])
    return coarsened


def definition_identifiability(
    definition: OutcomeDefinition,
    mapping: Mapping[str, str],
) -> dict[str, Any]:
    """Audit whether a fine-state definition survives a coarsening map.

    A definition is identifiable after coarsening if and only if its positive
    state set is a union of complete fibres of the mapping. A split fibre
    contains both positive and negative fine states and therefore destroys the
    definition without additional information or assumptions.
    """

    latent_states = set(mapping)
    positive_states = set(definition.positive_states)
    if not positive_states <= latent_states:
        unknown = sorted(positive_states - latent_states)
        raise ODSAValidationError(f"definition contains states absent from mapping: {unknown}")

    fibres: dict[str, set[str]] = defaultdict(set)
    for latent, observed in mapping.items():
        label = str(observed).strip()
        if not label:
            raise ODSAValidationError("coarsened state labels must not be empty")
        fibres[label].add(latent)

    positive_observed_states: list[str] = []
    split_fibres: list[dict[str, Any]] = []
    for observed in sorted(fibres):
        fibre = fibres[observed]
        positive = sorted(fibre & positive_states)
        negative = sorted(fibre - positive_states)
        if positive and negative:
            split_fibres.append(
                {
                    "observed_state": observed,
                    "positive_latent_states": positive,
                    "negative_latent_states": negative,
                }
            )
        elif positive:
            positive_observed_states.append(observed)

    return {
        "definition": definition.name,
        "identifiable": not split_fibres,
        "positive_observed_states": positive_observed_states if not split_fibres else None,
        "split_fibres": split_fibres,
    }


def identifiability_register(
    definitions: Sequence[OutcomeDefinition],
    mapping: Mapping[str, str],
) -> list[dict[str, Any]]:
    """Return identifiability diagnostics for a registered definition set."""

    return [definition_identifiability(definition, mapping) for definition in definitions]


def common_denominator_monotonicity(
    state_space: StateSpace,
    counts: Mapping[str, int],
    narrower: OutcomeDefinition,
    broader: OutcomeDefinition,
) -> bool:
    """Verify the nested-level monotonicity invariant on one analysis set."""

    return bool(
        exact_level_increment(state_space, counts, narrower, broader)[
            "monotonicity_holds"
        ]
    )
