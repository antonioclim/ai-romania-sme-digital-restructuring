# Romanian SME AI survey analysis: aggregate reproducibility package

**Version:** 2.0.2  
**DOI:** [10.5281/zenodo.21603732](https://doi.org/10.5281/zenodo.21603732)  
**Repository:** [https://github.com/antonioclim/ai-romania-sme-digital-restructuring](https://github.com/antonioclim/ai-romania-sme-digital-restructuring)

## Version lineage

Version 2.0.2 is the current aligned patch release. It preserves the aggregate-only architecture and all scientific outputs of version 2.0.1 while aligning the repository branch, Git tag, automatic source snapshot and archived asset after the final PyYAML dependency declaration. Versions 1.0.0, 2.0.0 and 2.0.1 remain available only as historical provenance for the current workflow.

## Purpose

This repository reproduces the descriptive estimates, exploratory association diagnostics, tables and figures reported for a cross-sectional survey analysis of AI engagement among Romanian SME-classified responses. The analysis is deliberately organised around outcome-definition sensitivity: reported active use, a heterogeneous project-stage category and their combined sensitivity indicator are preserved as distinct quantities.

The build operates exclusively from aggregate counts and low-dimensional contingency tables. It also documents the reconstructed Romanian questionnaire, a British-English documentary translation, response coding, case flow and the limits of the measures. The public tree contains no respondent-level records, open-text answers, direct identifiers, precise timestamps or paradata.

## Reproduce the outputs

```bash
python -m pip install --requirement requirements.lock.txt
make all
```

The complete verification sequence checks frozen inputs, metadata, the Python environment, generated outputs, the public-release boundary, automated tests and the full manifest.

## Repository map

- `data/aggregate/` — aggregate inputs and contingency tables
- `survey/` — reconstructed questionnaires, dictionaries and coding documentation
- `scripts/` — deterministic build, metadata and integrity tools
- `tests/` — analytical and release-boundary tests
- `outputs/tables/` — generated analytical tables
- `outputs/figure_source_data/` — source data for the figures
- `outputs/figures/` — generated figures
- `metadata/` — analysis contract, claim-evidence ledger and release metadata

## Evidential boundary

The source contained 212 completed responses. The principal analysis comprises 172 completed responses classified through self-reported employee bands of 1–249 employees. The empirical unit is one completed response, not a verified unique firm. The package does not estimate national prevalence and does not identify causal effects, firm-level determinants, verified deployment or organisational restructuring.

Public aggregate inputs reproduce the following central counts:

| Quantity | Count |
|---|---:|
| Reported active AI use | 54/172 |
| Project-stage category | 51/172 |
| Active use or project-stage engagement | 105/172 |
| High implementation-cost constraint | 150/172 |
| Lack of technical expertise | 137/172 |
| At least one workforce-preparation measure | 134/172 |
| Conservative workforce-preparation measure | 121/172 |

See `survey/DESCRIPTIONS.md`, `DATA_AVAILABILITY.md` and `PROVENANCE.md` before reusing the material.

## Version continuity

Version 2.0.2 supersedes versions 2.0.0 and 2.0.1 for current scholarly use. The patch changes release engineering and version metadata only. It does not change the aggregate data, analysis, outputs or evidential boundaries. The earlier tags are retained as historical provenance and must not be interpreted as restoring or endorsing the earlier respondent-level public-data architecture.

## Citation

The citation metadata are provided in `CITATION.cff`. The version-specific DOI is `10.5281/zenodo.21603732`.

## Licence

The software and associated documentation are distributed under the MIT Licence. The licence does not override ethical, legal or contractual restrictions governing respondent-level source material, which is not included in this release.
