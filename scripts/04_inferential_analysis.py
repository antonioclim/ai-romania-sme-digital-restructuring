from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import math
import numpy as np
import pandas as pd
import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
TABLES = OUT / 'tables'
LOGS = OUT / 'logs'
for _d in [TABLES, LOGS]:
    _d.mkdir(parents=True, exist_ok=True)

def log(msg: str, name: str = 'pipeline.log') -> None:
    ts = datetime.now(timezone.utc).isoformat()
    with (LOGS / name).open('a', encoding='utf-8') as f:
        f.write(f'[{ts}] {msg}\n')
    print(msg)

def write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding='utf-8-sig')

def contingency_stats(table: pd.DataFrame) -> tuple[float, int, np.ndarray, float]:
    obs = table.to_numpy(dtype=float)
    row_sums = obs.sum(axis=1, keepdims=True)
    col_sums = obs.sum(axis=0, keepdims=True)
    n = obs.sum()
    expected = row_sums @ col_sums / n if n else np.zeros_like(obs)
    with np.errstate(divide='ignore', invalid='ignore'):
        chi = np.nansum((obs - expected) ** 2 / expected)
    dof = int((obs.shape[0] - 1) * (obs.shape[1] - 1))
    p = chi2_sf(float(chi), dof) if dof > 0 else float('nan')
    return float(chi), dof, expected, float(p)

def chi2_sf(x: float, df: int) -> float:
    if df <= 0 or math.isnan(x):
        return float('nan')
    # Survival function for chi-square: Q(k/2, x/2). mpmath avoids a heavy scipy dependency in quickstart runs.
    q = mp.gammainc(df / 2.0, x / 2.0, mp.inf) / mp.gamma(df / 2.0)
    return max(0.0, min(1.0, float(q)))

def cramers_v(table: pd.DataFrame) -> float:
    chi2, _, _, _ = contingency_stats(table)
    n = table.to_numpy(dtype=float).sum()
    r, k = table.shape
    denom = n * (min(k - 1, r - 1))
    return float(np.sqrt(chi2 / denom)) if denom else np.nan

def run_chi(df: pd.DataFrame, rowvar: str, colvar: str, label: str) -> dict:
    table = pd.crosstab(df[rowvar], df[colvar])
    chi2, dof, expected, p = contingency_stats(table)
    return {
        'test_label': label,
        'row_variable': rowvar,
        'column_variable': colvar,
        'n': int(table.values.sum()),
        'rows': table.shape[0],
        'columns': table.shape[1],
        'chi_square': round(float(chi2), 4),
        'df': int(dof),
        'p_value': round(float(p), 6),
        'cramers_v': round(cramers_v(table), 4),
        'min_expected': round(float(expected.min()), 4),
        'method_note': 'chi-square; exploratory; no causal inference; p-value computed from chi-square survival function without scipy dependency'
    }

def comb(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)

def fisher_exact_2x2(table: pd.DataFrame) -> tuple[float, float]:
    arr = table.to_numpy(dtype=int)
    if arr.shape != (2, 2):
        return float('nan'), float('nan')
    a, b = arr[0]
    c, d = arr[1]
    n = int(arr.sum())
    r1 = int(a + b)
    c1 = int(a + c)
    def prob(x: int) -> float:
        return comb(c1, x) * comb(n - c1, r1 - x) / comb(n, r1)
    lo = max(0, r1 - (n - c1))
    hi = min(r1, c1)
    p_obs = prob(int(a))
    p_two = sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= p_obs + 1e-12)
    odds = (a * d / (b * c)) if b * c else (float('inf') if a * d else float('nan'))
    return float(odds), max(0.0, min(1.0, float(p_two)))

def main() -> None:
    df = pd.read_csv(OUT / 'analysis_dataset_constructed.csv')
    rows = []
    rows.append(run_chi(df[df['firm_size_category'].notna()], 'firm_size_category', 'adoption_binary_active', 'Active AI use by firm size, full sample'))
    rows.append(run_chi(df[df['firm_size_category'].notna()], 'firm_size_category', 'adoption_binary_active_or_planning', 'Active or planning AI by firm size, full sample'))
    rows.append(run_chi(df[df['is_sme'] == 1], 'firm_size_category', 'adoption_binary_active', 'Active AI use by SME size strata'))
    rows.append(run_chi(df, 'has_any_upskilling_measure', 'adoption_binary_active', 'Active AI use by any upskilling measure'))
    rows.append(run_chi(df, 'governance_support_strict_regulation', 'adoption_binary_active', 'Active AI use by stricter-regulation support'))

    sub = df[df['firm_size_category'].isin(['micro_1_9', 'small_10_49', 'medium_50_249', 'large_250_plus'])].copy()
    sub['sme_vs_large'] = np.where(sub['is_sme'] == 1, 'SME', 'large')
    table = pd.crosstab(sub['sme_vs_large'], sub['adoption_binary_active']).reindex(index=['SME','large']).fillna(0).astype(int)
    oddsratio, p = fisher_exact_2x2(table)
    rows.append({
        'test_label': 'Active AI use: SME versus large comparator',
        'row_variable': 'sme_vs_large',
        'column_variable': 'adoption_binary_active',
        'n': int(table.values.sum()),
        'rows': table.shape[0],
        'columns': table.shape[1],
        'chi_square': np.nan,
        'df': np.nan,
        'p_value': round(float(p), 6),
        'cramers_v': round(cramers_v(table), 4),
        'min_expected': np.nan,
        'method_note': f'Fisher exact odds ratio={oddsratio:.4f}; exploratory; no causal inference; exact p-value computed by hypergeometric enumeration'
    })
    write_csv(pd.DataFrame(rows), TABLES / 'exploratory_association_tests.csv')
    log('Exploratory association tests written')

if __name__ == '__main__':
    main()
