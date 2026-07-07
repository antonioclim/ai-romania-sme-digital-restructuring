# Reproducibility notes

Software archive DOI: https://doi.org/10.5281/zenodo.21245180

Associated dataset DOI: https://doi.org/10.5281/zenodo.17021824

The analysis uses relative paths and a cleaned quantitative dataset. No internet access is required for core reproduction.

Recommended verification sequence:

```bash
python scripts/verify_sha256sums.py SHA256SUMS.txt
python scripts/run_all.py
python -m compileall scripts tests
python -m pytest -q
```

`SHA256SUMS.txt` verifies the packaged repository snapshot before regeneration. The analysis pipeline then rebuilds tables, figures and logs from the cleaned quantitative dataset.

## Figure reproduction

`scripts/06_generate_figures.py` is the canonical figure generator. It reads the cleaned dataset and generated tables, then writes:

- `outputs/figures_editorial/*.png` for manuscript embedding;
- `outputs/figures/*.png` as compatibility copies;
- `outputs/figure_source_data/*.csv` for per-figure source data;
- `outputs/FIGURE_MANIFEST.csv`;
- `outputs/FIGURE_VISUAL_QA.csv`.

The optional conceptual figure is generated from explicit node and edge tables. It is not required for the manuscript unless the author decides to use a conceptual visual.
