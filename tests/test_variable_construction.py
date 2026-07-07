from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_pipeline_outputs_are_available_after_run_all():
    """Fast reviewer smoke test: the quickstart pipeline should have generated the core tables."""
    path = ROOT / 'outputs' / 'tables' / 'key_recomputed_values.csv'
    assert path.exists(), 'Run python scripts/run_all.py before pytest if outputs are absent.'
    key = pd.read_csv(path)
    lookup = dict(zip(key['metric'], key['value']))
    assert float(lookup['full_active_ai_use_percent']) == 34.4
    assert float(lookup['sme_active_ai_use_percent']) == 31.4
    assert float(lookup['sme_active_or_planning_percent']) == 61.0


def test_reconciliation_blocks_old_operational_deployment_claim():
    path = ROOT / 'outputs' / 'tables' / 'claim_reconciliation_blocklist.csv'
    assert path.exists()
    text = path.read_text(encoding='utf-8-sig')
    assert '15-17' in text
    assert '34.4' in text
    assert 'revise wording' in text.lower() or 'blocked' in text.lower() or 'reject' in text.lower()
