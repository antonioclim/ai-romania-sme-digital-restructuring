"""Validation of the pre-specified simulation registry and outputs."""

from __future__ import annotations

from odsa.simulation import build_scenarios, simulate_replicate


def test_profile_sizes_and_identifiers_are_stable() -> None:
    smoke = build_scenarios("smoke")
    ci = build_scenarios("ci")
    article = build_scenarios("article")
    robustness = build_scenarios("group_count_robustness")

    assert len(smoke) == 3
    assert len(ci) == 96
    assert len(article) == 972
    assert len(robustness) == 144
    assert smoke[0].scenario_id == "scenario-0001"
    assert article[-1].scenario_id == "scenario-0972"


def test_replicate_is_deterministic_for_fixed_seed() -> None:
    scenario = build_scenarios("smoke")[1]
    first = simulate_replicate(scenario, replication=1, master_seed=20260814)
    second = simulate_replicate(scenario, replication=1, master_seed=20260814)
    assert first == second


def test_denominator_is_locked_through_misclassification_and_coarsening() -> None:
    for scenario in build_scenarios("smoke"):
        result = simulate_replicate(
            scenario,
            replication=1,
            master_seed=20260814,
        )
        assert result["recorded_total_after_coarsening"] == result["total_n"]


def test_expected_recoverability_boundaries_are_reported() -> None:
    scenarios = build_scenarios("smoke")

    fine = simulate_replicate(
        scenarios[0],
        replication=1,
        master_seed=20260814,
    )
    assert fine["active_use_recoverable_after_coarsening"]
    assert fine["implementation_recoverable_after_coarsening"]
    assert fine["broad_engagement_recoverable_after_coarsening"]
    assert fine["strategic_or_active_recoverable_after_coarsening"]

    project_collapsed = simulate_replicate(
        scenarios[1],
        replication=1,
        master_seed=20260814,
    )
    assert project_collapsed["active_use_recoverable_after_coarsening"]
    assert not project_collapsed[
        "implementation_recoverable_after_coarsening"
    ]
    assert project_collapsed[
        "broad_engagement_recoverable_after_coarsening"
    ]
    assert not project_collapsed[
        "strategic_or_active_recoverable_after_coarsening"
    ]

    binary = simulate_replicate(
        scenarios[2],
        replication=1,
        master_seed=20260814,
    )
    assert not binary["active_use_recoverable_after_coarsening"]
    assert not binary["implementation_recoverable_after_coarsening"]
    assert binary["broad_engagement_recoverable_after_coarsening"]
