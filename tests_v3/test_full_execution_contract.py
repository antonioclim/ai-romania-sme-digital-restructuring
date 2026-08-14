from __future__ import annotations

import hashlib
from pathlib import Path

from simulations.full_execution import (
    EVENT_COLUMNS,
    EXPECTED_CELL_COUNT,
    EXPECTED_PROTOCOL_SHA256,
    EXPECTED_ROWS_PER_STREAM,
    PRIMARY_CONTINUOUS_METRICS,
    REPLICATIONS_PER_CELL_PER_STREAM,
    STREAM_COUNT,
    _typed_replicate_row,
    child_stream_descriptor,
    verify_frozen_protocol,
)
from simulations.run_factorial_protocol import _cell_summary


ROOT = Path(__file__).resolve().parents[1]


def test_frozen_protocol_hash_and_contract() -> None:
    actual = hashlib.sha256(
        (ROOT / "simulations" / "manuscript_protocol.yml").read_bytes()
    ).hexdigest()
    assert actual == EXPECTED_PROTOCOL_SHA256
    audit = verify_frozen_protocol()
    assert audit["status"] == "PASS"
    assert audit["expected_cell_count"] == EXPECTED_CELL_COUNT
    assert audit["frozen_replications_per_cell"] == 4000


def test_four_seedsequence_streams_are_unique_and_stable() -> None:
    descriptors = [child_stream_descriptor(index) for index in range(STREAM_COUNT)]
    assert [item["stream_index"] for item in descriptors] == [0, 1, 2, 3]
    assert len({item["child_seed_uint64"] for item in descriptors}) == STREAM_COUNT
    assert len({tuple(item["spawn_key"]) for item in descriptors}) == STREAM_COUNT
    assert all(item["stream_count"] == STREAM_COUNT for item in descriptors)


def test_frozen_execution_row_counts() -> None:
    assert REPLICATIONS_PER_CELL_PER_STREAM == 1000
    assert EXPECTED_CELL_COUNT == 432
    assert EXPECTED_ROWS_PER_STREAM == 432_000
    assert EXPECTED_ROWS_PER_STREAM * STREAM_COUNT == 1_728_000


def test_csv_rows_are_retyped_for_pooled_cell_summary() -> None:
    row = {
        "mode": "full",
        "scenario": "null_same_mixture",
        "sample_size_per_group": "50",
        "allocation_profile": "balanced",
        "misclassification_profile": "none",
        "missingness_profile": "none",
        "replication": "1",
    }
    for metric in PRIMARY_CONTINUOUS_METRICS:
        row[metric] = "0.0"
    for event in EVENT_COLUMNS:
        row[event] = "False"
    typed = _typed_replicate_row(row)
    summary = _cell_summary([typed, typed, typed])
    assert summary["replications"] == 3
    assert summary["mean_delta_level_broad_minus_active"] == 0.0
