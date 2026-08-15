# Study 2 `s1b` documentation and invariance protocol

## Purpose

IM-R6C disabled `s7` as the primary cross-source-stratum numeric size
descriptor because 7.305% of its valid values were below the frozen
five-worker universe threshold. `e1` is too incomplete to become the primary
descriptor, and `s1b` is never interpreted as a numeric worker count.

IM-R6D asks a narrower question:

> May `s1b` be used only as a categorical sampling-frame size-stratum
> descriptor in secondary Study 2 diagnostics?

## Official-source boundary

The pooled World Bank catalogue identifies `s1b` as **Sampling size**. The FAT
collection covers formal firms with five or more workers and uses firm size as
a sampling dimension. Country-level designs are not identical: for example,
Croatia documents three strata (5–19, 20–99 and 100+), whereas Poland
documents six finer strata. Consequently, the pooled codes must not be
interpreted from a single country design.

The final mapping requires the official pooled Data Dictionary XLSX. The local
CSV alone cannot establish the semantic labels of codes 1, 2 and 3.

## Frozen candidate mapping

The local audit tests the candidate mapping:

```text
1 → small sampling-frame stratum
2 → medium sampling-frame stratum
3 → large sampling-frame stratum
```

This mapping is **not accepted** until the official pooled dictionary is
reviewed.

## Local audit scope

The browser-only tool reads only:

```text
country
s1b
s7
e1
```

It verifies:

1. exact file identity;
2. pooled dimensions;
3. complete `s1b` code domain;
4. use of codes 1, 2 and 3 across all source strata;
5. sixteen source labels mapped to fifteen reporting countries;
6. source-stratum-specific code counts;
7. descriptive agreement with valid `s7` size bands;
8. descriptive agreement with valid `e1` size bands;
9. ordinal median ordering by code where cell support is adequate;
10. exclusion of all technology-outcome fields and row-level material.

Numeric concordance is a hostile plausibility diagnostic, not a substitute for
official value labels. A sampling-frame category need not exactly equal a
current or reference-year worker count.

## Final acceptance rule

`s1b` may be accepted only if all conditions hold:

- the official pooled dictionary explicitly maps codes 1, 2 and 3 to small,
  medium and large size strata, or semantically equivalent labels;
- the pooled CSV contains only those three non-missing codes;
- the same code domain is present across the sixteen source strata;
- the local audit reveals no structural evidence that the code order is
  reversed across the pooled source strata;
- the manuscript calls it a **sampling-frame size stratum**, never current
  establishment size or employee count.

If any necessary condition fails, all Study 2 size-based diagnostics are
disabled.

## Permitted claim if accepted

> Results differed across the small, medium and large sampling-frame size
> strata recorded in the pooled FAT file.

## Prohibited claims

- current firm size;
- actual employee count;
- verified growth or downsizing;
- causal size effects;
- a globally harmonised statutory SME classification;
- comparability with the Study 1 employee bands without an explicit
  measurement caveat.

## Stop rule

No Study 2 technology outcome may be calculated until the local JSON and the
official Data Dictionary XLSX have both been reviewed and a final SHA-256
decision record has been committed.
