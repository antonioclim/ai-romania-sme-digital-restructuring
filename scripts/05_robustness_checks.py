from __future__ import annotations
import json, os, sys, hashlib, platform, subprocess, re
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'processed' / 'public_quantitative_dataset_no_text_no_direct_identifiers.csv'
OUT = ROOT / 'outputs'
TABLES = OUT / 'tables'
FIGS = OUT / 'figures'
LOGS = OUT / 'logs'
REPORTS = OUT / 'reports'
for _d in [TABLES, FIGS, LOGS, REPORTS]:
    _d.mkdir(parents=True, exist_ok=True)

def log(msg: str, name: str = 'pipeline.log') -> None:
    ts = datetime.now(timezone.utc).isoformat()
    with (LOGS / name).open('a', encoding='utf-8') as f:
        f.write(f'[{ts}] {msg}\n')
    print(msg)

def read_data() -> pd.DataFrame:
    return pd.read_csv(DATA)

def pct(n, d):
    return round((100*n/d), 1) if d else np.nan

def write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding='utf-8-sig')

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    df = pd.read_csv(OUT/'analysis_dataset_constructed.csv')
    full_n=len(df); sme=df[df['is_sme']==1]; large=df[df['firm_size_category']=='large_250_plus']
    rows=[]
    for name, sub in [('full_completed', df), ('sme_only', sme), ('large_comparator', large)]:
        denom=len(sub)
        rows.append({'scope':name,'denominator':denom,'active_ai_use_n':int(sub['ai_active_use'].sum()),'active_ai_use_percent':pct(int(sub['ai_active_use'].sum()),denom),'active_or_planning_n':int(sub['adoption_binary_active_or_planning'].sum()),'active_or_planning_percent':pct(int(sub['adoption_binary_active_or_planning'].sum()),denom),'has_any_upskilling_n':int(sub['has_any_upskilling_measure'].sum()),'has_any_upskilling_percent':pct(int(sub['has_any_upskilling_measure'].sum()),denom)})
    write_csv(pd.DataFrame(rows), TABLES/'robustness_scope_comparison.csv')
    reconcile = pd.DataFrame([
        {'old_or_prior_claim':'operational deployment approximately 15-17 percent','recomputed_full_sample':'34.4 percent active AI use','recomputed_sme_only':'31.4 percent active AI use','decision':'block old claim; use G02Q04 active-use category with full and SME denominators'},
        {'old_or_prior_claim':'N=212 as SME sample','recomputed_full_sample':'212 completed responses','recomputed_sme_only':'172 SME-only responses; 39 large-firm comparators; 1 unknown firm size','decision':'use n=172 for SME-specific claims; use full sample only when labelled'},
        {'old_or_prior_claim':'one-third active use or projects','recomputed_full_sample':'64.6 percent active or planning/deployment','recomputed_sme_only':'61.0 percent active or planning/deployment','decision':'revise wording; distinguish active use from planning/deployment'},
    ])
    write_csv(reconcile, TABLES/'claim_reconciliation_blocklist.csv')
    log('Robustness checks written')

if __name__ == '__main__':
    main()
