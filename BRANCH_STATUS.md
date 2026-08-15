# Branch status — `im-v3.0.0-rc1`

This branch is the active development branch for Outcome-Definition
Sensitivity Analysis version `3.0.0-rc1`.

## Current phase

IM-R6C-A is complete. The source-stratum, size-descriptor, weight and
reporting rules for Study 2 have been frozen before any technology outcome is
inspected. A browser-only local audit is now open for the non-outcome fields
`country`, `s1b`, `s7`, `e1` and `base_wt`.

The IM-R5 registry nominated `e1` as the primary size descriptor. IM-R6B showed
that `e1` is missing for 7,656 rows (36.36%). The pre-outcome amendment now
nominates `s7` as the primary numeric size candidate, retains `e1` as a
complete-case sensitivity descriptor and restricts `s1b` to sample-frame
validation. If `s7` fails the frozen quality gates, employee-size association
analysis is disabled rather than reassigned after outcomes are seen.

The branch contains:

- a literature-collision and Information & Management conversation lock;
- a SHA-256-frozen manuscript simulation protocol;
- a full four-stream simulation engine;
- 432 factorial cells and 4,000 pooled replications per cell;
- compact manuscript-facing simulation summaries;
- executable full-engine conformance tests;
- a claim–evidence ledger and hostile result audit;
- a prespecified Study 2 candidate register;
- a conditionally selected independent World Bank FAT source;
- locked Study 2 outcome states and nested definitions;
- a SHA-256 selection freeze that preceded microdata acquisition and outcome
  inspection;
- browser-only acquisition, non-redistribution and structural-gate protocols;
- verified sanitised acquisition and structural evidence;
- a frozen pre-analysis harmonisation protocol and descriptor amendment;
- executable regression tests that preserve the Study 2 outcome-analysis
  NO-GO gate.

## Full-execution status

```text
protocol SHA-256:                   157bc88f41ff68261253fb19e79cc2c0aeebe63a4687d1f1073edd25ecc0b8f3
streams:                            4
cells:                              432
replications per cell:              4,000
replicate rows:                     1,728,000
maximum event-probability MCSE:     0.007905694150420948
undefined primary associations:     0
nested-level violations:            0
convergence failures:               0
independent core rerun:             byte-identical
```

## Study 2 status

```text
selected source:          World Bank Technology Sophistication Across Establishments
survey reference:         WLD_2019-2023_FAT_v01_M
dataset DOI:              10.48529/assd-3j65
focal function:           production-planning MOST-used method
archive name:             WLD_2019-2023_FAT_v01_M_CSV.zip
archive size:             1,752,618 bytes
archive SHA-256:          6d77d3ffb9dcef2ca4534e1c438ddd2e0b357eb852e6c5b48aa5fa6c3cbe2f0e
main CSV:                 fat0_raw_data_qje.csv
main CSV size:            19,633,172 bytes
main CSV SHA-256:         f61a2c6e09f4763818ae1d4db8b330e97bffd8bb0824c2d833b79d728152bd17
rows / columns:           21,055 / 723
state source:             complete one-hot ib9b1–ib9b5 family
eligible state mappings:  20,069
mapping failures:         0
unresolved all-zero rows: 986
source labels:            16 labels representing 15 documented countries
e1 numeric / missing:     13,399 / 7,656
base_wt positive / missing: 21,054 / 1
microdata in repository:  no
outcomes inspected:       no
mechanical structural gate: PASS
semantic structural gate: PASS WITH MANDATORY CAVEATS
preanalysis freeze SHA-256: 8c8743a5c4757f6eb8f56fc3dda91fc89d82bcb506847fe35efd4e448e3ab727
primary size candidate:   s7, subject to frozen local quality gates
secondary sensitivity:   e1 complete cases
s1b role:                 sample-frame validation only
local preanalysis audit:  PENDING
analysis gate:            NO-GO
replication executed:     no
submission gate:          NO-GO
```

## Frozen preanalysis rules

1. `India` and `India_Wave2_New` remain separate analytical source strata and
   map to one reporting country, India.
2. Results are described as sixteen source strata from fifteen documented
   countries.
3. The primary numeric size candidate is `s7`; the frozen bands are 5–19,
   20–99 and 100 or more workers.
4. `s7` must pass overall, within-stratum, below-universe and integer-quality
   thresholds before size analysis is enabled.
5. `e1` is a secondary complete-case sensitivity field and `s1b` is not a
   numeric fallback.
6. Weighted levels are calculated within source stratum using positive
   `base_wt`; no pooled world estimate is permitted.
7. Weighted and unweighted association diagnostics are descriptive and receive
   no inferential p-values.
8. The 986 unresolved all-zero outcome rows remain outside the primary
   denominator and are not labelled `Other`, missing or non-users by
   assumption.

## Isolation

- base lineage: published `v2.0.2`;
- default branch `main`: not modified by RC development;
- final tag `v3.0.0`: not created;
- final GitHub release: not created;
- final Zenodo version and DOI: not created.

## Open scientific gates

- local non-outcome IM-R6C audit and external review;
- final Study 2 analysis-specification closure;
- secondary-use ethics and data-governance wording;
- locked Study 2 execution and hostile result audit;
- reconstruction of the Information & Management manuscript;
- final article–code–table–figure crosswalk;
- complete Elsevier AI disclosure and submission preflight;
- frozen `v3.0.0` asset and version-specific DOI.

The full simulation is manuscript evidence under the frozen design. Study 2 is
not yet empirical evidence. Smoke and CI outputs remain engineering evidence
only.

## Public-data boundary

No respondent-level Study 1 data, free-text responses, direct identifiers, IP
addresses, precise timestamps or paradata may be added to the version 3 public
workflow.

The selected Study 2 source microdata are governed by the World Bank Microdata
Library terms and must not be redistributed through GitHub, Zenodo, email,
cloud storage or an AI service without prior written permission.
