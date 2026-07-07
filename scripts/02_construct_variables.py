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
    df = pd.read_csv(OUT/'analysis_dataset.csv')
    df['analysis_scope_full_completed'] = 1
    df['analysis_scope_sme_only'] = (df['is_sme'] == 1).astype(int)
    df['analysis_scope_large_comparator'] = (df['firm_size_category'] == 'large_250_plus').astype(int)
    df['adoption_stage'] = df['ai_familiarity_label'].map({
        'Deloc familiarizat':'unaware_or_not_familiar',
        'Puțin familiarizat':'slightly_familiar',
        'Familiarizat, dar nu folosim tehnologii AI în companie':'familiar_no_use',
        'Familiarizat, avem proiecte (în diverse faze – bugetare, testare, implementare) pentru implementări de tehnologii AI în companie':'planning_or_deployment',
        'Folosim tehnologii AI în mod activ':'active_use'
    }).fillna('unknown')
    df['adoption_binary_active'] = df['ai_active_use'].astype(int)
    df['adoption_binary_active_or_planning'] = ((df['ai_active_use']==1) | (df['ai_project_planning_or_deployment']==1)).astype(int)
    df['resource_constraint_count'] = df[[c for c in ['barrier_costuri_mari_de_implementare','barrier_lipsa_expertizei_tehnice'] if c in df.columns]].sum(axis=1)
    df['governance_support_strict_regulation'] = df['regulation_view_label'].astype(str).str.contains('reglementări mai stricte', case=False, na=False).astype(int)
    write_csv(df, OUT/'analysis_dataset_constructed.csv')
    construct_summary = pd.DataFrame([
        {'variable':'adoption_binary_active','description':'1 if respondent selected active AI use; 0 otherwise'},
        {'variable':'adoption_binary_active_or_planning','description':'1 if active AI use or projects in planning/deployment; 0 otherwise'},
        {'variable':'analysis_scope_sme_only','description':'1 if micro, small or medium; 0 otherwise'},
        {'variable':'resource_constraint_count','description':'count of cost and expertise barriers selected'},
        {'variable':'governance_support_strict_regulation','description':'1 if stricter ethical regulation selected'}
    ])
    write_csv(construct_summary, TABLES/'constructed_variable_summary.csv')
    log('Constructed variables written')

if __name__ == '__main__':
    main()
