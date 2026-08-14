"""Reproduce the aggregate-only Romanian organisational AI example."""

from __future__ import annotations

import argparse
from pathlib import Path

from odsa.cli import run


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default=str(ROOT / "outputs_v3" / "study1"),
        help="Output directory",
    )
    parsed = parser.parse_args()
    namespace = argparse.Namespace(
        registry=str(ROOT / "examples" / "romanian_ai_engagement" / "registry.yml"),
        state_counts=str(ROOT / "examples" / "romanian_ai_engagement" / "state_counts.csv"),
        group_state_counts=str(
            ROOT / "examples" / "romanian_ai_engagement" / "group_state_counts.csv"
        ),
        output=parsed.output,
    )
    run(namespace)


if __name__ == "__main__":
    main()
