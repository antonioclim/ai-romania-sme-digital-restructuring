# Release notes — Outcome-Definition Sensitivity Analysis 3.0.0-rc1

## Status

Version `3.0.0-rc1` is an executable development release candidate for the
generic Outcome-Definition Sensitivity Analysis methodology. It is not the
final archival `v3.0.0` release and no new DOI is claimed.

## Methodological purpose

ODSA audits how substantively defensible categorical outcome definitions
change:

- reported level;
- positive-class composition;
- association with an organisational descriptor;
- subgroup order;
- the claims that the outcome can support.

The method is deliberately non-scalar. It does not combine these dimensions
into one quality score and it does not select one universally correct
definition.

## Formal-method consolidation included

The branch now adds:

- exact symmetric-difference decomposition for nested and non-nested
  definitions;
- total variation as a descriptive composition diagnostic;
- association contrasts with explicit non-monotonicity counterexamples;
- pairwise subgroup-order disagreement that separates strict reversals from
  tie changes;
- proof sketches for level monotonicity, coarsening non-identifiability and
  claim-admissibility closure;
- a novelty boundary relative to multiverse, specification-curve and
  Information Systems measurement approaches;
- executable formal-property tests.

## Candidate factorial simulation protocol

The candidate protocol includes:

- six controlled state-distribution mechanisms;
- four base sample sizes;
- balanced and skewed group allocation;
- within-broad and boundary-crossing misclassification;
- state-independent and project-heavy missingness;
- generating population, sampled true and observed layers;
- separate sampling, observation-process and total errors;
- explicit reporting of undefined association margins;
- Monte Carlo standard errors for event probabilities.

The CI subset is deterministic and verifies mechanics only. Its output is not
manuscript evidence. The full design remains subject to statistical freeze and
hostile review.

## Locked Study 1 regression values

```text
Active use:        54/172 = 31.4%; Cramér's V = 0.134
Project stage:     51/172 = 29.7%; Cramér's V = 0.350
Broad engagement: 105/172 = 61.0%; Cramér's V = 0.428
```

The public example contains aggregate counts only. It does not establish
national prevalence, unique firms, causal effects, verified deployment or
realised business value.

## Relationship to version 2.0.2

Version `2.0.2` remains the published aggregate reproduction package,
identified by DOI `10.5281/zenodo.21603732`. RC1 preserves that evidence
boundary while developing a reusable method. Final `v3.0.0` will supersede
`v2.0.2` only for the aligned Information & Management methodology article
and release workflow.

## Remaining release gates

Final `v3.0.0` requires:

1. literature-collision and journal-conversation lock;
2. hostile statistical review and full simulation freeze;
3. full simulation execution;
4. independent Study 2;
5. exact article–code–table–figure parity;
6. final ethics and data-governance wording;
7. complete Elsevier AI disclosure;
8. a frozen release asset and version-specific DOI;
9. hostile internal review with no unresolved critical issue.

## Citation

Do not cite this branch as a final archived release. Use the final
version-specific DOI after publication of `v3.0.0`.
