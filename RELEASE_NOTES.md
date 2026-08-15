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

The branch includes:

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

## Frozen factorial simulation and full execution

The frozen protocol includes:

- six controlled state-distribution mechanisms;
- four base sample sizes;
- balanced and skewed group allocation;
- within-broad and boundary-crossing misclassification;
- state-independent and project-heavy missingness;
- generating population, sampled true and observed layers;
- separate sampling, observation-process and total errors;
- explicit reporting of undefined association margins;
- Monte Carlo standard errors for event probabilities.

The frozen full design was executed through four independent seed streams. It
contains 432 cells, 4,000 pooled replications per cell and 1,728,000 replicate
rows. All core matrices and summaries were reproduced byte-for-byte in a
complete independent rerun. CI and smoke outputs remain engineering evidence
only.

## IM-R4 full-result status

```text
full streams:                         4
factorial cells:                      432
replications per cell:                4,000
replicate rows:                       1,728,000
maximum event-probability MCSE:       0.007905694150420948
undefined primary associations:       0
nested-level violations:              0
convergence failures:                 0
independent core rerun:                byte-identical
```

The results demonstrate that nesting guarantees level monotonicity but does
not constrain association strength or subgroup order. They do not identify one
universally correct definition or establish improved managerial decisions.

## Study 2 selection freeze

The independent Study 2 source has been conditionally selected before
microdata acquisition and before outcome inspection:

```text
source:              World Bank Technology Sophistication Across Establishments
survey reference:    WLD_2019-2023_FAT_v01_M
dataset DOI:         10.48529/assd-3j65
focal function:      production-planning MOST-used method
selection score:     20/21
microdata acquired:  no
results inspected:   no
```

The locked outcome definitions are:

```text
integrated_planning
    = {ERP}

specialised_planning
    = {specialised software, ERP}

digitally_enabled_planning
    = {standard software, mobile apps or digital platforms,
       specialised software, ERP}
```

Selection is conditional on a ten-part structural acquisition gate. The
source microdata are governed by the World Bank Microdata Library terms and
must not be redistributed through this repository or the final Zenodo asset.
A fixed reserve order is retained if the selected record fails the structural
gate.

Study 2 is not yet empirical evidence and no independent-replication claim is
made at this stage.

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

Final `v3.0.0` still requires:

1. lawful acquisition and structural verification of the selected Study 2
   source;
2. secondary-use ethics and data-governance wording;
3. locked Study 2 execution and hostile result audit;
4. reconstruction of the Information & Management manuscript;
5. exact article–code–table–figure parity;
6. complete Elsevier AI disclosure;
7. a frozen release asset and version-specific DOI;
8. hostile internal review with no unresolved critical issue.

## Citation

Do not cite this branch as a final archived release. Use the final
version-specific DOI after publication of `v3.0.0`.
