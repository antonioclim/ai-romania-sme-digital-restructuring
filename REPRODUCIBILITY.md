# Reproducibility notes

The analysis uses relative paths and a cleaned quantitative dataset. No internet access is required for core reproduction.

Recommended verification sequence:

```bash
python scripts/verify_sha256sums.py SHA256SUMS.txt
python scripts/run_all.py
python -m compileall scripts tests
python -m pytest
```

The table values are deterministic given identical inputs and package versions. Figure rendering may vary slightly across Matplotlib versions, but all figures are generated from source-data CSV files and the generation manifest reports the exported files and SHA-256 hashes.

## Figure reproduction

`scripts/06_generate_figures.py` is the canonical figure generator. It reads the cleaned dataset and generated tables, then writes:

- `outputs/figures_editorial/*.png` for manuscript embedding;
- `outputs/figures/*.png` as compatibility copies;
- `outputs/figure_source_data/*.csv` for per-figure source data;
- `outputs/FIGURE_MANIFEST.csv`;
- `outputs/FIGURE_VISUAL_QA.csv`.

The optional conceptual figure is generated from explicit node and edge tables. It is not required for the manuscript unless the authors decide to use a conceptual visual.
