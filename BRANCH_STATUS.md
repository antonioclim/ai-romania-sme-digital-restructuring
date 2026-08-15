# Branch status — `im-v3.0.0-rc1`

This branch is the active development branch for Outcome-Definition Sensitivity Analysis version `3.0.0-rc1`.

## Current phase

IM-R6D-B is complete. The browser-only local audit passed its structural checks but the official pooled World Bank Data Dictionary XLSX does not contain `s1b` or value labels for codes 1, 2 and 3. The prespecified official-label gate D9 therefore failed.

The candidate mapping `1/2/3 → small/medium/large sampling-frame size strata` is rejected for the current Study 2 analysis. All Study 2 size-based diagnostics are disabled before any production-planning outcome is inspected.

The next phase is IM-R7-A: freeze and implement the Study 2 outcome analysis without a size descriptor.

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
IM-R6C report SHA-256:             f1a2197a8a60e37ffa6664f3e512beea448c875ddc9c86d60cadda1fa5250e8f
s7 valid / below five:             21,055 / 1,538
s7 below-five share:               7.305%
s7 primary numeric descriptor:     DISABLED
s7 threshold relaxation:           PROHIBITED
e1 size analysis:                  DISABLED
s1b observed codes:                1, 2, 3
s1b local report SHA-256:           cb524fadcf64d43b84603b421ea717647c18458dd2261069bb7e38ce4d6338d2
official dictionary SHA-256:       bf26b87b4801f4f6e64df90bcc7a2738f3c674683b2b3b2045ef0410b59af8ac
s1b official value labels:         NOT PROVIDED
s1b candidate mapping:             REJECTED
all size-based diagnostics:        DISABLED
s1b audit freeze SHA-256:          1e1169c2e8e85428fa28c48d3f792795dce09d52c153173b2a0af3a0c21daa88
s1b final decision SHA-256:        b2a89a389ea24508c40a1ea4d08577c0393fce170129557c708487866ac6a09b
analysis gate:                     NO-GO pending IM-R7-A freeze
replication executed:              no
submission gate:                   NO-GO
```

## Frozen methodological consequences

1. `s7` is not used as a cross-source-stratum primary numeric descriptor.
2. The 1% below-universe threshold is not relaxed after audit inspection.
3. The 1,538 below-five `s7` values are not dropped, repaired or relabelled by assumption.
4. `e1` is not used for a primary or secondary Study 2 size analysis.
5. `s1b` is never interpreted as a numeric worker count or current firm size.
6. `s1b` is not used as a categorical size descriptor because the official pooled dictionary does not provide its value labels.
7. No size-band outcome rate, size-based Cramér's V or size-effect claim is permitted.
8. `India` and `India_Wave2_New` remain separate analytical source strata and map to one reporting country.
9. No pooled global prevalence or pooled cross-country association is permitted.
10. The 986 unresolved all-zero outcome rows remain outside the primary denominator and are not relabelled by assumption.

## Retained Study 2 scope

The next prespecified analysis may include:

- weighted and unweighted outcome-definition levels within source stratum;
- positive-class composition within source stratum;
- exact contrasts between the frozen outcome definitions;
- source-stratum ordering and ordering changes across definitions;
- cross-stratum descriptive synthesis without a pooled global prevalence.

## Open scientific gates

- IM-R7-A outcome-analysis specification and SHA-256 freeze without size diagnostics;
- browser-only Study 2 execution and hostile result audit;
- secondary-use ethics and data-governance wording;
- reconstruction of the Information & Management manuscript;
- article–code–table–figure parity and final release audit;
- final Elsevier disclosure and submission preflight.

## Isolation and public-data boundary

- base lineage: published `v2.0.2`;
- default branch `main`: not modified by RC development;
- final tag `v3.0.0`: not created;
- final GitHub release and Zenodo version: not created;
- no respondent-level Study 1 data or World Bank microdata may enter the public workflow;
- the public World Bank Data Dictionary XLSX was reviewed only as documentation and is not required in the release.
