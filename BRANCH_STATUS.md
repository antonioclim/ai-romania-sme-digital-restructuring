# Branch status — `im-v3.0.0-rc1`

This branch is the active development branch for Outcome-Definition
Sensitivity Analysis version `3.0.0-rc1`.

## Current phase

IM-R4 full-engine conformance, four-stream execution and hostile result audit
are complete.

The branch now contains:

- a literature-collision and Information & Management conversation lock;
- a SHA-256-frozen manuscript simulation protocol;
- a full four-stream simulation engine;
- 432 factorial cells and 4,000 pooled replications per cell;
- compact manuscript-facing simulation summaries;
- executable full-engine conformance tests;
- a claim–evidence ledger and hostile result audit;
- figure-ready source data for the prespecified result displays.

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

## Isolation

- base lineage: published `v2.0.2`;
- default branch `main`: not modified by RC development;
- final tag `v3.0.0`: not created;
- final GitHub release: not created;
- final Zenodo version and DOI: not created.

## Open scientific gates

- independent Study 2 selection and replication;
- reconstruction of the Information & Management manuscript;
- institutionally defensible ethics wording;
- final article–code–table–figure crosswalk;
- complete Elsevier AI disclosure and submission preflight;
- frozen `v3.0.0` asset and version-specific DOI.

The full simulation is manuscript evidence under the frozen design. Smoke and
CI outputs remain engineering evidence only.

## Public-data boundary

No respondent-level data, free-text responses, direct identifiers, IP
addresses, precise timestamps or paradata may be added to the version 3 public
workflow.
