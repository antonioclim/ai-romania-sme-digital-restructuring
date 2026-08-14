"""Pool four frozen IM-R4 simulation streams and audit convergence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from simulations.full_execution import pool_streams


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--streams-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    audit = pool_streams(streams_root=args.streams_root, output=args.output)
    print(json.dumps(audit, indent=2, sort_keys=True))
    if audit["scientific_gate"] == "FAIL":
        raise SystemExit(
            "Mechanical execution completed, but hostile statistical audit failed."
        )


if __name__ == "__main__":
    main()
