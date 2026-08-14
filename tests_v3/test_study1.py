from __future__ import annotations

from pathlib import Path

from odsa.analysis import association_diagnostics, definition_level
from odsa.io import load_group_state_counts, load_registry, load_state_counts


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "romanian_ai_engagement"


def _objects():
    state_space, definitions, _claims = load_registry(EXAMPLE / "registry.yml")
    counts = load_state_counts(EXAMPLE / "state_counts.csv")
    group_counts = load_group_state_counts(EXAMPLE / "group_state_counts.csv")
    by_name = {definition.name: definition for definition in definitions}
    return state_space, by_name, counts, group_counts


def test_study1_levels_match_locked_values() -> None:
    state_space, definitions, counts, _ = _objects()
    active = definition_level(state_space, counts, definitions["active_use"])
    project = definition_level(state_space, counts, definitions["project_stage"])
    broad = definition_level(state_space, counts, definitions["broad_engagement"])
    assert active["numerator"] == 54
    assert project["numerator"] == 51
    assert broad["numerator"] == 105
    assert round(active["level"] * 100, 1) == 31.4
    assert round(project["level"] * 100, 1) == 29.7
    assert round(broad["level"] * 100, 1) == 61.0


def test_study1_associations_match_locked_values() -> None:
    state_space, definitions, _, group_counts = _objects()
    active = association_diagnostics(state_space, group_counts, definitions["active_use"])
    project = association_diagnostics(state_space, group_counts, definitions["project_stage"])
    broad = association_diagnostics(state_space, group_counts, definitions["broad_engagement"])
    assert round(active["cramers_v"], 3) == 0.134
    assert round(project["cramers_v"], 3) == 0.350
    assert round(broad["cramers_v"], 3) == 0.428
