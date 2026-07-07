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
    df = read_data().copy()
    # Deterministic typing for binary columns and counts.
    binary_prefixes = ('sector_', 'role_', 'motivation_', 'barrier_', 'upskilling_', 'app_potential_')
    binary_cols = [c for c in df.columns if c.startswith(binary_prefixes)]
    for c in binary_cols + ['ai_active_use','ai_project_planning_or_deployment','ai_familiar_no_use','ai_awareness_any','ai_at_least_familiar','has_any_upskilling_measure']:
        if c in df.columns:
            df[c] = df[c].fillna(0).astype(int)
    for c in ['firm_size_order','is_sme','ai_familiarity_order','sector_selection_count','role_selection_count','motivation_selection_count','barrier_selection_count','upskilling_positive_selection_count','app_potential_selection_count','capability_pressure_index']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    write_csv(df, OUT/'analysis_dataset.csv')
    log(f'Clean data written: {len(df)} rows, {len(df.columns)} columns')

if __name__ == '__main__':
    main()
