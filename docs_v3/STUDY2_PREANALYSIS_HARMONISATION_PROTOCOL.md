# Study 2 pre-analysis harmonisation protocol

## Purpose

This protocol freezes the source-stratum, size-descriptor, weight and
reporting rules before any Study 2 technology outcome is calculated.

## Evidence already available

The pooled file contains 21,055 rows and 723 columns. The production-planning
MOST-used state is recoverable for 20,069 rows through `ib9b1`–`ib9b5`, with
zero attempted mapping failures. The employee field `e1` is missing for 7,656
rows. These facts were established without disclosing state-specific outcome
counts.

## Pre-outcome descriptor amendment

The IM-R5 registry nominated `e1` as the primary size descriptor. IM-R6B showed
that `e1` is missing for 36.36% of rows. Before any outcome inspection, the
analysis is amended as follows:

1. `s7` — Number of workers (screener) — becomes the primary numeric size
   candidate.
2. `e1` — Total number of workers by the end of the reference year — becomes a
   complete-case sensitivity descriptor.
3. `s1b` — Sampling size — is used only as a sample-frame validation field and
   never as a substitute numeric worker count.
4. If `s7` fails the frozen quality gates, employee-size association analysis
   is disabled rather than moved to another convenient field after outcomes
   are seen.

This amendment is methodological provenance, not routine data cleaning.

## Frozen `s7` quality gates

The primary numeric descriptor is authorised only when all conditions hold:

- numeric non-negative integer values on at least 95% of all rows;
- valid-value completeness of at least 90% within every source stratum with at
  least 100 rows;
- values below the five-worker survey universe on no more than 1% of otherwise
  valid rows;
- non-integer values on no more than 0.1% of non-missing numeric rows;
- at least ten source strata contain at least 100 records with `s7 >= 5`.

If any condition fails, no primary size-association result is produced.

## Frozen size bands

For `s7` and the secondary complete-case `e1` sensitivity:

- small: 5–19 workers;
- medium: 20–99 workers;
- large: 100 or more workers.

Values below five are reported as outside the target-universe band and are not
silently included in the small category.

## Source-stratum harmonisation

The pooled file contains sixteen source labels from fifteen documented
countries.

- `India` and `India_Wave2_New` remain separate analytical source strata.
- Both map to the reporting country `India`.
- They are not merged for primary estimation.
- Results are described as sixteen source strata from fifteen countries.
- Brazil and India retain the source documentation's subnational-coverage
  caveat.
- `BurkinaFaso`, `Korea` and `Vietnam` may receive presentation labels only;
  their stored source labels are preserved.

## Weight policy

- weighted level estimates are calculated within source stratum using positive
  `base_wt`;
- the one record without a valid weight is excluded only from weighted
  estimates and may remain in unweighted sensitivity estimates if otherwise
  eligible;
- unweighted rates are reported as sensitivity estimates;
- both unweighted Cramér's V and within-stratum weight-normalised descriptive
  Cramér's V are reported;
- neither form receives an inferential p-value;
- disagreement between weighted and unweighted sensitivity directions is
  disclosed rather than adjudicated post hoc;
- no pooled global prevalence or pooled cross-country association is reported.

## Source-stratum eligibility and sparse-result rules

A source stratum may contribute:

- level estimates when it has at least 100 outcome-eligible records;
- a displayed size-band rate only when the relevant band has at least 30
  records;
- a size-association diagnostic only when at least two size bands have at
  least 30 records and the outcome has at least 20 positive and 20 negative
  cases.

Sparse estimates are marked `not estimated`; bands are not merged after
outcomes are seen.

## Cross-stratum synthesis

The manuscript may report, separately for weighted and unweighted estimates:

- number of eligible source strata;
- median;
- interquartile range;
- minimum and maximum;
- count of positive, negative and near-zero definition contrasts;
- count of source strata with stable and changed subgroup ordering.

No result is labelled a worldwide or fifteen-country prevalence estimate.

## Unresolved all-zero records

The 986 rows with no positive `ib9b1`–`ib9b5` indicator remain outside the
primary outcome denominator. Because `ib9b6` is absent, they are not labelled
as `Other`, non-users or missing by assumption.

## Public-output boundary

Permitted:

- source metadata and hashes;
- field names and code domains;
- non-outcome completeness and consistency summaries;
- prespecified analysis code;
- non-disclosive derived aggregate results.

Prohibited:

- World Bank microdata;
- row-level extracts;
- establishment identifiers;
- source-stratum microdata;
- any material that permits reconstruction of individual records.

## Stop rule

The local IM-R6C audit may select `s7` under the frozen rules, but no Study 2
technology outcome may be calculated until the sanitised report is externally
reviewed and the freeze hash is recorded.
