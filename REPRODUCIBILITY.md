# Reproducibility scope

## Canonical version 3 commands

```bash
python -m pip install -e ".[test]"
python -m pytest -q tests_v3
python scripts/run_study1.py
python simulations/run_simulation.py --replications 2000 --seed 20260813
```

The equivalent build target is:

```bash
make v3-all
```

## Reproduced from public inputs

The version 3 workflow reproduces:

- registered state and outcome-definition relations;
- definition-specific levels and Wilson intervals;
- positive-state composition;
- group-specific positive rates;
- Pearson chi-square and Cramér's V diagnostics;
- group rankings and rank reversals;
- conservative definition–claim admissibility;
- deterministic simulation outputs.

Study 1 is reproduced from aggregate counts and low-dimensional group-by-state tables. The regression tests lock the published counts and effect-size values for the three current outcome definitions.

## Not reproduced publicly

The public workflow does not reproduce:

- respondent-level recoding;
- duplicate adjudication;
- free-text interpretation;
- the transformation from restricted platform exports to aggregate counts;
- linkage to verified unique organisations.

These limitations must be stated as an evidence boundary. The package provides claim-level computational verification from frozen aggregate inputs, not unrestricted end-to-end reproduction from private source records.

## Determinism

The smoke simulation uses an explicit seed and fixed replication count. Dependencies are pinned for the RC build. Generated files are excluded from Git and are reconstructed by CI. The final `v3.0.0` release will add a complete manifest, output checksums and clean-environment byte-level release verification after the manuscript-final simulation and Study 2 are frozen.
