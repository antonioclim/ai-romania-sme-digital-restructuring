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

REQUIRED = [
    'case_id','response_status','lastpage','firm_size_category','is_sme',
    'ai_familiarity_label','ai_active_use','ai_project_planning_or_deployment',
    'has_any_upskilling_measure','regulation_view_label','government_support_role_label'
]
FORBIDDEN_PATTERNS = [r'ipaddr', r'ip_address', r'\bip\b', r'email', r'phone', r'telefon', r'nume', r'company_name', r'startdate', r'datestamp', r'submitdate', r'token', r'comment', r'free_text']

def main():
    df = read_data()
    issues = []
    if len(df) != 212:
        issues.append(f'Expected 212 rows, found {len(df)}')
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        issues.append('Missing required columns: ' + ', '.join(missing))
    lower_cols = [c.lower() for c in df.columns]
    forbidden_hits = []
    for c in lower_cols:
        for pat in FORBIDDEN_PATTERNS:
            if re.search(pat, c):
                forbidden_hits.append(c)
    # Allow selection columns containing "altul" because they are binary flags, not text.
    forbidden_hits = [c for c in forbidden_hits if 'altul_va_rugam_sa_specificati' not in c]
    if forbidden_hits:
        issues.append('Potential direct/open-text identifier columns: ' + ', '.join(sorted(set(forbidden_hits))))
    full = len(df)
    sme = int((df['is_sme'] == 1).sum())
    large = int((df['firm_size_category'] == 'large_250_plus').sum())
    unknown = int(df['firm_size_category'].isna().sum())
    checks = pd.DataFrame([
        {'check':'row_count_full_completed','expected':212,'observed':full,'status':'pass' if full==212 else 'fail'},
        {'check':'sme_only_count','expected':172,'observed':sme,'status':'pass' if sme==172 else 'fail'},
        {'check':'large_comparator_count','expected':39,'observed':large,'status':'pass' if large==39 else 'fail'},
        {'check':'unknown_firm_size_count','expected':1,'observed':unknown,'status':'pass' if unknown==1 else 'fail'},
        {'check':'forbidden_identifier_columns','expected':0,'observed':len(forbidden_hits),'status':'pass' if not forbidden_hits else 'fail'},
    ])
    write_csv(checks, TABLES/'input_validation_checks.csv')
    summary = {'status':'fail' if issues else 'pass','issues':issues,'rows':full,'columns':len(df.columns),'sha256':sha256(DATA)}
    (REPORTS/'input_validation_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    log('Input validation: ' + summary['status'])
    if issues:
        raise SystemExit('Input validation failed: ' + '; '.join(issues))

if __name__ == '__main__':
    main()
