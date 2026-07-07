from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]

def test_public_dataset_shape_and_core_counts():
    df = pd.read_csv(ROOT/'data/processed/public_quantitative_dataset_no_text_no_direct_identifiers.csv')
    assert len(df) == 212
    assert int((df['is_sme'] == 1).sum()) == 172
    assert int((df['firm_size_category'] == 'large_250_plus').sum()) == 39
    assert int(df['firm_size_category'].isna().sum()) == 1

def test_no_public_direct_identifier_columns():
    df = pd.read_csv(ROOT/'data/processed/public_quantitative_dataset_no_text_no_direct_identifiers.csv')
    bad_terms = ['ipaddr','ip_address','email','phone','telefon','startdate','submitdate','datestamp','token','comment','free_text']
    cols = [c.lower() for c in df.columns]
    hits = [c for c in cols if any(term in c for term in bad_terms)]
    hits = [c for c in hits if 'altul_va_rugam_sa_specificati' not in c]
    assert hits == []
