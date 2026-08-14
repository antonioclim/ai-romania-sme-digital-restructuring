"""Full-manuscript simulation execution helpers for ODSA.

This module operationalises the frozen IM-R3 simulation contract without
modifying the frozen protocol file. Four independent NumPy SeedSequence child
streams each execute 1,000 replications per factorial cell. Pooled evidence is
created only after all stream audits pass.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
import platform
import sys
from copy import deepcopy
from datetime import datetime, timezone
from itertools import groupby
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

import numpy as np

from simulations.run_factorial_protocol import (
    _cell_summary,
    load_design,
    run_protocol,
    validate_design,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "simulations" / "manuscript_protocol.yml"
FREEZE_PATH = ROOT / "simulations" / "manuscript_protocol.freeze.json"
EXPECTED_PROTOCOL_SHA256 = "157bc88f41ff68261253fb19e79cc2c0aeebe63a4687d1f1073edd25ecc0b8f3"
ROOT_ENTROPY = 20260814
STREAM_COUNT = 4
REPLICATIONS_PER_CELL_PER_STREAM = 1000
EXPECTED_CELL_COUNT = 432
EXPECTED_ROWS_PER_STREAM = EXPECTED_CELL_COUNT * REPLICATIONS_PER_CELL_PER_STREAM

CELL_KEY_FIELDS = (
    "mode",
    "scenario",
    "sample_size_per_group",
    "allocation_profile",
    "misclassification_profile",
    "missingness_profile",
)

PRIMARY_CONTINUOUS_METRICS = (
    "delta_level_broad_minus_active",
    "delta_cramers_v_broad_minus_active",
    "cross_definition_pairwise_disagreement_share",
    "cross_definition_strict_reversal_share",
    "added_state_share_of_right_positive",
    "project_share_of_broad_positive",
    "active_level_sampling_error",
    "broad_level_sampling_error",
    "active_level_observation_error",
    "broad_level_observation_error",
    "active_level_total_error",
    "broad_level_total_error",
    "active_association_sampling_error",
    "broad_association_sampling_error",
    "active_association_observation_error",
    "broad_association_observation_error",
    "active_association_total_error",
    "broad_association_total_error",
    "active_order_error_share",
    "broad_order_error_share",
    "missing_share",
)

ERROR_METRICS = (
    "active_level_sampling_error",
    "broad_level_sampling_error",
    "active_level_observation_error",
    "broad_level_observation_error",
    "active_level_total_error",
    "broad_level_total_error",
    "active_association_sampling_error",
    "broad_association_sampling_error",
    "active_association_observation_error",
    "broad_association_observation_error",
    "active_association_total_error",
    "broad_association_total_error",
)

EVENT_COLUMNS = (
    "broad_association_stronger",
    "cross_definition_any_disagreement",
    "cross_definition_any_strict_reversal",
)


class FullExecutionError(RuntimeError):
    """Raised when the frozen full-execution contract is violated."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def protocol_sha256(path: str | Path = PROTOCOL_PATH) -> str:
    return sha256_file(path)


def verify_frozen_protocol() -> dict[str, Any]:
    actual = protocol_sha256()
    if actual != EXPECTED_PROTOCOL_SHA256:
        raise FullExecutionError(
            "Frozen protocol SHA-256 mismatch: "
            f"expected {EXPECTED_PROTOCOL_SHA256}, obtained {actual}"
        )
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    serialised = json.dumps(freeze, sort_keys=True)
    if EXPECTED_PROTOCOL_SHA256 not in serialised:
        raise FullExecutionError(
            "Freeze record does not contain the expected protocol SHA-256."
        )
    design = load_design(PROTOCOL_PATH)
    validation = validate_design(design)
    if validation.get("status") != "PASS":
        raise FullExecutionError("Frozen protocol did not pass design validation.")
    execution = design["execution"]
    if int(execution["full_replications_per_cell"]) != 4000:
        raise FullExecutionError(
            "Frozen design must specify 4,000 pooled replications per cell."
        )
    return {
        "status": "PASS",
        "protocol_sha256": actual,
        "schema_version": str(design["schema_version"]),
        "root_entropy": int(design["seed"]),
        "frozen_replications_per_cell": int(
            execution["full_replications_per_cell"]
        ),
        "expected_cell_count": EXPECTED_CELL_COUNT,
    }


def child_stream_descriptor(
    stream_index: int,
    *,
    stream_count: int = STREAM_COUNT,
    root_entropy: int = ROOT_ENTROPY,
) -> dict[str, Any]:
    if stream_count != STREAM_COUNT:
        raise FullExecutionError(
            f"The frozen contract requires exactly {STREAM_COUNT} streams."
        )
    if stream_index < 0 or stream_index >= stream_count:
        raise FullExecutionError(
            f"stream_index must be between 0 and {stream_count - 1}."
        )
    root = np.random.SeedSequence(root_entropy)
    children = root.spawn(stream_count)
    child = children[stream_index]
    state = child.generate_state(4, dtype=np.uint32)
    child_seed = int(state[0]) << 32 | int(state[1])
    return {
        "stream_index": stream_index,
        "stream_count": stream_count,
        "root_entropy": root_entropy,
        "spawn_key": list(child.spawn_key),
        "child_seed_uint64": child_seed,
        "child_state_uint32": [int(value) for value in state],
    }


def run_stream(
    *,
    stream_index: int,
    output: str | Path,
    stream_count: int = STREAM_COUNT,
    replications_per_cell: int = REPLICATIONS_PER_CELL_PER_STREAM,
) -> dict[str, Any]:
    started = utc_now()
    frozen = verify_frozen_protocol()
    if replications_per_cell != REPLICATIONS_PER_CELL_PER_STREAM:
        raise FullExecutionError(
            "Each frozen stream must execute exactly "
            f"{REPLICATIONS_PER_CELL_PER_STREAM} replications per cell."
        )
    descriptor = child_stream_descriptor(
        stream_index,
        stream_count=stream_count,
        root_entropy=int(frozen["root_entropy"]),
    )
    design = deepcopy(load_design(PROTOCOL_PATH))
    design["seed"] = int(descriptor["child_seed_uint64"])
    design["protocol_status"] = (
        "IM-R4 full manuscript execution stream; component evidence only"
    )
    design["execution"]["full_replications_per_cell"] = replications_per_cell

    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    audit = run_protocol(
        design,
        mode="full",
        output=output,
        replications_override=replications_per_cell,
    )

    replicates = output / "factorial_replicates.csv"
    summaries = output / "factorial_cell_summary.csv"
    protocol_audit = output / "protocol_run_audit.json"
    for required in (replicates, summaries, protocol_audit):
        if not required.is_file() or required.stat().st_size == 0:
            raise FullExecutionError(f"Missing or empty stream output: {required}")

    if int(audit.get("replicate_row_count", -1)) != EXPECTED_ROWS_PER_STREAM:
        raise FullExecutionError(
            "Unexpected replicate count: "
            f"{audit.get('replicate_row_count')} != {EXPECTED_ROWS_PER_STREAM}"
        )
    summary_count = int(
        audit.get(
            "cell_summary_row_count",
            audit.get("summary_row_count", EXPECTED_CELL_COUNT),
        )
    )
    if summary_count != EXPECTED_CELL_COUNT:
        raise FullExecutionError(
            f"Unexpected cell-summary count: {summary_count} != {EXPECTED_CELL_COUNT}"
        )

    stream_audit = {
        "schema_version": "1.0",
        "status": "PASS",
        "role": "one component of the frozen four-stream manuscript execution",
        "manuscript_evidence": False,
        "started_utc": started,
        "completed_utc": utc_now(),
        "protocol_sha256": frozen["protocol_sha256"],
        "protocol_schema_version": frozen["schema_version"],
        "stream": descriptor,
        "replications_per_cell": replications_per_cell,
        "expected_cell_count": EXPECTED_CELL_COUNT,
        "cell_count": summary_count,
        "expected_replicate_row_count": EXPECTED_ROWS_PER_STREAM,
        "replicate_row_count": int(audit["replicate_row_count"]),
        "files": {
            "factorial_replicates.csv": {
                "size_bytes": replicates.stat().st_size,
                "sha256": sha256_file(replicates),
            },
            "factorial_cell_summary.csv": {
                "size_bytes": summaries.stat().st_size,
                "sha256": sha256_file(summaries),
            },
            "protocol_run_audit.json": {
                "size_bytes": protocol_audit.stat().st_size,
                "sha256": sha256_file(protocol_audit),
            },
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
        },
    }
    stream_audit_path = output / "full_stream_audit.json"
    stream_audit_path.write_text(
        json.dumps(stream_audit, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return stream_audit


def _cell_key(row: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(str(row[field]) for field in CELL_KEY_FIELDS)


def iter_cell_groups(
    path: str | Path,
) -> Iterator[tuple[tuple[str, ...], list[dict[str, str]]]]:
    """Yield contiguous factorial cells from a replicate CSV."""

    seen: set[tuple[str, ...]] = set()
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = set(CELL_KEY_FIELDS) - set(reader.fieldnames or [])
        if missing:
            raise FullExecutionError(
                f"{path} omits cell-key fields: {sorted(missing)}"
            )
        for key, group in groupby(reader, key=_cell_key):
            if key in seen:
                raise FullExecutionError(
                    f"Cell {key!r} appears in non-contiguous blocks in {path}."
                )
            seen.add(key)
            yield key, list(group)


def _typed_replicate_row(row: Mapping[str, Any]) -> dict[str, Any]:
    """Convert CSV scalar strings back to the types used by the engine."""

    converted: dict[str, Any] = {}
    for key, value in row.items():
        if value is None:
            converted[key] = value
            continue
        raw = str(value).strip()
        if raw in {"True", "true"}:
            converted[key] = True
        elif raw in {"False", "false"}:
            converted[key] = False
        elif raw in {"", "nan", "NaN", "None"}:
            converted[key] = (
                float("nan") if key in PRIMARY_CONTINUOUS_METRICS else raw
            )
        elif key in {"replication", "sample_size_per_group"}:
            converted[key] = int(float(raw))
        elif key in PRIMARY_CONTINUOUS_METRICS:
            converted[key] = float(raw)
        else:
            converted[key] = value
    return converted


def _float(row: Mapping[str, Any], name: str) -> float:
    raw = row.get(name, "")
    if raw is None or str(raw).strip() in {"", "nan", "NaN", "None"}:
        return float("nan")
    return float(raw)


def _rmse(values: Sequence[float]) -> float:
    finite = np.asarray([value for value in values if math.isfinite(value)], dtype=float)
    return float(np.sqrt(np.mean(np.square(finite)))) if finite.size else float("nan")


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
        for row in rows:
            writer.writerow(row)


def discover_streams(root: str | Path) -> list[dict[str, Any]]:
    root = Path(root)
    audits = sorted(root.rglob("full_stream_audit.json"))
    if len(audits) != STREAM_COUNT:
        raise FullExecutionError(
            f"Expected {STREAM_COUNT} stream audits, found {len(audits)}."
        )
    records: list[dict[str, Any]] = []
    for audit_path in audits:
        record = json.loads(audit_path.read_text(encoding="utf-8"))
        record["_audit_path"] = str(audit_path)
        record["_directory"] = str(audit_path.parent)
        records.append(record)
    records.sort(key=lambda item: int(item["stream"]["stream_index"]))
    indices = [int(item["stream"]["stream_index"]) for item in records]
    if indices != list(range(STREAM_COUNT)):
        raise FullExecutionError(f"Unexpected stream indices: {indices}")
    seeds = [int(item["stream"]["child_seed_uint64"]) for item in records]
    if len(set(seeds)) != STREAM_COUNT:
        raise FullExecutionError("Child stream seeds are not unique.")
    spawn_keys = [tuple(item["stream"]["spawn_key"]) for item in records]
    if len(set(spawn_keys)) != STREAM_COUNT:
        raise FullExecutionError("SeedSequence spawn keys are not unique.")

    for record in records:
        if record.get("status") != "PASS":
            raise FullExecutionError("At least one stream audit did not pass.")
        if record.get("protocol_sha256") != EXPECTED_PROTOCOL_SHA256:
            raise FullExecutionError("Stream protocol hash mismatch.")
        if int(record.get("cell_count", -1)) != EXPECTED_CELL_COUNT:
            raise FullExecutionError("Stream cell count mismatch.")
        if int(record.get("replicate_row_count", -1)) != EXPECTED_ROWS_PER_STREAM:
            raise FullExecutionError("Stream replicate count mismatch.")
        directory = Path(record["_directory"])
        for filename, metadata in record["files"].items():
            path = directory / filename
            if not path.is_file():
                raise FullExecutionError(f"Missing stream file: {path}")
            if sha256_file(path) != metadata["sha256"]:
                raise FullExecutionError(f"SHA-256 mismatch for {path}")
    return records


def _stream_summary_index(path: Path) -> dict[tuple[str, ...], dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        index = {_cell_key(row): row for row in reader}
    if len(index) != EXPECTED_CELL_COUNT:
        raise FullExecutionError(
            f"{path} has {len(index)} cells; expected {EXPECTED_CELL_COUNT}."
        )
    return index


def pool_streams(
    *,
    streams_root: str | Path,
    output: str | Path,
) -> dict[str, Any]:
    started = utc_now()
    frozen = verify_frozen_protocol()
    records = discover_streams(streams_root)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)

    group_iterators = [
        iter_cell_groups(Path(record["_directory"]) / "factorial_replicates.csv")
        for record in records
    ]
    pooled_summary_rows: list[dict[str, Any]] = []
    convergence_rows: list[dict[str, Any]] = []
    undefined_rows: list[dict[str, Any]] = []
    pooled_replicates = output / "factorial_replicates_pooled.csv.gz"

    readers = [iter(iterator) for iterator in group_iterators]
    stream_summary_indices = [
        _stream_summary_index(
            Path(record["_directory"]) / "factorial_cell_summary.csv"
        )
        for record in records
    ]

    with gzip.open(pooled_replicates, "wt", newline="", encoding="utf-8") as gz:
        pooled_writer: csv.DictWriter | None = None
        processed_cells = 0
        processed_rows = 0

        while True:
            chunks: list[tuple[tuple[str, ...], list[dict[str, str]]]] = []
            ended = 0
            for iterator in readers:
                try:
                    chunks.append(next(iterator))
                except StopIteration:
                    ended += 1
            if ended:
                if ended != STREAM_COUNT:
                    raise FullExecutionError(
                        "Stream replicate files ended at different cells."
                    )
                break

            keys = [chunk[0] for chunk in chunks]
            if len(set(keys)) != 1:
                raise FullExecutionError(f"Stream cell-order mismatch: {keys}")
            key = keys[0]
            rows: list[dict[str, Any]] = []
            for stream_index, (_key, chunk_rows) in enumerate(chunks):
                if len(chunk_rows) != REPLICATIONS_PER_CELL_PER_STREAM:
                    raise FullExecutionError(
                        f"Cell {key} in stream {stream_index} has "
                        f"{len(chunk_rows)} rows."
                    )
                for row in chunk_rows:
                    enriched = dict(row)
                    enriched["stream_index"] = stream_index
                    enriched["global_replication"] = (
                        stream_index * REPLICATIONS_PER_CELL_PER_STREAM
                        + int(row["replication"])
                    )
                    rows.append(enriched)
                    if pooled_writer is None:
                        pooled_writer = csv.DictWriter(
                            gz,
                            fieldnames=list(enriched),
                        )
                        pooled_writer.writeheader()
                    pooled_writer.writerow(enriched)

            if len(rows) != 4000:
                raise FullExecutionError(
                    f"Pooled cell {key} has {len(rows)} rows instead of 4,000."
                )
            if len({int(row["global_replication"]) for row in rows}) != 4000:
                raise FullExecutionError(
                    f"Pooled cell {key} contains duplicate global replications."
                )

            typed_rows = [_typed_replicate_row(row) for row in rows]
            summary = _cell_summary(typed_rows)
            summary["stream_count"] = STREAM_COUNT
            summary["replications_per_stream"] = REPLICATIONS_PER_CELL_PER_STREAM
            summary["pooled_replications"] = len(rows)
            for metric in ERROR_METRICS:
                summary[f"rmse_{metric}"] = _rmse(
                    [_float(row, metric) for row in rows]
                )
            pooled_summary_rows.append(summary)

            for metric in PRIMARY_CONTINUOUS_METRICS:
                pooled_mean = float(summary.get(f"mean_{metric}", float("nan")))
                pooled_sd = float(summary.get(f"sd_{metric}", float("nan")))
                pooled_n = int(summary.get(f"defined_{metric}", 0))
                pooled_se = (
                    pooled_sd / math.sqrt(pooled_n)
                    if pooled_n > 0 and math.isfinite(pooled_sd)
                    else float("nan")
                )
                for stream_index, index in enumerate(stream_summary_indices):
                    stream_row = index[key]
                    stream_mean = _float(stream_row, f"mean_{metric}")
                    stream_sd = _float(stream_row, f"sd_{metric}")
                    stream_n = int(float(stream_row.get(f"defined_{metric}", 0)))
                    stream_se = (
                        stream_sd / math.sqrt(stream_n)
                        if stream_n > 0 and math.isfinite(stream_sd)
                        else float("nan")
                    )
                    denominator = math.sqrt(
                        (stream_se if math.isfinite(stream_se) else 0.0) ** 2
                        + (pooled_se if math.isfinite(pooled_se) else 0.0) ** 2
                    )
                    z = (
                        (stream_mean - pooled_mean) / denominator
                        if denominator > 0
                        and math.isfinite(stream_mean)
                        and math.isfinite(pooled_mean)
                        else float("nan")
                    )
                    convergence_rows.append(
                        {
                            **dict(zip(CELL_KEY_FIELDS, key)),
                            "metric": metric,
                            "stream_index": stream_index,
                            "stream_mean": stream_mean,
                            "pooled_mean": pooled_mean,
                            "difference": stream_mean - pooled_mean
                            if math.isfinite(stream_mean)
                            and math.isfinite(pooled_mean)
                            else float("nan"),
                            "standardised_difference": z,
                            "stream_defined": stream_n,
                            "pooled_defined": pooled_n,
                        }
                    )

                undefined = int(summary.get(f"undefined_{metric}", 0))
                share = undefined / len(rows)
                classification = (
                    "PASS"
                    if share <= 0.01
                    else "WARNING"
                    if share <= 0.05
                    else "NO_COMPARATIVE_CLAIM"
                )
                undefined_rows.append(
                    {
                        **dict(zip(CELL_KEY_FIELDS, key)),
                        "metric": metric,
                        "undefined_count": undefined,
                        "replications": len(rows),
                        "undefined_share": share,
                        "classification": classification,
                    }
                )

            processed_cells += 1
            processed_rows += len(rows)

    if processed_cells != EXPECTED_CELL_COUNT:
        raise FullExecutionError(
            f"Pooled cell count {processed_cells} != {EXPECTED_CELL_COUNT}."
        )
    expected_total = EXPECTED_CELL_COUNT * 4000
    if processed_rows != expected_total:
        raise FullExecutionError(
            f"Pooled row count {processed_rows} != {expected_total}."
        )

    pooled_summary_path = output / "factorial_cell_summary_pooled.csv"
    convergence_path = output / "stream_convergence.csv"
    undefined_path = output / "undefined_diagnostics.csv"
    _write_csv(pooled_summary_path, pooled_summary_rows)
    _write_csv(convergence_path, convergence_rows)
    _write_csv(undefined_path, undefined_rows)

    convergence_finite = [
        abs(float(row["standardised_difference"]))
        for row in convergence_rows
        if math.isfinite(float(row["standardised_difference"]))
    ]
    convergence_over_3 = (
        sum(value > 3.0 for value in convergence_finite)
        / len(convergence_finite)
        if convergence_finite
        else float("nan")
    )
    convergence_over_5 = (
        sum(value > 5.0 for value in convergence_finite)
        / len(convergence_finite)
        if convergence_finite
        else float("nan")
    )
    max_convergence = max(convergence_finite) if convergence_finite else float("nan")

    undefined_no_claim = [
        row
        for row in undefined_rows
        if row["classification"] == "NO_COMPARATIVE_CLAIM"
    ]
    undefined_warnings = [
        row for row in undefined_rows if row["classification"] == "WARNING"
    ]

    convergence_gate = (
        "PASS"
        if (
            not convergence_finite
            or (
                convergence_over_3 <= 0.01
                and convergence_over_5 <= 0.001
                and max_convergence <= 7.0
            )
        )
        else "WARNING"
        if convergence_over_3 <= 0.05 and max_convergence <= 10.0
        else "FAIL"
    )
    undefined_gate = "PASS" if not undefined_no_claim else "CONDITIONAL"

    overall_gate = (
        "PASS"
        if convergence_gate == "PASS" and undefined_gate == "PASS"
        else "CONDITIONAL"
        if convergence_gate != "FAIL"
        else "FAIL"
    )

    pooled_audit = {
        "schema_version": "1.0",
        "status": "PASS",
        "scientific_gate": overall_gate,
        "role": "pooled frozen four-stream manuscript simulation",
        "manuscript_evidence": overall_gate in {"PASS", "CONDITIONAL"},
        "started_utc": started,
        "completed_utc": utc_now(),
        "protocol_sha256": frozen["protocol_sha256"],
        "root_entropy": ROOT_ENTROPY,
        "stream_count": STREAM_COUNT,
        "replications_per_cell_per_stream": REPLICATIONS_PER_CELL_PER_STREAM,
        "pooled_replications_per_cell": 4000,
        "cell_count": processed_cells,
        "replicate_row_count": processed_rows,
        "mechanical_integrity": "PASS",
        "convergence": {
            "gate": convergence_gate,
            "finite_standardised_comparisons": len(convergence_finite),
            "share_abs_z_gt_3": convergence_over_3,
            "share_abs_z_gt_5": convergence_over_5,
            "maximum_abs_z": max_convergence,
        },
        "undefined_results": {
            "gate": undefined_gate,
            "warning_rows": len(undefined_warnings),
            "no_comparative_claim_rows": len(undefined_no_claim),
        },
        "files": {},
    }
    for path in (
        pooled_replicates,
        pooled_summary_path,
        convergence_path,
        undefined_path,
    ):
        pooled_audit["files"][path.name] = {
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }

    audit_path = output / "pooled_execution_audit.json"
    audit_path.write_text(
        json.dumps(pooled_audit, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return pooled_audit
