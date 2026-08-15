# Branch status — `im-v3.0.0-rc1`

This branch is the active development branch for Outcome-Definition
Sensitivity Analysis version `3.0.0-rc1`.

## Current phase

IM-R6D-A is open. IM-R6C remains closed with a frozen descriptor failure:
1,538 of 21,055 valid `s7` values (7.305%) were below the prespecified
five-worker universe threshold, exceeding the frozen 1% maximum. `s7` is
disabled as the primary numeric size descriptor, the threshold will not be
relaxed and `e1` will not be promoted to primary after the failure.

IM-R6D asks whether `s1b` may be used only as a categorical sampling-frame size
stratum. The candidate mapping `1/2/3 → small/medium/large` has been frozen but
is **not accepted**. Acceptance requires both a browser-only local invariance
audit and review of the official pooled World Bank Data Dictionary XLSX. `s1b`
will never be interpreted as a numeric worker count or current establishment
size. No production-planning outcome has been inspected.

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
IM-R6C report SHA-256:              f1a2197a8a60e37ffa6664f3e512beea448c875ddc9c86d60cadda1fa5250e8f
s7 valid / below five:             21,055 / 1,538
s7 below-five share:               7.305%
primary numeric descriptor:        DISABLED
s7 threshold relaxation:           PROHIBITED
e1 promotion to primary:           PROHIBITED
s1b observed codes:                1, 2, 3
s1b candidate mapping:             1/2/3 → small/medium/large frame strata
s1b candidate status:              NOT ACCEPTED
s1b audit freeze SHA-256:          1e1169c2e8e85428fa28c48d3f792795dce09d52c153173b2a0af3a0c21daa88
official pooled dictionary review: PENDING
local IM-R6D audit:                PENDING
analysis gate:                     NO-GO
replication executed:              no
submission gate:                   NO-GO
```

## Frozen methodological consequences

1. `s7` is not used as a cross-source-stratum primary numeric descriptor.
2. The 1% below-universe threshold is not relaxed after audit inspection.
3. The 1,538 below-five `s7` values are not dropped, repaired or relabelled by
   assumption.
4. `e1` is not promoted to the primary descriptor.
5. `s1b` is never interpreted as a numeric worker count or current firm size.
6. The candidate `s1b` mapping remains unaccepted until the official pooled
   Data Dictionary and local invariance report are jointly reviewed.
7. If that mapping cannot be verified before outcome inspection, all Study 2
   size-based diagnostics are disabled.
8. `India` and `India_Wave2_New` remain separate analytical source strata and
   map to one reporting country.
9. No pooled global prevalence or pooled cross-country association is
   permitted.
10. The 986 unresolved all-zero outcome rows remain outside the primary
    denominator and are not relabelled by assumption.

## Open scientific gates

- public pooled Data Dictionary XLSX review;
- browser-only IM-R6D local `s1b` invariance audit;
- final categorical-descriptor decision and SHA-256 closure;
- final Study 2 analysis-specification closure;
- secondary-use ethics and data-governance wording;
- locked Study 2 execution and hostile result audit;
- reconstruction of the Information & Management manuscript;
- article–code–table–figure parity and final release audit;
- final Elsevier disclosure and submission preflight.

## Isolation and public-data boundary

- base lineage: published `v2.0.2`;
- default branch `main`: not modified by RC development;
- final tag `v3.0.0`: not created;
- final GitHub release and Zenodo version: not created;
- no respondent-level Study 1 data or World Bank microdata may enter the public
  workflow;
- the public World Bank Data Dictionary XLSX may be reviewed separately from
  the restricted source microdata.
