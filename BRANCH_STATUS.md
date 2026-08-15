# Branch status — `im-v3.0.0-rc1`

This branch is the active development branch for Outcome-Definition
Sensitivity Analysis version `3.0.0-rc1`.

## Current phase

IM-R6C is complete. The authorised user executed the frozen browser-only
pre-analysis audit on the non-outcome fields `country`, `s1b`, `s7`, `e1` and
`base_wt`. The tool read no production-planning technology field and no Study 2
outcome result has been inspected.

The audit returned `NO-GO` because 1,538 of 21,055 valid `s7` values (7.305%)
are below the prespecified five-worker universe threshold, exceeding the frozen
1% maximum. In accordance with the preanalysis freeze, `s7` is disabled as the
primary numeric size descriptor. The threshold will not be relaxed, the
below-five cases will not be repaired by assumption and `e1` will not be
promoted to the primary descriptor after the failure.

The next phase is IM-R6D: official code-label verification and cross-source-
stratum invariance audit for `s1b`. `s1b` may be considered only as a
categorical sampling-frame size stratum, never as a numeric worker count. If
its official mapping cannot be verified and frozen before outcome inspection,
all size-based Study 2 diagnostics remain disabled.

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
- a frozen pre-analysis harmonisation protocol;
- the sanitised IM-R6C audit and hostile external review;
- executable regression tests preserving the Study 2 outcome-analysis NO-GO
  gate.

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
IM-R6C report SHA-256:     f1a2197a8a60e37ffa6664f3e512beea448c875ddc9c86d60cadda1fa5250e8f
s7 valid / below five:    21,055 / 1,538
s7 below-five share:      7.305%
IM-R6C frozen gate:       NO-GO
primary numeric descriptor: DISABLED
s7 threshold relaxation:  PROHIBITED
e1 promotion to primary:  PROHIBITED
s1b observed codes:       1, 2, 3; official categorical mapping audit pending
analysis gate:            NO-GO
replication executed:     no
submission gate:          NO-GO
```

## Frozen consequences of IM-R6C

1. `s7` is not used as a cross-source-stratum primary numeric descriptor.
2. The 1% below-universe threshold is not relaxed after audit inspection.
3. The 1,538 below-five `s7` values are not dropped, repaired or relabelled by
   assumption.
4. `e1` is not promoted to the primary descriptor; any complete-case role
   remains secondary and requires a final scope decision.
5. `s1b` is never interpreted as a numeric worker count.
6. `s1b` may be considered only as a categorical sampling-frame size stratum
   after official code-label and cross-source-stratum invariance verification.
7. `India` and `India_Wave2_New` remain separate analytical source strata and
   map to one reporting country.
8. No pooled global prevalence or pooled cross-country association is
   permitted.
9. The 986 unresolved all-zero outcome rows remain outside the primary
   denominator and are not labelled `Other`, missing or non-users by
   assumption.

## Isolation

- base lineage: published `v2.0.2`;
- default branch `main`: not modified by RC development;
- final tag `v3.0.0`: not created;
- final GitHub release: not created;
- final Zenodo version and DOI: not created.

## Open scientific gates

- IM-R6D official `s1b` mapping and categorical-descriptor decision;
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
