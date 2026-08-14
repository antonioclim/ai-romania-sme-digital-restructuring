"""Deterministic simulation of association and ranking sensitivity.

This RC simulation is a methodological smoke study, not the final simulation
reported in the Information & Management manuscript.  It demonstrates that
nested outcome definitions guarantee level monotonicity but do not guarantee
association monotonicity or stable group rankings.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from odsa.analysis import association_diagnostics, group_rate_diagnostics, ranking_reversal
from odsa.models import OutcomeDefinition, StateSpace


ROOT = Path(__file__).resolve().parents[1]
STATE_SPACE = StateSpace(["active_use", "project_stage", "other"])
ACTIVE = OutcomeDefinition("active_use", ["active_use"])
BROAD = OutcomeDefinition("broad_engagement", ["active_use", "project_stage"])


def simulate(replications: int, seed: int) -> tuple[list[dict[str, object]], dict[str, object]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, object]] = []

    for replication in range(replications):
        group_counts: dict[str, dict[str, int]] = {}
        for group in ("Group A", "Group B", "Group C"):
            probabilities = rng.dirichlet(np.array([1.5, 1.5, 2.0]))
            sample_size = int(rng.integers(40, 201))
            observed = rng.multinomial(sample_size, probabilities)
            group_counts[group] = {
                "active_use": int(observed[0]),
                "project_stage": int(observed[1]),
                "other": int(observed[2]),
            }

        active_assoc = association_diagnostics(STATE_SPACE, group_counts, ACTIVE)
        broad_assoc = association_diagnostics(STATE_SPACE, group_counts, BROAD)
        active_rates = group_rate_diagnostics(STATE_SPACE, group_counts, ACTIVE)
        broad_rates = group_rate_diagnostics(STATE_SPACE, group_counts, BROAD)

        rows.append(
            {
                "replication": replication + 1,
                "active_cramers_v": active_assoc["cramers_v"],
                "broad_cramers_v": broad_assoc["cramers_v"],
                "delta_v_broad_minus_active": (
                    broad_assoc["cramers_v"] - active_assoc["cramers_v"]
                ),
                "broad_association_stronger": (
                    broad_assoc["cramers_v"] > active_assoc["cramers_v"]
                ),
                "ranking_reversal": ranking_reversal(active_rates, broad_rates),
            }
        )

    stronger = sum(bool(row["broad_association_stronger"]) for row in rows)
    reversals = sum(bool(row["ranking_reversal"]) for row in rows)
    deltas = np.array([float(row["delta_v_broad_minus_active"]) for row in rows])
    summary: dict[str, object] = {
        "status": "PASS",
        "role": "release-engineering smoke simulation",
        "replications": replications,
        "seed": seed,
        "broad_association_stronger_share": stronger / replications,
        "broad_association_weaker_or_equal_share": 1.0 - stronger / replications,
        "ranking_reversal_share": reversals / replications,
        "mean_delta_v_broad_minus_active": float(deltas.mean()),
        "median_delta_v_broad_minus_active": float(np.median(deltas)),
        "minimum_delta_v": float(deltas.min()),
        "maximum_delta_v": float(deltas.max()),
    }
    return rows, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replications", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260813)
    parser.add_argument(
        "--output",
        default=str(ROOT / "outputs_v3" / "simulation"),
    )
    args = parser.parse_args()
    if args.replications <= 0:
        raise SystemExit("replications must be positive")

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    rows, summary = simulate(args.replications, args.seed)

    with (output / "simulation_replications.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    (output / "simulation_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
