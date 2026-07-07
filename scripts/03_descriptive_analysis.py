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

SCOPE_FILTERS = {
    'full_completed': lambda df: df,
    'sme_only': lambda df: df[df['is_sme'] == 1],
    'large_comparator': lambda df: df[df['firm_size_category'] == 'large_250_plus']
}

def freq_table(df, var, label, scope):
    denom = len(df)
    vc = df[var].value_counts(dropna=False)
    rows = []
    for cat, n in vc.items():
        rows.append({'scope':scope,'variable':var,'variable_label':label,'category':str(cat),'n':int(n),'denominator':denom,'percent':pct(int(n),denom)})
    return rows

def multi_table(df, cols, label, scope):
    denom = len(df)
    rows = []
    for c in cols:
        n = int(pd.to_numeric(df[c], errors='coerce').fillna(0).sum())
        rows.append({'scope':scope,'variable':c,'variable_label':label,'category':'selected/yes','n':n,'denominator':denom,'percent':pct(n,denom)})
    return rows

def main():
    df = pd.read_csv(OUT/'analysis_dataset_constructed.csv')
    rows=[]
    single_vars = [
        ('firm_size_category','Firm size'),
        ('ai_familiarity_label','AI familiarity/adoption'),
        ('job_impact_expectation_label','Job impact'),
        ('regulation_view_label','Regulation view'),
        ('government_support_role_label','Government support role'),
        ('romania_ai_competitiveness_label','Perceived Romanian AI competitiveness'),
    ]
    groups = [
        ([c for c in df.columns if c.startswith('motivation_')], 'Motivation'),
        ([c for c in df.columns if c.startswith('barrier_')], 'Barrier'),
        ([c for c in df.columns if c.startswith('upskilling_')], 'Upskilling'),
        ([c for c in df.columns if c.startswith('sector_') and c != 'sector_selection_count'], 'Sector'),
        ([c for c in df.columns if c.startswith('role_') and c != 'role_selection_count'], 'Role'),
        ([c for c in df.columns if c.startswith('app_potential_')], 'AI application potential'),
    ]
    for scope, fn in SCOPE_FILTERS.items():
        sub=fn(df)
        for var,label in single_vars:
            if var in sub.columns:
                rows.extend(freq_table(sub,var,label,scope))
        for cols,label in groups:
            if cols:
                rows.extend(multi_table(sub,cols,label,scope))
    out = pd.DataFrame(rows)
    write_csv(out, TABLES/'frequency_tables_by_scope.csv')
    key = pd.DataFrame([
        {'metric':'full_completed_n','value':len(df)},
        {'metric':'sme_only_n','value':int((df['is_sme']==1).sum())},
        {'metric':'large_comparator_n','value':int((df['firm_size_category']=='large_250_plus').sum())},
        {'metric':'unknown_firm_size_n','value':int(df['firm_size_category'].isna().sum())},
        {'metric':'full_active_ai_use_n','value':int(df['ai_active_use'].sum())},
        {'metric':'full_active_ai_use_percent','value':pct(int(df['ai_active_use'].sum()), len(df))},
        {'metric':'sme_active_ai_use_n','value':int(df.loc[df['is_sme']==1,'ai_active_use'].sum())},
        {'metric':'sme_active_ai_use_percent','value':pct(int(df.loc[df['is_sme']==1,'ai_active_use'].sum()), int((df['is_sme']==1).sum()))},
        {'metric':'full_active_or_planning_percent','value':pct(int(df['adoption_binary_active_or_planning'].sum()), len(df))},
        {'metric':'sme_active_or_planning_percent','value':pct(int(df.loc[df['is_sme']==1,'adoption_binary_active_or_planning'].sum()), int((df['is_sme']==1).sum()))},
    ])
    write_csv(key, TABLES/'key_recomputed_values.csv')
    # crosstabs
    ct_size = pd.crosstab(df['firm_size_category'].fillna('missing'), df['adoption_binary_active'], margins=False)
    ct_size.columns = ['not_active','active'] if len(ct_size.columns)==2 else [str(c) for c in ct_size.columns]
    ct_size = ct_size.reset_index()
    if 'active' in ct_size.columns:
        ct_size['denominator'] = ct_size[['not_active','active']].sum(axis=1)
        ct_size['active_percent'] = (ct_size['active']/ct_size['denominator']*100).round(1)
    write_csv(ct_size, TABLES/'crosstab_active_use_by_firm_size.csv')
    sector_cols=[c for c in df.columns if c.startswith('sector_') and c!='sector_selection_count']
    rows=[]
    for c in sector_cols:
        sub=df[df[c]==1]
        denom=len(sub)
        rows.append({'sector_variable':c,'denominator_selected_sector':denom,'active_n':int(sub['ai_active_use'].sum()),'active_percent':pct(int(sub['ai_active_use'].sum()),denom)})
    write_csv(pd.DataFrame(rows), TABLES/'crosstab_active_use_by_sector.csv')
    log('Descriptive tables written')

if __name__ == '__main__':
    main()
