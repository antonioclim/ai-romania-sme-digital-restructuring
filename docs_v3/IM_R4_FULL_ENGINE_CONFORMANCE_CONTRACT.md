# IM-R4 full-engine conformance contract

## Status

The frozen IM-R3 design was executed without changing its protocol file. The
protocol SHA-256 is:

```text
157bc88f41ff68261253fb19e79cc2c0aeebe63a4687d1f1073edd25ecc0b8f3
```

The full engine verifies this hash before generating any result.

## Execution architecture

The programme contains 432 factorial cells. Four independent NumPy
`SeedSequence` streams were spawned from root entropy `20260814`. Each stream
produced 1,000 replications per cell. The pooled evidence therefore contains:

```text
432 cells
× 4 streams
× 1,000 replications
= 1,728,000 replicate rows
```

Each stream was written to a separate lossless NumPy matrix. Pooling occurred
only after shape, row-count and stream-level audits passed.

## Evidential layers

The engine keeps three layers separate:

1. generating-population parameters;
2. sampled true values before observation error;
3. observed values after missingness and misclassification.

Sampling error, observation-process error and total error are therefore
reported separately.

## Frozen primary diagnostics

- narrow-versus-broad level contrast;
- narrow-versus-broad Cramér's V contrast;
- positive-class composition;
- pairwise subgroup-order disagreement;
- strict subgroup-order reversal;
- definition-specific group-rate changes;
- missingness and misclassification error;
- undefined-association frequency;
- Monte Carlo standard errors.

The sign of the Cramér's V contrast is not a quality score. No p-values are
calculated across simulation cells or replications.

## Conformance result

The full audit passed:

```text
stream count:                         4
cells:                                432
replications per cell:                4,000
replicate rows:                       1,728,000
undefined primary associations:       0
nested-level violations:              0
convergence failures:                 0
convergence warnings:                 1
maximum event-probability MCSE:       0.007905694150420948
target event-probability MCSE:        0.008
```

A complete second execution reproduced all stream matrices, cell summaries,
the pooled summary and the convergence outputs byte-for-byte.

## Convergence warning

One stream-level comparison exceeded the warning threshold of 4 standardised
units but remained below the failure threshold of 5. It occurred for the
pairwise order-disagreement diagnostic in one project-only, skewed,
misclassified and project-heavy-missingness cell. There were zero failures and
no repeated pattern across related cells. The byte-identical full rerun rules
out non-deterministic implementation drift, although it does not turn the
warning into a scientific result.

## Storage boundary

The repository stores compact manuscript-facing summaries and audits. The four
large replicate matrices are retained in the phase evidence archive and will
be incorporated into the frozen v3.0.0 release asset only after Study 2 and the
article-output crosswalk are complete.
