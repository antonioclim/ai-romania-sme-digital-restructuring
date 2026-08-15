# Study 2 — FAT production-planning replication

## Current status

The source, structural mapping, descriptor exclusions and size-free analytical
choices remain frozen. The first IM-R7A execution is quarantined because its
browser classifier reported 986 structurally unresolved one-hot rows as
invalid. The mapped denominator itself remained the expected 20,069.

A corrective browser-only rerun under implementation amendment 01 is required.
No definition, denominator membership rule, weight, estimand, threshold,
suppression rule or claim boundary has changed after aggregate outcomes were
rendered.

```text
source: World Bank Technology Sophistication Across Establishments
survey reference: WLD_2019-2023_FAT_v01_M
dataset DOI: https://doi.org/10.48529/assd-3j65
focal function: production planning — MOST-used method
mapped denominator established structurally: 20,069
unresolved or structurally missing rows: 986
analytical source strata / reporting countries: 16 / 15
size diagnostics: disabled
microdata included here: no
failed aggregate report included here: no
failed aggregate report status: quarantined
corrected local rerun: pending
result interpretation: blocked
```

## Locked definitions

1. `integrated_planning` — ERP;
2. `specialised_planning` — specialised software or ERP;
3. `digitally_enabled_planning` — standard software, mobile apps or digital
   platforms, specialised software or ERP.

The three definitions use one common mapped denominator and are strictly
nested.

## Correction and non-change safeguards

```text
original outcome-analysis freeze:
2491149bcc41596d8dbb9e509ee731447da70100de380d909daf45a4c46603be

implementation amendment 01:
03244a3761052b294ab122999ff061b8f5932b4332b2ad7bd713e5f2f255e1ef

effective corrected contract:
f096825efd95c0afc699410d174517e3797ee4610b8a392c5809bdfd20789d87

quarantined aggregate fingerprint:
b18fa495616d28bcb315634c6247e2c8c94aa10724759e82cabed19a03251fe0
```

The corrected tool adds E13 and must reproduce the quarantined aggregate
fingerprint exactly. This proves that the correction concerns classification
metadata only.

## Analysis scope

A passing corrected execution may produce only disclosure-screened aggregate
outputs:

- weighted and unweighted levels within source stratum;
- positive-class composition;
- exact definition contrasts;
- source-stratum order diagnostics;
- equal-stratum descriptive synthesis.

It may not produce size-based diagnostics, p-values, confidence intervals,
global pooled prevalence or pooled cross-country association.

## Source-data boundary

The World Bank source microdata are not redistributed and must remain local.
The repository contains only the source citation, hashes, frozen rules,
quarantine metadata, analysis contracts, tests and eventually derived
non-disclosive aggregates from a passing execution.
