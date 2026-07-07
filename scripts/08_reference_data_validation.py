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
    # This script performs offline validation of metadata stored in the repository.
    expected = {
        'associated_dataset_doi':'10.5281/zenodo.17021824',
        'zenodo_record_title':'Impact of AI on Romanian Businesses (survey dataset description)',
        'zenodo_record_type':'Dataset',
        'public_dataset_policy':'no raw LimeSurvey exports, no IP addresses, no exact timestamps, no open text'
    }
    meta = json.loads((ROOT/'.zenodo.json').read_text(encoding='utf-8'))
    doi_in_meta = any(ri.get('identifier') == expected['associated_dataset_doi'] for ri in meta.get('related_identifiers', []))
    rows = pd.DataFrame([
        {'check':'associated_dataset_doi_present_in_zenodo_json','expected':expected['associated_dataset_doi'],'observed':str(doi_in_meta),'status':'pass' if doi_in_meta else 'fail'},
        {'check':'raw_data_excluded','expected':'data/raw contains README only','observed':', '.join(p.name for p in (ROOT/'data/raw').iterdir()),'status':'pass' if sorted(p.name for p in (ROOT/'data/raw').iterdir())==['README_DO_NOT_EDIT.md'] else 'fail'},
    ])
    write_csv(rows, TABLES/'reference_data_validation.csv')
    (REPORTS/'reference_data_validation_summary.json').write_text(json.dumps(expected, ensure_ascii=False, indent=2), encoding='utf-8')
    log('Reference/data metadata validation written')

if __name__ == '__main__':
    main()
