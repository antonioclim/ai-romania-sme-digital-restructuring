"""Input and output helpers for the ODSA command-line workflow."""

from __future__ import annotations

import csv
import json
from collections import OrderedDict
from pathlib import Path
from typing import Any

import yaml

from .models import Claim, ODSAValidationError, OutcomeDefinition, StateSpace


def load_yaml(path: str | Path) -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ODSAValidationError(f"{path} must contain a YAML mapping")
    return data


def load_state_counts(path: str | Path) -> OrderedDict[str, int]:
    counts: OrderedDict[str, int] = OrderedDict()
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["state", "count"]:
            raise ODSAValidationError("state-count CSV must have columns: state,count")
        for row in reader:
            state = str(row["state"]).strip()
            if state in counts:
                raise ODSAValidationError(f"duplicate state {state!r}")
            counts[state] = int(row["count"])
    if not counts:
        raise ODSAValidationError("state-count CSV is empty")
    return counts


def load_group_state_counts(path: str | Path) -> OrderedDict[str, OrderedDict[str, int]]:
    rows: OrderedDict[str, OrderedDict[str, int]] = OrderedDict()
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        expected = ["group", "state", "count"]
        if reader.fieldnames != expected:
            raise ODSAValidationError(
                "group-state CSV must have columns: group,state,count"
            )
        for row in reader:
            group = str(row["group"]).strip()
            state = str(row["state"]).strip()
            rows.setdefault(group, OrderedDict())
            if state in rows[group]:
                raise ODSAValidationError(f"duplicate group-state cell: {group!r}, {state!r}")
            rows[group][state] = int(row["count"])
    if not rows:
        raise ODSAValidationError("group-state CSV is empty")
    return rows


def load_registry(path: str | Path) -> tuple[StateSpace, list[OutcomeDefinition], list[Claim]]:
    data = load_yaml(path)
    state_space = StateSpace(data["states"], label=data.get("state_space_label", "Observed state space"))
    definitions = [
        OutcomeDefinition(
            name=item["name"],
            positive_states=item["positive_states"],
            label=item.get("label"),
            intended_question=item.get("intended_question", ""),
        )
        for item in data.get("definitions", [])
    ]
    if not definitions:
        raise ODSAValidationError("registry must contain at least one definition")
    claims = [
        Claim(
            name=item["name"],
            allowed_positive_states=item["allowed_positive_states"],
            wording=item["wording"],
        )
        for item in data.get("claims", [])
    ]
    return state_space, definitions, claims


def write_csv(path: str | Path, rows: list[dict[str, Any]]) -> None:
    path = Path(path)
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
        for row in rows:
            serialised = {
                key: json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else value
                for key, value in row.items()
            }
            writer.writerow(serialised)


def write_json(path: str | Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
