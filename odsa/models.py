"""Validated domain models for Outcome-Definition Sensitivity Analysis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


class ODSAValidationError(ValueError):
    """Raised when an ODSA state space, definition or claim is invalid."""


def _normalise_names(values: Iterable[str], *, field: str) -> frozenset[str]:
    result = frozenset(str(value).strip() for value in values if str(value).strip())
    if not result:
        raise ODSAValidationError(f"{field} must contain at least one non-empty value")
    return result


@dataclass(frozen=True, slots=True)
class StateSpace:
    """Finite set of mutually exclusive observed states.

    ODSA requires an explicit state register.  A state may be coarsened by the
    source instrument, but that loss of distinction must be declared rather
    than silently repaired after collection.
    """

    states: frozenset[str]
    label: str = "Observed state space"

    def __init__(self, states: Iterable[str], label: str = "Observed state space"):
        object.__setattr__(self, "states", _normalise_names(states, field="states"))
        object.__setattr__(self, "label", str(label).strip() or "Observed state space")

    def validate_counts(self, counts: Mapping[str, int]) -> None:
        unknown = set(counts) - set(self.states)
        missing = set(self.states) - set(counts)
        if unknown:
            raise ODSAValidationError(f"counts contain unknown states: {sorted(unknown)}")
        if missing:
            raise ODSAValidationError(f"counts omit registered states: {sorted(missing)}")
        for state, value in counts.items():
            if isinstance(value, bool) or int(value) != value or int(value) < 0:
                raise ODSAValidationError(
                    f"count for state {state!r} must be a non-negative integer"
                )


@dataclass(frozen=True, slots=True)
class OutcomeDefinition:
    """A registered mapping from observed states to a binary outcome."""

    name: str
    positive_states: frozenset[str]
    label: str
    intended_question: str = ""

    def __init__(
        self,
        name: str,
        positive_states: Iterable[str],
        label: str | None = None,
        intended_question: str = "",
    ):
        clean_name = str(name).strip()
        if not clean_name:
            raise ODSAValidationError("definition name must not be empty")
        object.__setattr__(self, "name", clean_name)
        object.__setattr__(
            self,
            "positive_states",
            _normalise_names(positive_states, field=f"positive_states for {clean_name}"),
        )
        object.__setattr__(self, "label", str(label or clean_name).strip())
        object.__setattr__(self, "intended_question", str(intended_question).strip())

    def validate(self, state_space: StateSpace) -> None:
        unknown = set(self.positive_states) - set(state_space.states)
        if unknown:
            raise ODSAValidationError(
                f"definition {self.name!r} includes unknown states: {sorted(unknown)}"
            )


@dataclass(frozen=True, slots=True)
class Claim:
    """Claim boundary expressed as the states compatible with the wording.

    A definition is admissible for a claim only when every positive state in
    the definition is among the states allowed by that claim.  This is a
    conservative semantic rule: it prevents a broad positive class from being
    rhetorically narrowed into a state not met by all positive observations.
    """

    name: str
    allowed_positive_states: frozenset[str]
    wording: str

    def __init__(
        self,
        name: str,
        allowed_positive_states: Iterable[str],
        wording: str,
    ):
        clean_name = str(name).strip()
        clean_wording = str(wording).strip()
        if not clean_name:
            raise ODSAValidationError("claim name must not be empty")
        if not clean_wording:
            raise ODSAValidationError(f"claim {clean_name!r} requires wording")
        object.__setattr__(self, "name", clean_name)
        object.__setattr__(
            self,
            "allowed_positive_states",
            _normalise_names(
                allowed_positive_states,
                field=f"allowed_positive_states for {clean_name}",
            ),
        )
        object.__setattr__(self, "wording", clean_wording)

    def validate(self, state_space: StateSpace) -> None:
        unknown = set(self.allowed_positive_states) - set(state_space.states)
        if unknown:
            raise ODSAValidationError(
                f"claim {self.name!r} refers to unknown states: {sorted(unknown)}"
            )
