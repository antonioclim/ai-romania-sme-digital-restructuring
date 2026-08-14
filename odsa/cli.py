"""Command-line interface for the generic ODSA workflow."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analysis import (
    association_diagnostics,
    definition_composition,
    definition_level,
    definition_relation,
    group_rate_diagnostics,
    ranking_reversal,
)
from .claims import audit_claims
from .io import (
    load_group_state_counts,
    load_registry,
    load_state_counts,
    write_csv,
    write_json,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="odsa",
        description="Audit definition-sensitive categorical outcomes.",
    )
    parser.add_argument("--registry", required=True, help="YAML state, definition and claim register")
    parser.add_argument("--state-counts", required=True, help="CSV with state,count columns")
    parser.add_argument(
        "--group-state-counts",
        help="Optional CSV with group,state,count columns for association diagnostics",
    )
    parser.add_argument("--output", required=True, help="Output directory")
    return parser


def run(args: argparse.Namespace) -> dict[str, object]:
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    state_space, definitions, claims = load_registry(args.registry)
    state_counts = load_state_counts(args.state_counts)

    levels = [definition_level(state_space, state_counts, definition) for definition in definitions]
    composition = [
        row
        for definition in definitions
        for row in definition_composition(state_space, state_counts, definition)
    ]
    relations = [
        {
            "left_definition": left.name,
            "right_definition": right.name,
            "relation": definition_relation(left, right),
        }
        for left in definitions
        for right in definitions
    ]
    claim_rows = audit_claims(state_space, definitions, claims) if claims else []

    write_csv(output / "definition_levels.csv", levels)
    write_csv(output / "definition_composition.csv", composition)
    write_csv(output / "definition_relations.csv", relations)
    write_csv(output / "claim_admissibility.csv", claim_rows)

    summary: dict[str, object] = {
        "state_space": sorted(state_space.states),
        "definitions": [definition.name for definition in definitions],
        "claims": [claim.name for claim in claims],
        "group_diagnostics_included": bool(args.group_state_counts),
    }

    if args.group_state_counts:
        group_counts = load_group_state_counts(args.group_state_counts)
        rate_rows = [
            row
            for definition in definitions
            for row in group_rate_diagnostics(state_space, group_counts, definition)
        ]
        associations = [
            association_diagnostics(state_space, group_counts, definition)
            for definition in definitions
        ]
        reversals = []
        rates_by_definition = {
            definition.name: group_rate_diagnostics(state_space, group_counts, definition)
            for definition in definitions
        }
        for index, left in enumerate(definitions):
            for right in definitions[index + 1 :]:
                reversals.append(
                    {
                        "left_definition": left.name,
                        "right_definition": right.name,
                        "ranking_reversal": ranking_reversal(
                            rates_by_definition[left.name],
                            rates_by_definition[right.name],
                        ),
                    }
                )
        write_csv(output / "group_rates.csv", rate_rows)
        write_csv(output / "association_diagnostics.csv", associations)
        write_csv(output / "ranking_sensitivity.csv", reversals)
        summary["groups"] = list(group_counts)

    write_json(output / "odsa_run_summary.json", summary)
    return summary


def main() -> None:
    parser = build_parser()
    run(parser.parse_args())


if __name__ == "__main__":
    main()
