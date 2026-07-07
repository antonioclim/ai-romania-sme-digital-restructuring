# AI-related restructuring in Romanian SMEs: reproducible analysis kit

[![Software DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21245180.svg)](https://doi.org/10.5281/zenodo.21245180)

This repository reproduces the quantitative analysis for the article **Capability pressure and AI-related restructuring in a transition EU economy: Evidence from Romanian SMEs**. It contains a cleaned, de-identified quantitative survey dataset, Python scripts, source-data CSV files, generated tables and generated figures.

## Citation and persistent identifiers

Software archive DOI: https://doi.org/10.5281/zenodo.21245180

Repository URL: https://github.com/antonioclim/ai-romania-sme-digital-restructuring

Release tag: `v1.0.0`

Associated dataset DOI: https://doi.org/10.5281/zenodo.17021824

The software DOI identifies the reproducible analysis package. The dataset DOI identifies the associated de-identified quantitative survey dataset. Please cite both when reusing the software and data.

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
python scripts/verify_sha256sums.py SHA256SUMS.txt
python scripts/run_all.py
python -m compileall scripts tests
python -m pytest -q
```

The commands regenerate `outputs/ecr/tables/`, `outputs/ecr/figures/`, `outputs/ecr/figure_source_data/` and the core analysis outputs used in the manuscript.

## GitHub Actions workflow

The repository includes `.github/workflows/reproducibility-smoke-test.yml`. It verifies the release snapshot, installs the Python dependencies, runs the analysis pipeline and executes the test suite on push or manual dispatch.

## Data

The public analysis file is `data/processed/public_quantitative_dataset_no_text_no_direct_identifiers.csv`. The associated dataset record is https://doi.org/10.5281/zenodo.17021824. Raw LimeSurvey exports, IP addresses, technical metadata, timestamps and open-text responses are excluded from this public software release.

## Double-blind review

Do not upload this unblinded release archive as the reviewer-facing archive if double-blind anonymity is required. Use the separate blinded reviewer archive provided with the submission package.

## Licence

Code is released under the MIT Licence. Dataset reuse must respect the dataset licence and the anonymisation limits documented in `docs/ethics_and_data_protection.md`.
