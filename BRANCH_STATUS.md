# Branch status — `im-v3.0.0-rc1`

This branch is the active development branch for Outcome-Definition
Sensitivity Analysis version `3.0.0-rc1`.

## Current phase

IM-R6B is complete. The authorised user acquired the selected World Bank pooled
CSV package, verified its archive and extracted-member identity in a local
browser and executed the sanitised structural gate. No Study 2 outcome result
has been inspected.

The next phase is IM-R6C: source-stratum harmonisation, size-descriptor
completeness audit and analysis-specification freeze.

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
- executable regression tests that preserve the Study 2 analysis NO-GO gate.

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
independent core rerun:              byte-identical
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
analysis gate:            NO-GO
replication executed:     no
submission gate:          NO-GO
```

## Mandatory preanalysis decisions

IM-R6C must be completed before any ODSA result is calculated. It must freeze:

1. the treatment of `India` and `India_Wave2_New` as source strata;
2. a non-outcome comparison of `s1b`, `s7` and `e1` for meaning,
   completeness and source-stratum coverage;
3. the primary size descriptor and source-stratum eligibility thresholds;
4. within-stratum use of `base_wt` and the across-stratum synthesis;
5. the conservative treatment of the 986 all-zero records, which cannot be
   separated into other, missing, not applicable or structurally ineligible
   states from `ib9b1`–`ib9b5` alone;
6. the public-output and disclosure boundary.

## Isolation

- base lineage: published `v2.0.2`;
- default branch `main`: not modified by RC development;
- final tag `v3.0.0`: not created;
- final GitHub release: not created;
- final Zenodo version and DOI: not created.

## Open scientific gates

- IM-R6C preanalysis harmonisation and descriptor freeze;
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
