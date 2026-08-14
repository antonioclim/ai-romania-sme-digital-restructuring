from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "simulations" / "manuscript_protocol.yml"
FREEZE = ROOT / "simulations" / "manuscript_protocol.freeze.json"
EXPECTED_SHA256 = "157bc88f41ff68261253fb19e79cc2c0aeebe63a4687d1f1073edd25ecc0b8f3"


def test_frozen_protocol_sha256_matches_lock() -> None:
    calculated = hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()
    lock = json.loads(FREEZE.read_text(encoding="utf-8"))
    assert calculated == EXPECTED_SHA256
    assert lock["protocol_sha256"] == EXPECTED_SHA256
    assert lock["status"] == "FROZEN DESIGN; full execution not yet authorised"
    assert lock["full_cell_count"] == 432
    assert lock["replications_per_cell"] == 4000
    assert lock["full_replicate_row_count"] == 1_728_000
    assert lock["stream_count"] == 4
    assert lock["replications_per_stream_per_cell"] == 1000
    assert lock["ci_output_is_manuscript_evidence"] is False
