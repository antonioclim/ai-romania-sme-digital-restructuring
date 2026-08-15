# Branch status — `im-v3.0.0-rc1`

This branch is the active development branch for Outcome-Definition
Sensitivity Analysis version `3.0.0-rc1`.

## Current phase

IM-R7-A is open. The Study 2 outcome definitions and size-free analytical
contract have been frozen before the first production-planning outcome
execution.

The local browser-only tool is the only authorised execution route. Result
interpretation remains blocked until the sanitised aggregate report passes the
IM-R7-B hostile audit.

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

## Study 2 status

```text
selected source:                   World Bank Technology Sophistication Across Establishments
survey reference:                  WLD_2019-2023_FAT_v01_M
dataset DOI:                       10.48529/assd-3j65
focal function:                    production-planning MOST-used method
main CSV SHA-256:                  f61a2c6e09f4763818ae1d4db8b330e97bffd8bb0824c2d833b79d728152bd17
rows / columns:                    21,055 / 723
state source:                      complete one-hot ib9b1–ib9b5 family
eligible state mappings:           20,069
mapping failures:                  0
unresolved all-zero rows:          986
source labels / countries:         16 / 15
microdata in repository:           no
outcomes inspected:                no
s7 primary numeric descriptor:     DISABLED
e1 size analysis:                  DISABLED
s1b candidate mapping:             REJECTED
all size-based diagnostics:        DISABLED
s1b final decision SHA-256:        b2a89a389ea24508c40a1ea4d08577c0393fce170129557c708487866ac6a09b
definitions file SHA-256:          100d7a17cf415aa5faad4a3ec55787e224d29b04fe1ba9ee357db9647ecc77fa
outcome-analysis freeze SHA-256:   2491149bcc41596d8dbb9e509ee731447da70100de380d909daf45a4c46603be
local outcome execution:           PENDING USER
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

Permitted:

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
- row-level material or cells containing counts 1–4.

## Open scientific gates

- browser-only Study 2 execution;
- IM-R7-B hostile result and disclosure audit;
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
