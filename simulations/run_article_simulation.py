"""Run the pre-specified ODSA simulation profiles.

The script supports deterministic sharding so the article profile can be
executed across multiple GitHub Actions jobs without changing the scenario
registry or random-number stream.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from math import sqrt
from pathlib import Path
from typing import Any

import numpy as np

from odsa.simulation import build_scenarios, simulate_replicate


ROOT = Path(__file__).resolve().parents[1]


NUMERIC_SUMMARY_FIELDS = (
    "true_level_inflation",
    "true_active_claim_contamination",
    "true_delta_v_broad_minus_narrow",
    "true_normalised_rank_distance",
    "active_level_bias_from_misclassification",
    "broad_level_bias_from_misclassification",
    "active_v_bias_from_misclassification",
    "broad_v_bias_from_misclassification",
)

BOOLEAN_SUMMARY_FIELDS = (
    "true_contrast_direction_reversal",
    "true_ranking_reversal",
    "recorded_fine_contrast_direction_reversal",
    "recorded_fine_ranking_reversal",
    "active_use_recoverable_after_coarsening",
    "implementation_recoverable_after_coarsening",
    "broad_engagement_recoverable_after_coarsening",
    "strategic_or_active_recoverable_after_coarsening",
)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _mean(values: list[float]) -> float | None:
    return float(np.mean(values)) if values else None


def _quantile(values: list[float], q: float) -> float | None:
    return float(np.quantile(values, q)) if values else None


def _scenario_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    first = rows[0]
    summary = {
        key: first[key]
        for key in (
            "scenario_id",
            "base_profile",
            "signal_pattern",
            "group_count",
            "n_per_group",
            "imbalance_ratio",
            "misclassification_kind",
            "misclassification_rate",
            "coarsening",
        )
    }
    summary["replications_completed"] = len(rows)

    for field in NUMERIC_SUMMARY_FIELDS:
        values = [
            float(row[field])
            for row in rows
            if row.get(field) is not None
        ]
        summary[f"{field}_mean"] = _mean(values)
        summary[f"{field}_q05"] = _quantile(values, 0.05)
        summary[f"{field}_median"] = _quantile(values, 0.50)
        summary[f"{field}_q95"] = _quantile(values, 0.95)

    for field in BOOLEAN_SUMMARY_FIELDS:
        values = [
            bool(row[field])
            for row in rows
            if row.get(field) is not None
        ]
        share = sum(values) / len(values) if values else None
        summary[f"{field}_share"] = share
        summary[f"{field}_mcse"] = (
            sqrt(share * (1.0 - share) / len(values))
            if values and share is not None
            else None
        )

    delta_values = [
        float(row["true_delta_v_broad_minus_narrow"])
        for row in rows
        if row.get("true_delta_v_broad_minus_narrow") is not None
    ]
    summary["true_broad_association_stronger_share"] = (
        sum(value > 0 for value in delta_values) / len(delta_values)
        if delta_values
        else None
    )
    summary["true_broad_association_weaker_share"] = (
        sum(value < 0 for value in delta_values) / len(delta_values)
        if delta_values
        else None
    )
    summary["true_equal_association_share"] = (
        sum(value == 0 for value in delta_values) / len(delta_values)
        if delta_values
        else None
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        choices=("smoke", "ci", "article", "group_count_robustness"),
        default="ci",
    )
    parser.add_argument("--replications", type=int, default=25)
    parser.add_argument("--seed", type=int, default=20260814)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument(
        "--output",
        default=str(ROOT / "outputs_v3" / "article_simulation"),
    )
    args = parser.parse_args()

    if args.replications <= 0:
        raise SystemExit("replications must be positive")
    if args.shard_count <= 0:
        raise SystemExit("shard-count must be positive")
    if not 0 <= args.shard_index < args.shard_count:
        raise SystemExit("shard-index must be in [0, shard-count)")

    all_scenarios = build_scenarios(args.profile)
    scenarios = [
        scenario
        for index, scenario in enumerate(all_scenarios)
        if index % args.shard_count == args.shard_index
    ]

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    registry_rows = [scenario.as_dict() for scenario in scenarios]
    _write_csv(output / "scenario_registry.csv", registry_rows)

    replicate_rows: list[dict[str, Any]] = []
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for scenario in scenarios:
        for replication in range(1, args.replications + 1):
            row = simulate_replicate(
                scenario,
                replication=replication,
                master_seed=args.seed,
            )
            replicate_rows.append(row)
            grouped[scenario.scenario_id].append(row)

    _write_csv(output / "simulation_replications.csv", replicate_rows)
    summary_rows = [
        _scenario_summary(grouped[scenario.scenario_id])
        for scenario in scenarios
    ]
    _write_csv(output / "scenario_summary.csv", summary_rows)

    design = {
        "status": "PASS",
        "profile": args.profile,
        "master_seed": args.seed,
        "replications_per_scenario": args.replications,
        "total_scenarios_in_profile": len(all_scenarios),
        "scenarios_in_this_shard": len(scenarios),
        "shard_index": args.shard_index,
        "shard_count": args.shard_count,
        "total_replications_in_this_shard": len(replicate_rows),
        "scenario_ids": [scenario.scenario_id for scenario in scenarios],
        "role": (
            "continuous-integration validation"
            if args.profile in {"smoke", "ci"}
            else "pre-specified article simulation"
        ),
    }
    (output / "simulation_design.json").write_text(
        json.dumps(design, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(design, indent=2))


if __name__ == "__main__":
    main()
