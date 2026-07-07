# Reproduction certificate

Software archive DOI: https://doi.org/10.5281/zenodo.21245180

Associated dataset DOI: https://doi.org/10.5281/zenodo.17021824

Repository: https://github.com/antonioclim/ai-romania-sme-digital-restructuring

Release tag: `v1.0.0`

## Environment used for package testing

- Python: 3.13.5
- Platform: Linux container

## Commands executed during package testing

```bash
python scripts/run_all.py
python -m compileall scripts tests
python -m pytest -q
python scripts/verify_sha256sums.py SHA256SUMS.txt
```

## Output scope

The default pipeline regenerates both the core cleaned-data outputs and the ECR-specific outputs in `outputs/ecr/`.

## Main analytical denominators

- Full completed sample: n = 212
- SME-only analytical sample: n = 172
- Large-firm comparator: n = 39
- Unknown firm size: n = 1

## Known limitations

- The survey is non-probability based and does not estimate national prevalence.
- Open-text responses are excluded from public release due to re-identification risk.
- The software DOI and dataset DOI identify different research objects and should both be cited when code and data are reused.
