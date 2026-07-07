# Quickstart

From a fresh extraction:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/verify_sha256sums.py SHA256SUMS.txt
python scripts/run_all.py
python -m pytest
```

The integrity check verifies the distributed archive state. Run it before regenerating outputs. Regenerating outputs writes fresh logs and may change timestamp-bearing files, while the substantive checks are the regenerated tables, figure source data and tests.
