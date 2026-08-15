# Study 2 structural-gate review

## Scope

This review evaluates the sanitised output produced locally from the authorised
World Bank FAT pooled CSV. The source microdata were not supplied to this
repository and are not reproduced here. The report contains structural metadata
and aggregates only, with no rows, state-specific counts, ODSA rates,
associations or country-level outcomes.

## Verified source identity

- dataset: *Technology Sophistication Across Establishments*;
- reference ID: `WLD_2019-2023_FAT_v01_M`;
- DOI: `10.48529/assd-3j65`;
- selected function: Production Planning — MOST-used method;
- pooled member: `fat0_raw_data_qje.csv`;
- size: 19,633,172 bytes;
- SHA-256: `f61a2c6e09f4763818ae1d4db8b330e97bffd8bb0824c2d833b79d728152bd17`;
- CRC-32: `4418a02b`.

The CSV contains 21,055 data rows and 723 columns. No row-width inconsistency,
duplicate header or empty header position was detected.

## Structural result

All ten mechanical structural checks passed. The required `country`, `e1` and
`base_wt` fields are present. The pooled file does not contain a direct `b9b`
field but does contain the complete binary MOST-used family `ib9b1`–`ib9b5`.
The observed domains of these fields are restricted to zero and one.

Exactly 20,069 rows contain a uniquely mapped state in the five-field family.
No attempted mapping failed. A further 986 rows contain no positive state in
that family and are therefore outside the primary state-defined denominator.
The structural report deliberately does not disclose the frequency of any
individual technology state.

## Adversarial interpretation

### 1. Sixteen file labels do not establish sixteen countries

The field contains sixteen source labels because `India` and
`India_Wave2_New` appear separately. The official record documents fifteen
countries. The two India labels must therefore remain separate source strata
until their sampling-wave provenance and weight compatibility are resolved.
They must not be reported as sixteen countries and must not be merged merely to
simplify presentation.

### 2. The absence of `ib9b6` prevents recovery of an explicit other state

The country questionnaires document an `Other` category for the direct MOST
item, but the pooled one-hot representation includes only `ib9b1`–`ib9b5`.
Consequently, the 986 all-zero records cannot be partitioned into `other`,
missing, not applicable or structurally ineligible cases using the frozen
fields alone. The primary denominator excludes them. The analysis must not
claim that there were no `Other` responses.

### 3. Employment-size completeness is a major unresolved gate

The `e1` field is numeric for 13,399 rows and missing for 7,656 rows, a missing
share of approximately 36.36%. This does not invalidate the dataset but it does
prevent immediate approval of the planned employee-size association analysis.
Before outcomes are inspected, the structurally available alternatives `s1b`,
`s7` and `e1` must be compared for meaning, completeness and cross-stratum
coverage. Any change from the originally proposed `e1` descriptor must be
recorded as a pre-outcome amendment rather than concealed as a routine data
cleaning decision.

### 4. Weight availability does not define a pooled estimand

`base_wt` is positive and numeric for 21,054 rows and missing for one row. This
supports within-source-stratum weighted summaries, subject to the official
sampling documentation. It does not by itself justify a single pooled
cross-country prevalence estimate or a weighted pooled association. A
cross-stratum synthesis must be prespecified and must preserve the distinction
between source strata and countries.

## Decision

```text
mechanical structural gate:       GO
semantic structural review:       GO WITH MANDATORY CAVEATS
outcome-analysis gate:             NO-GO
journal-submission gate:           NO-GO
```

The dataset is structurally suitable for the next pre-analysis phase. It is not
yet authorised for ODSA outcome calculation. IM-R6C must freeze:

1. the treatment of the two India source labels;
2. the primary size descriptor after a non-outcome completeness audit;
3. source-stratum eligibility thresholds;
4. weight use and the cross-stratum estimand;
5. the treatment and wording of the 986 unresolved all-zero cases;
6. the exact public-output and disclosure boundary.

No outcome definition, association or country-level result may be calculated
until that freeze is complete.
