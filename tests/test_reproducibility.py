from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]

def test_zenodo_metadata_links_dataset_doi():
    meta = json.loads((ROOT/'.zenodo.json').read_text(encoding='utf-8'))
    assert any(ri.get('identifier') == '10.5281/zenodo.17021824' for ri in meta.get('related_identifiers', []))

def test_raw_directory_has_readme_only():
    names = sorted(p.name for p in (ROOT/'data/raw').iterdir())
    assert names == ['README_DO_NOT_EDIT.md']
