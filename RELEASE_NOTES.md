# Release notes — Outcome-Definition Sensitivity Analysis 3.0.0-rc1

## Status

Version `3.0.0-rc1` is an executable development release candidate for the generic Outcome-Definition Sensitivity Analysis methodology. It is not the final archival `v3.0.0` release and no new DOI is claimed.

## Methodological purpose

ODSA audits how alternative defensible definitions of a categorical outcome change:

- the reported level;
- the positive-class composition;
- association with an organisational descriptor;
- group-specific rates and rankings;
- the wording of claims that the outcome can support.

The method is deliberately non-scalar. It does not combine these dimensions into a single quality score and it does not select one universally correct definition.

## Included in RC1

- installable Python package `odsa`;
- command-line interface;
- formal state-space and definition registers;
- nested, disjoint and overlapping definition diagnostics;
- Wilson intervals, Pearson chi-square and Cramér's V;
- composition, ranking and claim-admissibility diagnostics;
- aggregate-only Study 1 example reproducing the locked Romanian organisational AI counts;
- deterministic smoke simulation;
- methodological and empirical regression tests;
- GitHub Actions CI for the RC branch;
- formal method, reporting, ethics, data-governance and AI-assistance documentation.

## Locked Study 1 regression values

```text
Active use:        54/172 = 31.4%; Cramér's V = 0.134
Project stage:     51/172 = 29.7%; Cramér's V = 0.350
Broad engagement: 105/172 = 61.0%; Cramér's V = 0.428
```

The public example contains aggregate counts only. It does not establish national prevalence, unique firms, causal effects, verified deployment or realised business value.

## Relationship to version 2.0.2

Version `2.0.2` remains the published aggregate reproduction package and is identified by DOI `10.5281/zenodo.21603732`. RC1 preserves that evidence boundary while developing a reusable methodology. Final `v3.0.0` will supersede `v2.0.2` only for the aligned Information & Management methodological article and release workflow.

## Remaining release gates

The final `v3.0.0` release requires:

1. a manuscript-final simulation design;
2. independent Study 2 replication;
3. exact article–code–table–figure parity;
4. final ethics and data-governance wording;
5. complete Elsevier AI disclosure;
6. a frozen release asset and version-specific DOI;
7. hostile internal review with no unresolved critical issue.

## Citation

Do not cite this branch as a final archived release. Use the final version-specific DOI after publication of `v3.0.0`.
