# Branch status — `im-v3.0.0-rc1`

This branch is the active development branch for Outcome-Definition
Sensitivity Analysis version `3.0.0-rc1`.

## Current phase

IM-R7A-C1 is open. The first browser-only Study 2 outcome execution rendered
aggregate results but failed gate E4. The tool mapped the expected 20,069
complete one-hot rows and classified the remaining 986 rows incorrectly as
invalid rather than unresolved or structurally missing.

The failed report is quarantined. No result from it is admitted to the
manuscript, a release or Zenodo. A corrected browser-only rerun is required
before the IM-R7B hostile result audit.

## Failed-run and correction status

```text
failed report SHA-256:             c2331d544a131d414736aa049ba13fbce723b56c3889030ef2fb069ea9c777ae
failed overall gate:               NO-GO
failed gate:                       E4
E1–E3 and E5–E12:                 PASS
mapped common denominator:         20,069
misclassified invalid rows:           986
prior structural mapping failures:      0
prior unresolved/structural rows:      986
failed report status:              QUARANTINED
aggregate results were rendered:   yes
aggregate results admitted:        no
```

The correction changes only row-classification metadata and the E4 gate. It
does not change source fields, definitions, denominator membership, source
strata, weighting, estimands, thresholds, suppression or claim boundaries.

The corrected tool adds E13. E13 must reproduce the canonical aggregate
payload fingerprint from the failed run exactly:

```text
b18fa495616d28bcb315634c6247e2c8c94aa10724759e82cabed19a03251fe0
```

## Core package status

```text
simulation protocol SHA-256:       157bc88f41ff68261253fb19e79cc2c0aeebe63a4687d1f1073edd25ecc0b8f3
streams / cells:                   4 / 432
replications per cell:             4,000
replicate rows:                    1,728,000
maximum event-probability MCSE:    0.007905694150420948
undefined primary associations:    0
nested-level violations:           0
convergence failures:              0
independent core rerun:            byte-identical
```

## Study 2 frozen scientific status

```text
selected source:                   World Bank Technology Sophistication Across Establishments
survey reference:                  WLD_2019-2023_FAT_v01_M
dataset DOI:                       10.48529/assd-3j65
focal function:                    production-planning MOST-used method
main CSV SHA-256:                  f61a2c6e09f4763818ae1d4db8b330e97bffd8bb0824c2d833b79d728152bd17
rows / columns:                    21,055 / 723
state source:                      complete one-hot ib9b1–ib9b5 family
eligible state mappings:           20,069
unresolved or structural rows:        986
source labels / countries:         16 / 15
microdata in repository:           no
s7 primary numeric descriptor:     DISABLED
e1 size analysis:                  DISABLED
s1b candidate mapping:             REJECTED
all size-based diagnostics:        DISABLED
s1b final decision SHA-256:        b2a89a389ea24508c40a1ea4d08577c0393fce170129557c708487866ac6a09b
definitions file SHA-256:          100d7a17cf415aa5faad4a3ec55787e224d29b04fe1ba9ee357db9647ecc77fa
original outcome freeze SHA-256:   2491149bcc41596d8dbb9e509ee731447da70100de380d909daf45a4c46603be
implementation amendment SHA-256:  03244a3761052b294ab122999ff061b8f5932b4332b2ad7bd713e5f2f255e1ef
effective corrected contract:      f096825efd95c0afc699410d174517e3797ee4610b8a392c5809bdfd20789d87
corrected local rerun:              PENDING USER
result interpretation gate:        NO-GO
submission gate:                   NO-GO
```

## Locked outcome definitions

1. `integrated_planning` — ERP only;
2. `specialised_planning` — specialised software or ERP;
3. `digitally_enabled_planning` — standard software, mobile apps or digital
   platforms, specialised software or ERP.

The definitions share one denominator and are strictly nested.

## Frozen Study 2 outputs

Permitted after an E1–E13 PASS and the IM-R7B audit:

- weighted and unweighted levels within source stratum;
- disclosure-screened positive-class composition;
- exact adjacent and full definition contrasts;
- composition total-variation distance;
- pairwise source-stratum order disagreement;
- equal-stratum medians, quartiles, minima and maxima.

Prohibited:

- any size diagnostic;
- source-stratum Cramér's V;
- p-values or confidence intervals;
- global pooled prevalence;
- pooled cross-country association;
- row-level material or cells containing counts 1–4;
- interpretation of the quarantined first report.

## Open scientific gates

- corrected browser-only Study 2 rerun under E1–E13;
- IM-R7B hostile result and disclosure audit;
- secondary-use ethics and data-governance wording;
- reconstruction of the Information & Management manuscript;
- article–code–table–figure parity and final release audit;
- final Elsevier disclosure and submission preflight.

## Isolation and public-data boundary

- base lineage: published `v2.0.2`;
- default branch `main`: not modified by RC development;
- final tag `v3.0.0`: not created;
- final GitHub release and Zenodo version: not created;
- no respondent-level Study 1 data or World Bank microdata may enter the public
  workflow.
