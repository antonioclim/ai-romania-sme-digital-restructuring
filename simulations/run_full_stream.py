"""Execute one of four frozen IM-R4 simulation streams."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from simulations.full_execution import run_stream


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream-index", type=int, required=True)
    parser.add_argument("--stream-count", type=int, default=4)
    parser.add_argument("--replications-per-cell", type=int, default=1000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    audit = run_stream(
        stream_index=args.stream_index,
        stream_count=args.stream_count,
        replications_per_cell=args.replications_per_cell,
        output=args.output,
    )
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
