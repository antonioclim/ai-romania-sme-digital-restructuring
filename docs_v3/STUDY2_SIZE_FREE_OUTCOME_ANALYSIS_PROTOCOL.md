# Study 2 size-free outcome-analysis protocol

> **Implementation status, 15 August 2026.** The original analytical
> specification remains frozen. The first IM-R7A browser execution is
> quarantined because its row classifier labelled 986 structurally unresolved
> one-hot rows as invalid. Corrective implementation amendment 01 changes only
> that classification metadata and adds the aggregate-identity gate E13. It
> does not change a definition, denominator membership rule, weight, estimand,
> threshold, suppression rule or claim boundary.

## Purpose

This protocol governs the calculation of the World Bank FAT Study 2 outcomes.
Its scientific choices were frozen after the structural, descriptor and
dictionary audits and before any production-planning outcome frequency was
rendered.

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
one and every remaining field is a documented zero. The previously established
20,069 complete one-hot rows enter the common denominator. The remaining 986
rows are retained outside that denominator as unresolved or structurally
missing. Because `ib9b6` is absent, they are not relabelled as `Other`, missing,
non-users or not applicable.

Corrective amendment 01 distinguishes:

1. complete one-hot rows;
2. all-zero unresolved rows;
3. structurally missing unresolved rows;
4. one-positive rows with missing companion fields, which remain ambiguous;
5. multiple-positive rows;
6. non-missing non-binary invalid rows.

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

The corrected execution report must pass E1–E13:

1. exact file identity;
2. expected rows, columns and row widths;
3. required field presence;
4. exact complete one-hot mapping and transparent unresolved-row
   classification;
5. source-stratum and reporting-country architecture;
6. weight integrity;
7. nested level monotonicity;
8. exact added-state identities;
9. composition identities;
10. adequate unsuppressed cross-stratum support;
11. absence of size, association, inferential and pooled-global outputs;
12. disclosure and no-row contract;
13. byte-identical canonical aggregate-result fingerprint relative to the
    quarantined failed run.

E13 is a post-exposure safeguard. It ensures that the implementation correction
cannot silently change an aggregate result after the first run rendered
outcomes.

## Freeze and corrective amendment

```text
original outcome-analysis freeze SHA-256:
2491149bcc41596d8dbb9e509ee731447da70100de380d909daf45a4c46603be

implementation amendment 01 SHA-256:
03244a3761052b294ab122999ff061b8f5932b4332b2ad7bd713e5f2f255e1ef

effective corrected contract SHA-256:
f096825efd95c0afc699410d174517e3797ee4610b8a392c5809bdfd20789d87

quarantined aggregate payload fingerprint SHA-256:
b18fa495616d28bcb315634c6247e2c8c94aa10724759e82cabed19a03251fe0
```

A local result is not interpretation-ready until its corrected sanitised JSON
report passes E1–E13 and is reviewed externally in IM-R7B.
