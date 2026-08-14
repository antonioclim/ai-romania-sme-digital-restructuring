"""Create manuscript-facing summaries and a hostile audit from pooled ODSA results."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping

import matplotlib.pyplot as plt
import numpy as np


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _float(row: Mapping[str, Any], key: str) -> float:
    raw = row.get(key, "")
    if raw is None or str(raw).strip() in {"", "nan", "NaN", "None"}:
        return float("nan")
    return float(raw)


def _int(row: Mapping[str, Any], key: str) -> int:
    return int(float(row[key]))


def _select(
    rows: Iterable[dict[str, str]],
    **criteria: str | int,
) -> list[dict[str, str]]:
    selected = []
    for row in rows:
        if all(str(row.get(key)) == str(value) for key, value in criteria.items()):
            selected.append(row)
    return selected


def _single(rows: list[dict[str, str]], **criteria: str | int) -> dict[str, str]:
    selected = _select(rows, **criteria)
    if len(selected) != 1:
        raise RuntimeError(
            f"Expected one row for {criteria}, found {len(selected)}."
        )
    return selected[0]


def _strict_reversal_value(row: Mapping[str, Any]) -> float:
    for key in (
        "probability_cross_definition_any_strict_reversal",
        "event_probability_cross_definition_any_strict_reversal",
        "mean_cross_definition_strict_reversal_share",
    ):
        if key in row and str(row[key]).strip() not in {"", "nan", "NaN"}:
            return _float(row, key)
    return float("nan")


def _plot_delta_v(rows: list[dict[str, str]], output: Path) -> None:
    scenarios = [
        "null_same_mixture",
        "aligned_gradient",
        "project_only_gradient",
        "compensating_gradient",
        "rank_reversal",
        "mixed_order",
    ]
    fig, ax = plt.subplots(figsize=(10, 6))
    for scenario in scenarios:
        selected = sorted(
            _select(
                rows,
                scenario=scenario,
                allocation_profile="balanced",
                misclassification_profile="none",
                missingness_profile="none",
            ),
            key=lambda row: _int(row, "sample_size_per_group"),
        )
        x = [_int(row, "sample_size_per_group") for row in selected]
        y = [_float(row, "mean_delta_cramers_v_broad_minus_active") for row in selected]
        ax.plot(x, y, marker="o", label=scenario.replace("_", " "))
    ax.axhline(0.0, linewidth=1)
    ax.set_xlabel("Base sample size per group")
    ax.set_ylabel("Mean Δ Cramér's V (broad − active)")
    ax.set_title("Definition-sensitive association contrast under the frozen design")
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(output / "simulation_delta_v_by_scenario.png", dpi=300)
    fig.savefig(output / "simulation_delta_v_by_scenario.svg")
    plt.close(fig)


def _plot_reversal(rows: list[dict[str, str]], output: Path) -> None:
    scenarios = [
        "aligned_gradient",
        "project_only_gradient",
        "compensating_gradient",
        "rank_reversal",
        "mixed_order",
    ]
    fig, ax = plt.subplots(figsize=(10, 6))
    for scenario in scenarios:
        selected = sorted(
            _select(
                rows,
                scenario=scenario,
                allocation_profile="balanced",
                misclassification_profile="none",
                missingness_profile="none",
            ),
            key=lambda row: _int(row, "sample_size_per_group"),
        )
        x = [_int(row, "sample_size_per_group") for row in selected]
        y = [_strict_reversal_value(row) for row in selected]
        ax.plot(x, y, marker="o", label=scenario.replace("_", " "))
    ax.set_ylim(-0.02, 1.02)
    ax.set_xlabel("Base sample size per group")
    ax.set_ylabel("Strict cross-definition reversal diagnostic")
    ax.set_title("Subgroup-order sensitivity under the frozen design")
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(output / "simulation_strict_reversal_by_scenario.png", dpi=300)
    fig.savefig(output / "simulation_strict_reversal_by_scenario.svg")
    plt.close(fig)


def _plot_observation_error(rows: list[dict[str, str]], output: Path) -> None:
    selected = [
        row
        for row in rows
        if row["scenario"] == "project_only_gradient"
        and row["allocation_profile"] == "balanced"
        and _int(row, "sample_size_per_group") == 250
    ]
    labels = [
        f"{row['misclassification_profile']}\n{row['missingness_profile']}"
        for row in selected
    ]
    values = [_float(row, "mean_broad_level_observation_error") for row in selected]
    order = np.argsort(labels)
    labels = [labels[index] for index in order]
    values = [values[index] for index in order]
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(range(len(values)), values)
    ax.axhline(0.0, linewidth=1)
    ax.set_xticks(range(len(values)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Mean broad-level observation-process error")
    ax.set_title(
        "Observation-process sensitivity: project-only gradient, n=250 per group"
    )
    fig.tight_layout()
    fig.savefig(output / "simulation_observation_error.png", dpi=300)
    fig.savefig(output / "simulation_observation_error.svg")
    plt.close(fig)


def _plot_convergence(convergence: list[dict[str, str]], output: Path) -> None:
    values = [
        abs(_float(row, "standardised_difference"))
        for row in convergence
        if math.isfinite(_float(row, "standardised_difference"))
    ]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(values, bins=50)
    ax.axvline(3.0, linewidth=1)
    ax.axvline(5.0, linewidth=1)
    ax.set_xlabel("|standardised stream–pooled difference|")
    ax.set_ylabel("Frequency")
    ax.set_title("Independent-stream convergence audit")
    fig.tight_layout()
    fig.savefig(output / "simulation_stream_convergence.png", dpi=300)
    fig.savefig(output / "simulation_stream_convergence.svg")
    plt.close(fig)


def build_audit(
    pooled_rows: list[dict[str, str]],
    convergence_rows: list[dict[str, str]],
    undefined_rows: list[dict[str, str]],
    pooled_execution_audit: dict[str, Any],
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(identifier: str, passed: bool, observed: Any, requirement: str) -> None:
        checks.append(
            {
                "id": identifier,
                "status": "PASS" if passed else "FAIL",
                "observed": observed,
                "requirement": requirement,
            }
        )

    check(
        "MECH-01",
        pooled_execution_audit.get("mechanical_integrity") == "PASS",
        pooled_execution_audit.get("mechanical_integrity"),
        "All four streams, hashes, cells and replicate identifiers pass.",
    )
    check(
        "MECH-02",
        int(pooled_execution_audit.get("replicate_row_count", 0)) == 1_728_000,
        pooled_execution_audit.get("replicate_row_count"),
        "Exactly 1,728,000 pooled replicate rows.",
    )
    check(
        "MECH-03",
        int(pooled_execution_audit.get("cell_count", 0)) == 432,
        pooled_execution_audit.get("cell_count"),
        "Exactly 432 factorial cells.",
    )

    project = _single(
        pooled_rows,
        scenario="project_only_gradient",
        sample_size_per_group=500,
        allocation_profile="balanced",
        misclassification_profile="none",
        missingness_profile="none",
    )
    compensating = _single(
        pooled_rows,
        scenario="compensating_gradient",
        sample_size_per_group=500,
        allocation_profile="balanced",
        misclassification_profile="none",
        missingness_profile="none",
    )
    null = _single(
        pooled_rows,
        scenario="null_same_mixture",
        sample_size_per_group=500,
        allocation_profile="balanced",
        misclassification_profile="none",
        missingness_profile="none",
    )
    reversal = _single(
        pooled_rows,
        scenario="rank_reversal",
        sample_size_per_group=500,
        allocation_profile="balanced",
        misclassification_profile="none",
        missingness_profile="none",
    )

    project_delta = _float(project, "mean_delta_cramers_v_broad_minus_active")
    compensating_delta = _float(
        compensating, "mean_delta_cramers_v_broad_minus_active"
    )
    null_delta = _float(null, "mean_delta_cramers_v_broad_minus_active")
    check(
        "MECH-PATTERN-01",
        project_delta > 0.10,
        project_delta,
        "Project-only gradient must yield a materially positive broad-minus-active association contrast at n=500 under no observation error.",
    )
    check(
        "MECH-PATTERN-02",
        compensating_delta < -0.10,
        compensating_delta,
        "Compensating gradient must yield a materially negative broad-minus-active association contrast at n=500 under no observation error.",
    )
    check(
        "MECH-PATTERN-03",
        abs(null_delta) < 0.05,
        null_delta,
        "Null same-mixture scenario should not create a material systematic ΔV.",
    )

    reversal_value = _strict_reversal_value(reversal)
    check(
        "MECH-PATTERN-04",
        math.isfinite(reversal_value) and reversal_value >= 0.90,
        reversal_value,
        "Prespecified rank-reversal scenario should recover strict reversal with high probability at n=500.",
    )

    within_boundary = [
        row
        for row in pooled_rows
        if row["misclassification_profile"] == "active_project_swap_10"
        and row["missingness_profile"] == "none"
    ]
    max_broad_observation_error = max(
        abs(_float(row, "mean_broad_level_observation_error"))
        for row in within_boundary
    )
    check(
        "OBS-01",
        max_broad_observation_error < 1e-12,
        max_broad_observation_error,
        "Within-broad active/project swapping must preserve the broad positive count exactly when there is no missingness.",
    )

    no_claim_rows = [
        row
        for row in undefined_rows
        if row["classification"] == "NO_COMPARATIVE_CLAIM"
    ]
    check(
        "UNDEF-01",
        len(no_claim_rows) == 0,
        len(no_claim_rows),
        "No cell–metric combination should exceed the 5% undefined threshold.",
    )

    convergence_gate = pooled_execution_audit["convergence"]["gate"]
    check(
        "CONV-01",
        convergence_gate in {"PASS", "WARNING"},
        convergence_gate,
        "Independent-stream convergence must not fail.",
    )

    failed = [item for item in checks if item["status"] == "FAIL"]
    gate = "PASS" if not failed else "CONDITIONAL" if len(failed) <= 1 else "FAIL"
    return {
        "schema_version": "1.0",
        "scientific_gate": gate,
        "failed_check_count": len(failed),
        "checks": checks,
        "interpretation_contract": [
            "Simulation frequencies are conditional on the frozen design.",
            "A larger Cramér's V is not evidence of a better outcome definition.",
            "The simulation demonstrates possible mechanisms and performance, not empirical prevalence.",
            "Managerial decision quality is not tested by this simulation.",
            "Study 2 remains necessary for independent empirical replication.",
        ],
    }


def write_markdown(audit: dict[str, Any], output: Path) -> None:
    lines = [
        "# IM-R4 hostile full-simulation result audit",
        "",
        f"**Scientific gate:** `{audit['scientific_gate']}`",
        "",
        "## Checks",
        "",
        "| ID | Status | Observed | Requirement |",
        "|---|---:|---:|---|",
    ]
    for item in audit["checks"]:
        observed = str(item["observed"]).replace("|", "\\|")
        requirement = str(item["requirement"]).replace("|", "\\|")
        lines.append(
            f"| {item['id']} | {item['status']} | {observed} | {requirement} |"
        )
    lines.extend(["", "## Interpretation contract", ""])
    for statement in audit["interpretation_contract"]:
        lines.append(f"- {statement}")
    lines.extend(
        [
            "",
            "## Remaining gates",
            "",
            "- Independent Study 2 has not yet been completed.",
            "- The Information & Management manuscript has not yet been assembled.",
            "- The institutional ethics determination remains external to the simulation.",
            "- No final GitHub release or Zenodo version is authorised by this audit.",
            "",
        ]
    )
    (output / "HOSTILE_FULL_SIMULATION_AUDIT.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pooled-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.pooled_root
    pooled_rows = _read_csv(root / "factorial_cell_summary_pooled.csv")
    convergence_rows = _read_csv(root / "stream_convergence.csv")
    undefined_rows = _read_csv(root / "undefined_diagnostics.csv")
    execution_audit = json.loads(
        (root / "pooled_execution_audit.json").read_text(encoding="utf-8")
    )

    core_rows: list[dict[str, Any]] = []
    for row in pooled_rows:
        if (
            row["allocation_profile"] == "balanced"
            and row["misclassification_profile"] == "none"
            and row["missingness_profile"] == "none"
        ):
            core_rows.append(
                {
                    "scenario": row["scenario"],
                    "sample_size_per_group": row["sample_size_per_group"],
                    "mean_delta_level_broad_minus_active": row.get(
                        "mean_delta_level_broad_minus_active"
                    ),
                    "mean_delta_cramers_v_broad_minus_active": row.get(
                        "mean_delta_cramers_v_broad_minus_active"
                    ),
                    "mean_cross_definition_pairwise_disagreement_share": row.get(
                        "mean_cross_definition_pairwise_disagreement_share"
                    ),
                    "mean_cross_definition_strict_reversal_share": row.get(
                        "mean_cross_definition_strict_reversal_share"
                    ),
                    "mean_project_share_of_broad_positive": row.get(
                        "mean_project_share_of_broad_positive"
                    ),
                    "rmse_active_level_total_error": row.get(
                        "rmse_active_level_total_error"
                    ),
                    "rmse_broad_level_total_error": row.get(
                        "rmse_broad_level_total_error"
                    ),
                    "rmse_active_association_total_error": row.get(
                        "rmse_active_association_total_error"
                    ),
                    "rmse_broad_association_total_error": row.get(
                        "rmse_broad_association_total_error"
                    ),
                }
            )
    _write_csv(root / "manuscript_simulation_core_results.csv", core_rows)

    audit = build_audit(
        pooled_rows,
        convergence_rows,
        undefined_rows,
        execution_audit,
    )
    (root / "hostile_full_simulation_audit.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_markdown(audit, root)

    figure_dir = root / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    _plot_delta_v(pooled_rows, figure_dir)
    _plot_reversal(pooled_rows, figure_dir)
    _plot_observation_error(pooled_rows, figure_dir)
    _plot_convergence(convergence_rows, figure_dir)

    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
