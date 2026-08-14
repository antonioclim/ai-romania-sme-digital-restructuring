"""Generate constructive counterexamples used by the formal specification."""

from __future__ import annotations

import json
from pathlib import Path

from odsa.analysis import association_diagnostics, group_rate_diagnostics, ranking_reversal
from odsa.models import OutcomeDefinition, StateSpace
from odsa.properties import definition_identifiability


ROOT = Path(__file__).resolve().parents[1]
STATE_SPACE = StateSpace(["active", "project", "other"])
ACTIVE = OutcomeDefinition("active", ["active"])
BROAD = OutcomeDefinition("broad", ["active", "project"])


def _evaluate(group_counts: dict[str, dict[str, int]]) -> dict[str, object]:
    active_association = association_diagnostics(STATE_SPACE, group_counts, ACTIVE)
    broad_association = association_diagnostics(STATE_SPACE, group_counts, BROAD)
    active_rates = group_rate_diagnostics(STATE_SPACE, group_counts, ACTIVE)
    broad_rates = group_rate_diagnostics(STATE_SPACE, group_counts, BROAD)
    return {
        "group_counts": group_counts,
        "active_cramers_v": active_association["cramers_v"],
        "broad_cramers_v": broad_association["cramers_v"],
        "active_group_rates": active_rates,
        "broad_group_rates": broad_rates,
        "ranking_reversal": ranking_reversal(active_rates, broad_rates),
    }


def build_counterexamples() -> dict[str, object]:
    broad_stronger = _evaluate(
        {
            "Group A": {"active": 10, "project": 0, "other": 90},
            "Group B": {"active": 10, "project": 40, "other": 50},
        }
    )
    broad_weaker = _evaluate(
        {
            "Group A": {"active": 50, "project": 0, "other": 50},
            "Group B": {"active": 10, "project": 40, "other": 50},
        }
    )
    rank_reversal_case = _evaluate(
        {
            "Group A": {"active": 30, "project": 0, "other": 70},
            "Group B": {"active": 10, "project": 40, "other": 50},
        }
    )

    mapping = {
        "active_use": "active_use",
        "deployed": "project_stage",
        "testing": "project_stage",
        "planning": "project_stage",
        "no_engagement": "no_engagement",
    }
    identifiability = {
        name: definition_identifiability(OutcomeDefinition(name, states), mapping)
        for name, states in {
            "active_use": ["active_use"],
            "implemented": ["active_use", "deployed"],
            "tested_or_beyond": ["active_use", "deployed", "testing"],
            "broad_engagement": [
                "active_use",
                "deployed",
                "testing",
                "planning",
            ],
            "experimental_activity": ["active_use", "testing"],
        }.items()
    }

    return {
        "association_strengthening": broad_stronger,
        "association_weakening": broad_weaker,
        "rank_reversal": rank_reversal_case,
        "coarsening_identifiability": identifiability,
        "denominator_drift": {
            "narrow": {"numerator": 9, "denominator": 10, "level": 0.9},
            "broad": {"numerator": 50, "denominator": 100, "level": 0.5},
            "interpretation": (
                "The apparent reversal is possible only because the analysis sets and "
                "denominators differ; it is not a violation of common-denominator nesting."
            ),
        },
    }


def main() -> None:
    output = ROOT / "outputs_v3" / "formal" / "constructive_counterexamples.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    data = build_counterexamples()
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "output": str(output)}, indent=2))


if __name__ == "__main__":
    main()
