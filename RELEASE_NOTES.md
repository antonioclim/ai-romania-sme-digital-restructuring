# Release notes — Outcome-Definition Sensitivity Analysis 3.0.0-rc1

## Status

Version `3.0.0-rc1` is an executable development release candidate for the generic Outcome-Definition Sensitivity Analysis methodology. It is not the final archival `v3.0.0` release and no new DOI is claimed.

## Methodological purpose

ODSA audits how substantively defensible categorical outcome definitions change:

- reported level;
- positive-class composition;
- association with an organisational descriptor;
- subgroup order;
- recoverability after coarsening;
- the claims that the outcome can support.

The method is deliberately non-scalar. It does not identify one universally correct definition.

## Literature and journal lock

IM-R3 narrows the novelty claim. ODSA is not presented as the first analysis of alternative operationalisations. It is positioned as a specialised categorical state-map and inference-control audit, complementary to multiverse, specification-curve, vibration-of-effects, misclassification and IS measurement approaches.

The target article is locked as an *Information & Management* methodology paper with a formal framework, frozen simulation, Study 1, independent Study 2 and cross-study implications.

## Frozen simulation design

```text
Scenarios:                         6
Cells:                             432
Replications per cell:             4,000
Independent seed streams:          4
Replications per stream per cell:  1,000
Planned replicate rows:            1,728,000
Protocol SHA-256:                  157bc88f41ff68261253fb19e79cc2c0aeebe63a4687d1f1073edd25ecc0b8f3
```

The design follows an ADEMP structure and prespecifies Monte Carlo uncertainty, sparse-cell handling, reporting order and graphical summaries. Full execution remains prohibited until the engine implements the four-stream SeedSequence contract.

## Locked Study 1 regression values

```text
Active use:        54/172 = 31.4%; Cramér's V = 0.134
Project stage:     51/172 = 29.7%; Cramér's V = 0.350
Broad engagement: 105/172 = 61.0%; Cramér's V = 0.428
```

The public example contains aggregate counts only. It does not establish national prevalence, unique firms, causal effects, verified deployment or realised business value.

## Relationship to version 2.0.2

Version `2.0.2` remains the published aggregate reproduction package, identified by DOI `10.5281/zenodo.21603732`. RC1 preserves that evidence boundary while developing the methodology. Final `v3.0.0` will supersede `v2.0.2` only for the aligned *Information & Management* article and release workflow.

## Remaining release gates

1. full-engine conformance to the frozen seed-stream protocol;
2. full simulation execution and hostile result audit;
3. independent Study 2;
4. exact article–code–table–figure parity;
5. final ethics and data-governance wording;
6. complete Elsevier AI disclosure;
7. a frozen release asset and version-specific DOI;
8. hostile internal review with no unresolved critical issue.

## Citation

Do not cite this branch as a final archived release. Use the final version-specific DOI after publication of `v3.0.0`.
