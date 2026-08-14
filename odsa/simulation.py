"""Simulation primitives for the ODSA validation programme.

The module distinguishes three sources of sensitivity:

1. the substantive outcome definition;
2. measurement error through state misclassification;
3. information loss through state coarsening.

The routines are deterministic for a fixed seed and support both lightweight
continuous-integration profiles and the pre-specified article simulation.
"""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import asdict, dataclass
from itertools import product
from math import comb
from typing import Any

import numpy as np

from .analysis import (
    association_diagnostics,
    definition_level,
    group_rate_diagnostics,
    ranking_reversal,
    ranking_signature,
)
from .coarsening import (
    coarsen_counts,
    coarsen_group_state_counts,
    coarsened_state_space,
    definition_recoverability,
    recover_coarse_definition,
)
from .models import ODSAValidationError, OutcomeDefinition, StateSpace


FINE_STATES = (
    "active_use",
    "deployment",
    "testing",
    "planning",
    "no_engagement",
)

FINE_STATE_SPACE = StateSpace(
    FINE_STATES,
    label="Fine-grained organisational technology-engagement states",
)

DEFINITIONS = OrderedDict(
    [
        (
            "active_use",
            OutcomeDefinition(
                "active_use",
                ["active_use"],
                label="Active operational use",
                intended_question="Which organisations report active use?",
            ),
        ),
        (
            "implementation",
            OutcomeDefinition(
                "implementation",
                ["active_use", "deployment", "testing"],
                label="Implementation-or-use engagement",
                intended_question=(
                    "Which organisations have reached testing, deployment or use?"
                ),
            ),
        ),
        (
            "broad_engagement",
            OutcomeDefinition(
                "broad_engagement",
                ["active_use", "deployment", "testing", "planning"],
                label="Broad organisational engagement",
                intended_question=(
                    "Which organisations report planning, testing, deployment or use?"
                ),
            ),
        ),
        (
            "strategic_or_active",
            OutcomeDefinition(
                "strategic_or_active",
                ["active_use", "planning"],
                label="Strategic planning or active use",
                intended_question=(
                    "Which organisations are either planning strategically or using?"
                ),
            ),
        ),
    ]
)

BASE_PROFILES: dict[str, np.ndarray] = {
    "balanced": np.array([0.20, 0.15, 0.15, 0.20, 0.30], dtype=float),
    "active_sparse": np.array([0.08, 0.12, 0.18, 0.27, 0.35], dtype=float),
    "project_heavy": np.array([0.10, 0.22, 0.24, 0.29, 0.15], dtype=float),
}

SIGNAL_PATTERNS: dict[str, np.ndarray] = {
    "none": np.array([0.00, 0.00, 0.00, 0.00, 0.00]),
    "active_gradient": np.array([1.10, 0.10, 0.00, 0.00, -0.30]),
    "project_gradient": np.array([0.00, 0.65, 0.80, 0.95, -0.45]),
    "reinforcing": np.array([0.90, 0.50, 0.50, 0.40, -0.60]),
    "opposing": np.array([1.00, -0.45, -0.45, -0.45, 0.20]),
    "pipeline_substitution": np.array([-0.60, 0.40, 0.60, 0.80, -0.20]),
}

COARSENING_MAPS: dict[str, OrderedDict[str, str]] = {
    "fine": OrderedDict((state, state) for state in FINE_STATES),
    "project_collapsed": OrderedDict(
        [
            ("active_use", "active_use"),
            ("deployment", "project_stage"),
            ("testing", "project_stage"),
            ("planning", "project_stage"),
            ("no_engagement", "no_engagement"),
        ]
    ),
    "binary_engaged": OrderedDict(
        [
            ("active_use", "engaged"),
            ("deployment", "engaged"),
            ("testing", "engaged"),
            ("planning", "engaged"),
            ("no_engagement", "not_engaged"),
        ]
    ),
}


@dataclass(frozen=True)
class SimulationScenario:
    """A fully specified simulation condition."""

    scenario_id: str
    base_profile: str
    signal_pattern: str
    group_count: int
    n_per_group: int
    imbalance_ratio: float
    misclassification_kind: str
    misclassification_rate: float
    coarsening: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _softmax(logits: np.ndarray) -> np.ndarray:
    centred = logits - np.max(logits)
    values = np.exp(centred)
    return values / values.sum()


def group_scores(group_count: int) -> np.ndarray:
    """Return centred group positions on the closed interval [-1, 1]."""

    if group_count < 2:
        raise ODSAValidationError("group_count must be at least two")
    return np.linspace(-1.0, 1.0, group_count)


def group_sizes(
    group_count: int,
    n_per_group: int,
    imbalance_ratio: float,
) -> list[int]:
    """Return deterministic group sizes with mean approximately n_per_group."""

    if n_per_group <= 0:
        raise ODSAValidationError("n_per_group must be positive")
    if imbalance_ratio < 1.0:
        raise ODSAValidationError("imbalance_ratio must be at least one")
    if group_count < 2:
        raise ODSAValidationError("group_count must be at least two")

    if imbalance_ratio == 1.0:
        return [int(n_per_group)] * group_count

    raw = np.geomspace(1.0 / imbalance_ratio, 1.0, group_count)
    scaled = raw / raw.mean() * n_per_group
    return [max(2, int(round(value))) for value in scaled]


def group_probabilities(
    base_profile: str,
    signal_pattern: str,
    group_count: int,
) -> list[np.ndarray]:
    """Create group-specific fine-state probabilities."""

    if base_profile not in BASE_PROFILES:
        raise ODSAValidationError(f"unknown base profile: {base_profile}")
    if signal_pattern not in SIGNAL_PATTERNS:
        raise ODSAValidationError(f"unknown signal pattern: {signal_pattern}")

    base = BASE_PROFILES[base_profile]
    shifts = SIGNAL_PATTERNS[signal_pattern]
    base_logits = np.log(base)
    return [
        _softmax(base_logits + score * shifts)
        for score in group_scores(group_count)
    ]


def misclassification_matrix(kind: str, rate: float) -> np.ndarray:
    """Return a row-stochastic true-state to recorded-state matrix."""

    if not 0.0 <= rate < 0.5:
        raise ODSAValidationError("misclassification rate must be in [0, 0.5)")
    size = len(FINE_STATES)
    matrix = np.eye(size, dtype=float)

    if kind == "none" or rate == 0.0:
        return matrix

    if kind == "adjacent_symmetric":
        matrix = np.zeros((size, size), dtype=float)
        for index in range(size):
            neighbours = [
                candidate
                for candidate in (index - 1, index + 1)
                if 0 <= candidate < size
            ]
            matrix[index, index] = 1.0 - rate
            for neighbour in neighbours:
                matrix[index, neighbour] = rate / len(neighbours)
    elif kind == "optimistic_project_to_active":
        for source in (1, 2, 3):
            matrix[source, source] = 1.0 - rate
            matrix[source, 0] = rate
    elif kind == "pessimistic_active_to_deployment":
        matrix[0, 0] = 1.0 - rate
        matrix[0, 1] = rate
    else:
        raise ODSAValidationError(f"unknown misclassification kind: {kind}")

    if not np.allclose(matrix.sum(axis=1), 1.0):
        raise ODSAValidationError("misclassification matrix rows must sum to one")
    if (matrix < 0).any():
        raise ODSAValidationError("misclassification matrix must be non-negative")
    return matrix


def apply_misclassification(
    counts: np.ndarray,
    matrix: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    """Sample recorded counts conditional on true counts and a transition matrix."""

    counts = np.asarray(counts, dtype=int)
    if counts.shape != (len(FINE_STATES),):
        raise ODSAValidationError("count vector has the wrong state dimension")
    if matrix.shape != (len(FINE_STATES), len(FINE_STATES)):
        raise ODSAValidationError("misclassification matrix has the wrong shape")

    recorded = np.zeros_like(counts)
    for source, total in enumerate(counts):
        if total:
            recorded += rng.multinomial(int(total), matrix[source])
    return recorded


def _counts_mapping(values: np.ndarray) -> OrderedDict[str, int]:
    return OrderedDict(
        (state, int(values[index]))
        for index, state in enumerate(FINE_STATES)
    )


MappingLike = dict[str, OrderedDict[str, int]]


def _aggregate_group_counts(
    group_counts: MappingLike,
) -> OrderedDict[str, int]:
    totals = OrderedDict((state, 0) for state in FINE_STATES)
    for counts in group_counts.values():
        for state in FINE_STATES:
            totals[state] += int(counts[state])
    return totals


def _safe_association(
    state_space: StateSpace,
    group_counts: MappingLike,
    definition: OutcomeDefinition,
) -> dict[str, Any] | None:
    try:
        return association_diagnostics(state_space, group_counts, definition)
    except ODSAValidationError:
        return None


def _safe_rates(
    state_space: StateSpace,
    group_counts: MappingLike,
    definition: OutcomeDefinition,
) -> list[dict[str, Any]] | None:
    try:
        return group_rate_diagnostics(state_space, group_counts, definition)
    except ODSAValidationError:
        return None


def signed_extreme_group_contrast(
    rate_rows: list[dict[str, Any]],
) -> float:
    """Return the last-group minus first-group positive-rate contrast."""

    if len(rate_rows) < 2:
        raise ODSAValidationError("at least two group-rate rows are required")
    return float(rate_rows[-1]["rate"]) - float(rate_rows[0]["rate"])


def normalised_rank_distance(
    left_rows: list[dict[str, Any]],
    right_rows: list[dict[str, Any]],
) -> float:
    """Return the normalised Kendall inversion distance between two rankings."""

    left = ranking_signature(left_rows)
    right = ranking_signature(right_rows)
    if set(left) != set(right):
        raise ODSAValidationError("rankings must refer to the same groups")
    if len(left) < 2:
        return 0.0

    left_position = {group: index for index, group in enumerate(left)}
    right_position = {group: index for index, group in enumerate(right)}
    discordant = 0
    for index, first in enumerate(left):
        for second in left[index + 1 :]:
            left_order = left_position[first] - left_position[second]
            right_order = right_position[first] - right_position[second]
            if left_order * right_order < 0:
                discordant += 1
    return discordant / comb(len(left), 2)


def _pair_metrics(
    state_space: StateSpace,
    group_counts: MappingLike,
    narrow: OutcomeDefinition,
    broad: OutcomeDefinition,
    prefix: str,
) -> dict[str, Any]:
    aggregate = OrderedDict(
        (state, sum(int(counts[state]) for counts in group_counts.values()))
        for state in state_space.states
    )
    narrow_level = definition_level(state_space, aggregate, narrow)
    broad_level = definition_level(state_space, aggregate, broad)
    narrow_assoc = _safe_association(state_space, group_counts, narrow)
    broad_assoc = _safe_association(state_space, group_counts, broad)
    narrow_rates = _safe_rates(state_space, group_counts, narrow)
    broad_rates = _safe_rates(state_space, group_counts, broad)

    result: dict[str, Any] = {
        f"{prefix}_narrow_level": narrow_level["level"],
        f"{prefix}_broad_level": broad_level["level"],
        f"{prefix}_level_inflation": (
            broad_level["level"] - narrow_level["level"]
        ),
        f"{prefix}_active_claim_contamination": (
            1.0 - narrow_level["numerator"] / broad_level["numerator"]
            if broad_level["numerator"] > 0
            else None
        ),
        f"{prefix}_narrow_cramers_v": (
            narrow_assoc["cramers_v"] if narrow_assoc else None
        ),
        f"{prefix}_broad_cramers_v": (
            broad_assoc["cramers_v"] if broad_assoc else None
        ),
        f"{prefix}_delta_v_broad_minus_narrow": (
            broad_assoc["cramers_v"] - narrow_assoc["cramers_v"]
            if narrow_assoc and broad_assoc
            else None
        ),
    }

    if narrow_rates and broad_rates:
        narrow_contrast = signed_extreme_group_contrast(narrow_rates)
        broad_contrast = signed_extreme_group_contrast(broad_rates)
        result.update(
            {
                f"{prefix}_narrow_extreme_contrast": narrow_contrast,
                f"{prefix}_broad_extreme_contrast": broad_contrast,
                f"{prefix}_contrast_direction_reversal": (
                    narrow_contrast * broad_contrast < 0
                ),
                f"{prefix}_ranking_reversal": ranking_reversal(
                    narrow_rates,
                    broad_rates,
                ),
                f"{prefix}_normalised_rank_distance": normalised_rank_distance(
                    narrow_rates,
                    broad_rates,
                ),
            }
        )
    else:
        result.update(
            {
                f"{prefix}_narrow_extreme_contrast": None,
                f"{prefix}_broad_extreme_contrast": None,
                f"{prefix}_contrast_direction_reversal": None,
                f"{prefix}_ranking_reversal": None,
                f"{prefix}_normalised_rank_distance": None,
            }
        )
    return result


def simulate_replicate(
    scenario: SimulationScenario,
    replication: int,
    master_seed: int,
) -> dict[str, Any]:
    """Simulate one pre-specified scenario replication."""

    seed_sequence = np.random.SeedSequence(
        [master_seed, int(scenario.scenario_id.split("-")[-1]), replication]
    )
    rng = np.random.default_rng(seed_sequence)

    probabilities = group_probabilities(
        scenario.base_profile,
        scenario.signal_pattern,
        scenario.group_count,
    )
    sizes = group_sizes(
        scenario.group_count,
        scenario.n_per_group,
        scenario.imbalance_ratio,
    )
    matrix = misclassification_matrix(
        scenario.misclassification_kind,
        scenario.misclassification_rate,
    )

    true_groups: MappingLike = OrderedDict()
    recorded_groups: MappingLike = OrderedDict()
    for index, (probability, sample_size) in enumerate(zip(probabilities, sizes)):
        name = f"Group {index + 1}"
        true_vector = rng.multinomial(sample_size, probability)
        recorded_vector = apply_misclassification(true_vector, matrix, rng)
        true_groups[name] = _counts_mapping(true_vector)
        recorded_groups[name] = _counts_mapping(recorded_vector)

    active = DEFINITIONS["active_use"]
    broad = DEFINITIONS["broad_engagement"]

    result: dict[str, Any] = {
        **scenario.as_dict(),
        "replication": replication,
        "master_seed": master_seed,
        "total_n": sum(sizes),
    }
    result.update(
        _pair_metrics(FINE_STATE_SPACE, true_groups, active, broad, "true")
    )
    result.update(
        _pair_metrics(
            FINE_STATE_SPACE,
            recorded_groups,
            active,
            broad,
            "recorded_fine",
        )
    )

    result["active_level_bias_from_misclassification"] = (
        result["recorded_fine_narrow_level"] - result["true_narrow_level"]
    )
    result["broad_level_bias_from_misclassification"] = (
        result["recorded_fine_broad_level"] - result["true_broad_level"]
    )
    if (
        result["recorded_fine_narrow_cramers_v"] is not None
        and result["true_narrow_cramers_v"] is not None
    ):
        result["active_v_bias_from_misclassification"] = (
            result["recorded_fine_narrow_cramers_v"]
            - result["true_narrow_cramers_v"]
        )
    else:
        result["active_v_bias_from_misclassification"] = None
    if (
        result["recorded_fine_broad_cramers_v"] is not None
        and result["true_broad_cramers_v"] is not None
    ):
        result["broad_v_bias_from_misclassification"] = (
            result["recorded_fine_broad_cramers_v"]
            - result["true_broad_cramers_v"]
        )
    else:
        result["broad_v_bias_from_misclassification"] = None

    mapping = COARSENING_MAPS[scenario.coarsening]
    reported_space = coarsened_state_space(FINE_STATE_SPACE, mapping)
    reported_groups = coarsen_group_state_counts(
        FINE_STATE_SPACE,
        recorded_groups,
        mapping,
    )
    recorded_totals = _aggregate_group_counts(recorded_groups)
    reported_totals = coarsen_counts(
        FINE_STATE_SPACE,
        recorded_totals,
        mapping,
    )

    recovered: dict[str, OutcomeDefinition] = {}
    for name, definition in DEFINITIONS.items():
        audit = definition_recoverability(
            FINE_STATE_SPACE,
            definition,
            mapping,
        )
        result[f"{name}_recoverable_after_coarsening"] = audit["recoverable"]
        result[f"{name}_ambiguous_fibres"] = len(
            audit["ambiguous_reported_states"]
        )
        if audit["recoverable"]:
            recovered[name] = recover_coarse_definition(
                FINE_STATE_SPACE,
                definition,
                mapping,
            )

    if "active_use" in recovered and "broad_engagement" in recovered:
        result.update(
            _pair_metrics(
                reported_space,
                reported_groups,
                recovered["active_use"],
                recovered["broad_engagement"],
                "reported_coarse",
            )
        )
        result["coarsening_active_level_bias"] = (
            result["reported_coarse_narrow_level"]
            - result["recorded_fine_narrow_level"]
        )
        result["coarsening_broad_level_bias"] = (
            result["reported_coarse_broad_level"]
            - result["recorded_fine_broad_level"]
        )
    else:
        for key in (
            "reported_coarse_narrow_level",
            "reported_coarse_broad_level",
            "reported_coarse_level_inflation",
            "reported_coarse_active_claim_contamination",
            "reported_coarse_narrow_cramers_v",
            "reported_coarse_broad_cramers_v",
            "reported_coarse_delta_v_broad_minus_narrow",
            "reported_coarse_narrow_extreme_contrast",
            "reported_coarse_broad_extreme_contrast",
            "reported_coarse_contrast_direction_reversal",
            "reported_coarse_ranking_reversal",
            "reported_coarse_normalised_rank_distance",
            "coarsening_active_level_bias",
            "coarsening_broad_level_bias",
        ):
            result[key] = None

    result["recorded_total_after_coarsening"] = int(sum(reported_totals.values()))
    return result


def _scenario_identifier(index: int) -> str:
    return f"scenario-{index:04d}"


def build_scenarios(profile: str) -> list[SimulationScenario]:
    """Build a deterministic scenario registry for CI or article execution."""

    if profile == "smoke":
        factor_rows = [
            ("balanced", "none", 3, 100, 1.0, "none", 0.0, "fine"),
            (
                "active_sparse",
                "active_gradient",
                3,
                100,
                4.0,
                "adjacent_symmetric",
                0.10,
                "project_collapsed",
            ),
            (
                "project_heavy",
                "opposing",
                3,
                300,
                1.0,
                "optimistic_project_to_active",
                0.10,
                "binary_engaged",
            ),
        ]
    elif profile == "ci":
        raw_rows = list(
            product(
                ("balanced", "active_sparse"),
                ("none", "active_gradient", "opposing"),
                (3,),
                (60, 200),
                (1.0, 4.0),
                (("none", 0.0), ("adjacent_symmetric", 0.10)),
                ("fine", "project_collapsed"),
            )
        )
        factor_rows = [
            (base, signal, groups, n_value, imbalance, misc[0], misc[1], coarse)
            for base, signal, groups, n_value, imbalance, misc, coarse in raw_rows
        ]
    elif profile == "article":
        raw_rows = list(
            product(
                tuple(BASE_PROFILES),
                tuple(SIGNAL_PATTERNS),
                (3,),
                (50, 150, 500),
                (1.0, 4.0),
                (
                    ("none", 0.0),
                    ("adjacent_symmetric", 0.10),
                    ("optimistic_project_to_active", 0.10),
                ),
                tuple(COARSENING_MAPS),
            )
        )
        factor_rows = [
            (base, signal, groups, n_value, imbalance, misc[0], misc[1], coarse)
            for base, signal, groups, n_value, imbalance, misc, coarse in raw_rows
        ]
    elif profile == "group_count_robustness":
        raw_rows = list(
            product(
                tuple(BASE_PROFILES),
                tuple(SIGNAL_PATTERNS),
                (2, 5),
                (100, 500),
                (1.0,),
                (("none", 0.0), ("adjacent_symmetric", 0.10)),
                ("fine",),
            )
        )
        factor_rows = [
            (base, signal, groups, n_value, imbalance, misc[0], misc[1], coarse)
            for base, signal, groups, n_value, imbalance, misc, coarse in raw_rows
        ]
    else:
        raise ODSAValidationError(f"unknown simulation profile: {profile}")

    scenarios: list[SimulationScenario] = []
    for index, row in enumerate(factor_rows, start=1):
        scenarios.append(
            SimulationScenario(
                scenario_id=_scenario_identifier(index),
                base_profile=row[0],
                signal_pattern=row[1],
                group_count=int(row[2]),
                n_per_group=int(row[3]),
                imbalance_ratio=float(row[4]),
                misclassification_kind=row[5],
                misclassification_rate=float(row[6]),
                coarsening=row[7],
            )
        )
    return scenarios
