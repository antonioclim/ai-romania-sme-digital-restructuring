# Branch status — `im-v3.0.0-rc1`

This branch is the active development branch for Outcome-Definition
Sensitivity Analysis version `3.0.0-rc1`.

## Current phase

IM-R6B local structural verification is open. The authorised user has acquired
the selected World Bank pooled CSV package, verified its archive identity in a
local browser and supplied a sanitised metadata report. No Study 2 outcome
result has been inspected.

The branch now contains:

- a literature-collision and Information & Management conversation lock;
- a SHA-256-frozen manuscript simulation protocol;
- a full four-stream simulation engine;
- 432 factorial cells and 4,000 pooled replications per cell;
- compact manuscript-facing simulation summaries;
- executable full-engine conformance tests;
- a claim–evidence ledger and hostile result audit;
- a prespecified Study 2 candidate register;
- a conditionally selected independent World Bank FAT source;
- locked Study 2 states, definitions, denominator, weighting strategy and
  structural acquisition gate;
- a SHA-256 selection freeze that precedes microdata acquisition and outcome
  inspection;
- a browser-only acquisition and non-redistribution protocol;
- verified sanitised acquisition evidence for the pooled CSV archive;
- a local structural-gate protocol that prohibits outcome calculation before
  field, denominator and state-source verification.

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

## Study 2 acquisition status

```text
selected source:        World Bank Technology Sophistication Across Establishments
survey reference:       WLD_2019-2023_FAT_v01_M
dataset DOI:            10.48529/assd-3j65
focal function:         production-planning MOST-used method
selection score:        20/21
archive acquired:       yes, by the authorised user
archive name:           WLD_2019-2023_FAT_v01_M_CSV.zip
archive size:           1,752,618 bytes
archive SHA-256:        6d77d3ffb9dcef2ca4534e1c438ddd2e0b357eb852e6c5b48aa5fa6c3cbe2f0e
container verification: PASS
main CSV:               fat0_raw_data_qje.csv
main CSV size:          19,633,172 bytes
microdata in repository:no
outcomes inspected:     no
structural gate:        PENDING_LOCAL_BROWSER_EXECUTION
replication executed:   no
acquisition gate:       CONDITIONAL_GO
submission gate:        NO-GO
```

Only sanitised reports containing file metadata and non-disclosive structural
aggregates may be shared for verification. The source microdata and extracted
files remain under the authorised user's control.

## Isolation

- base lineage: published `v2.0.2`;
- default branch `main`: not modified by RC development;
- final tag `v3.0.0`: not created;
- final GitHub release: not created;
- final Zenodo version and DOI: not created.

## Open scientific gates

- local field, denominator and state-source verification;
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

The selected Study 2 source microdata are governed by the World Bank
Microdata Library terms and must not be redistributed through GitHub, Zenodo,
email, cloud storage or an AI service without prior written permission.
