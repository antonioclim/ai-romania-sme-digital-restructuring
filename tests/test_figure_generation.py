from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    'Figure_1_AI_readiness_ladder',
    'Figure_2_SME_barriers',
    'Figure_3_SME_workforce_preparation',
    'Figure_4_workforce_governance_orientation',
    'Supplementary_Figure_S1_capability_pressure',
    'Optional_Conceptual_Figure_capability_governance_model',
}

def test_figure_manifest_and_files_exist():
    manifest = ROOT / 'outputs' / 'FIGURE_MANIFEST.csv'
    assert manifest.exists()
    df = pd.read_csv(manifest)
    assert EXPECTED.issubset(set(df['figure_id']))
    for fig_id in EXPECTED:
        p = ROOT / 'outputs' / 'figures_editorial' / f'{fig_id}.png'
        assert p.exists(), f'missing figure {p}'
        assert p.stat().st_size > 20_000, f'figure looks too small: {p}'


def test_figure_source_data_exist():
    for fig_id in EXPECTED - {'Optional_Conceptual_Figure_capability_governance_model'}:
        p = ROOT / 'outputs' / 'figure_source_data' / f'{fig_id}_source.csv'
        assert p.exists(), f'missing source data {p}'
        assert p.stat().st_size > 0
    assert (ROOT / 'outputs' / 'figure_source_data' / 'Conceptual_Figure_nodes.csv').exists()
    assert (ROOT / 'outputs' / 'figure_source_data' / 'Conceptual_Figure_edges.csv').exists()
