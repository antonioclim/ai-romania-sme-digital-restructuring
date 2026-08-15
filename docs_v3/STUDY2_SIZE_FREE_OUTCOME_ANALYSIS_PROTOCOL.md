# Study 2 size-free outcome-analysis protocol

## Purpose

This protocol governs the first calculation of the World Bank FAT Study 2
outcomes. It was frozen after the structural, descriptor and dictionary audits
but before any production-planning outcome frequency was inspected.

The analysis is intentionally **size-free**. The prior audits disabled `s7`,
`e1` and `s1b` for Study 2 size diagnostics. No size-band rate, size-based
association or size-effect claim is permitted.

## Source and state reconstruction

The source is the pooled World Bank *Technology Sophistication Across
Establishments* dataset, reference `WLD_2019-2023_FAT_v01_M`, DOI
`10.48529/assd-3j65`.

The MOST-used production-planning state is reconstructed only from the complete
one-hot family:

| Field | Registered state |
|---|---|
| `ib9b1` | handwritten processes |
| `ib9b2` | computers with standard software |
| `ib9b3` | mobile apps or digital platforms |
| `ib9b4` | specialised software |
| `ib9b5` | ERP |

A row enters the common primary denominator only when exactly one field equals
one. The 986 previously identified all-zero rows remain excluded. Because
`ib9b6` is absent, those rows are not relabelled as `Other`, missing,
non-users or not applicable.

## Locked definitions

### Integrated planning

Positive state: ERP only.

Permitted wording:

> ERP is the establishment's most-used production-planning method.

This does not establish enterprise-wide transformation, superior performance
or causal effects.

### Specialised planning

Positive states: specialised software and ERP.

Permitted wording:

> Specialised or integrated software is the establishment's most-used
> production-planning method.

It does not imply that every positive establishment uses ERP.

### Digitally enabled planning

Positive states: standard software, mobile apps or digital platforms,
specialised software and ERP.

Permitted wording:

> The establishment's most-used production-planning method is computer- or
> platform-enabled rather than handwritten.

It does not imply specialised software, ERP or an integrated planning
architecture.

The exact pre-existing definition register has SHA-256:

```text
100d7a17cf415aa5faad4a3ec55787e224d29b04fe1ba9ee357db9647ecc77fa
```

## Common denominator and nesting

All three definitions use the same mapped observations. The locked order is:

```text
integrated_planning
  ⊂ specialised_planning
  ⊂ digitally_enabled_planning
```

Level monotonicity must therefore hold in every source stratum for both
weighted and unweighted rates.

## Source strata

The analysis uses sixteen analytical source labels from fifteen documented
reporting countries. `India` and `India_Wave2_New` remain separate analytical
strata and map to the same reporting country. They are not merged.

## Weighting

Primary descriptive results are within-source-stratum weighted rates:

```text
sum(base_wt × outcome) / sum(base_wt)
```

using positive numeric weights. The one previously detected missing weight is
excluded only from weighted calculations.

Unweighted rates are computational sensitivity results. No naive pooled global
rate is generated. Cross-stratum summaries give every source stratum equal
weight.

## Estimands

The local tool produces:

1. weighted and unweighted levels for each definition and source stratum;
2. positive-class composition for each definition and source stratum;
3. exact adjacent and full definition contrasts;
4. total-variation distance between positive-class compositions;
5. weighted-minus-unweighted rate sensitivity;
6. pairwise source-stratum order disagreement;
7. equal-stratum medians, quartiles, minima and maxima.

No source-stratum Cramér's V, p-value or confidence interval is produced.

## Pairwise order disagreement

For each pair of source strata, compare the sign of the rate difference under
two definitions. A pair is classified as:

- concordant;
- tie change;
- strict reversal.

This avoids interpreting a lexical tie-break as a substantive rank reversal.

## Cross-stratum synthesis

For each definition and contrast, report:

- number of eligible source strata;
- median;
- first and third quartiles;
- minimum and maximum.

Quantiles use linear interpolation at `h=(n-1)p`. These are distributions of
source-stratum estimates, not pooled prevalence estimates.

## Sparsity and disclosure

- source-stratum definition rates are suppressed when the positive or negative
  unweighted count is 1–4;
- compositions require at least 30 positive rows;
- an entire composition is suppressed when any contributing state count is
  1–4;
- contrasts are suppressed when their added-state count is 1–4 or either
  endpoint is suppressed;
- cells 1–4 are never exported;
- no row, identifier or source microdata enter the report.

Zero cells may be reported as zero.

## Inference boundary

The analysis is descriptive. The pooled file provides base weights, but this
protocol does not claim to reconstruct the complete design-based variance
estimator across all source studies. Accordingly, no inferential p-values,
confidence intervals or causal statements are produced.

## Validation gates

The execution report must pass E1–E12:

1. exact file identity;
2. expected rows, columns and row widths;
3. required field presence;
4. exact one-hot mapping totals;
5. source-stratum and reporting-country architecture;
6. weight integrity;
7. nested level monotonicity;
8. exact added-state identities;
9. composition identities;
10. adequate unsuppressed cross-stratum support;
11. absence of size, association, inferential and pooled-global outputs;
12. disclosure and no-row contract.

## Freeze

```text
outcome-analysis freeze SHA-256:
2491149bcc41596d8dbb9e509ee731447da70100de380d909daf45a4c46603be
```

A local result is not interpretation-ready until its sanitised JSON report has
been reviewed externally.
