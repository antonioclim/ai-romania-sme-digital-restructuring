# AI-related restructuring in Romanian SMEs: reproducible analysis kit

This repository reproduces the quantitative analysis for the article **Capability pressure and AI-related restructuring in a transition EU economy: Evidence from Romanian SMEs**. It contains a cleaned, de-identified quantitative survey dataset, Python scripts, source-data CSV files, generated tables and generated figures.

## What the kit reproduces

Running the kit regenerates validation logs, constructed analysis datasets, descriptive tables, exploratory association screens, robustness tables and ECR-oriented manuscript figures. The main analytical scopes are:

- full completed sample: n = 212;
- SME-only analytical sample: n = 172;
- large-firm comparator: n = 39;
- unknown firm size: n = 1, excluded from size-specific estimates.

The survey is an engaged non-probability sample. It is not a national prevalence estimate.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/run_all.py
python -m pytest
python scripts/verify_sha256sums.py SHA256SUMS.txt
```

The command regenerates `outputs/ecr/tables/`, `outputs/ecr/figures/`, `outputs/ecr/figure_source_data/` and the core analysis outputs used in the manuscript.

## Data

The public analysis file is `data/processed/public_quantitative_dataset_no_text_no_direct_identifiers.csv`. The associated dataset record is https://doi.org/10.5281/zenodo.17021824. This is the dataset DOI, not the software DOI for this repository. A software DOI should be minted only after the public GitHub release and Zenodo software deposit are created.

## Double-blind review

Do not upload this unblinded release archive as the reviewer-facing archive if double-blind anonymity is required. Use the separate blinded reviewer archive provided with the submission package.

## Licence

Code is released under the MIT Licence. Dataset reuse must respect the dataset licence and the anonymisation limits documented in `docs/ethics_and_data_protection.md`.
