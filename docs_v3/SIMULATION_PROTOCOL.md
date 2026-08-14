# Candidate manuscript simulation protocol

## Status

This is the IM-R2 design candidate for the simulation study. The accompanying
`ci` execution verifies implementation mechanics only. It is not manuscript
evidence and must not be cited as a completed Monte Carlo study. The full
design will be frozen and executed only after the novelty boundary and
statistical design have passed separate hostile audits.

## 1. Purpose

The simulation is not intended to prove the arithmetic fact that a nested
broader definition has an equal or higher level. Its purpose is to establish
the conditions under which alternative categorical outcome definitions alter:

- association strength;
- subgroup order;
- positive-class composition;
- sensitivity to missingness;
- sensitivity to state misclassification.

It also separates three evidential layers that must not be conflated:

1. the generating population parameter;
2. the sampled true value before observation error;
3. the observed value after missingness and misclassification.

## 2. Simulation questions

### SQ1 — association direction

Under which controlled state distributions does broadening strengthen, weaken
or leave unchanged Cramér's \(V\)?

### SQ2 — subgroup order

When do active-use and broad-engagement definitions imply different pairwise
subgroup orders?

### SQ3 — composition

How does the project-stage share of the broad positive class vary across
mechanisms and sample sizes?

### SQ4 — within-broad misclassification

How does active/project swapping affect the narrow outcomes while preserving
the broad positive boundary?

### SQ5 — boundary-crossing misclassification

How does project/other swapping affect both level and association for broad
engagement?

### SQ6 — missingness

How do state-independent and project-heavy missingness alter level,
association and subgroup-order diagnostics?

### SQ7 — error decomposition

How much observed deviation is attributable to finite sampling and how much
is attributable to the observation process?

## 3. Controlled scenario families

| Scenario | Active-use mechanism | Project-stage mechanism | Diagnostic role |
|---|---|---|---|
| `null_same_mixture` | equal across groups | equal across groups | finite-sample baseline and null bias |
| `aligned_gradient` | increases | increases | definitions broadly agree on direction |
| `project_only_gradient` | constant | increases | broad association emerges while active association remains null |
| `compensating_gradient` | decreases | increases by the same amount | active association remains while broad association is null |
| `rank_reversal` | decreases | increases strongly | active and broad group orders reverse |
| `mixed_order` | non-monotone | non-monotone | partial disagreement and a generating broad-outcome tie |

These are controlled mechanisms, not fitted approximations to the Romanian
response set.

## 4. Factorial design candidate

### Full candidate

- per-group base sample size: 50, 100, 250 and 500;
- allocation: balanced and skewed;
- misclassification: none, 10% active/project swapping and 10%
  project/other swapping;
- missingness: none, 10% state-independent and project-heavy;
- scenario: six controlled mechanisms;
- replications per cell: 1,000.

The design contains 432 cells and 432,000 candidate replicates.

At 1,000 replications, the maximum Monte Carlo standard error for an event
probability is approximately 0.0158, corresponding to an approximate 95%
half-width of 0.031 at \(p=0.5\). The final freeze must decide whether this
precision is adequate for every planned event estimate.

### Continuous-integration subset

The `ci` mode uses:

- all six scenario mechanisms;
- per-group base sizes 60 and 150;
- balanced allocation;
- no misclassification and 10% active/project swapping;
- no missingness;
- 40 replications per cell.

It verifies parsing, deterministic seeding, output completeness and test
integration only.

## 5. Observation model

For each group and replicate:

1. draw true state counts from the scenario-specific multinomial distribution;
2. calculate sampled true levels and associations;
3. apply state-specific missingness;
4. apply a row-stochastic misclassification matrix to retained cases;
5. calculate observed levels, associations, compositions and subgroup orders.

The active/project swap remains within the broad positive set. Conditional on
retention, it preserves the broad positive count exactly while potentially
biasing the narrow active-use and project-stage outcomes. The project/other
swap crosses the broad boundary and can bias broad engagement.

## 6. Population parameters and errors

For each cell, generating population levels are weighted averages of the
group-specific positive probabilities using the actual rounded group sizes.

Population Cramér's \(V\) is calculated from the joint probability table for
group and binary outcome, without introducing an arbitrary total sample size.

Each replicate records:

\[
\text{sampling error}
=
\text{sampled true value}
-
\text{population value},
\]

\[
\text{observation error}
=
\text{observed value}
-
\text{sampled true value},
\]

\[
\text{total error}
=
\text{observed value}
-
\text{population value}.
\]

This decomposition prevents observation-process bias from being confused with
ordinary finite-sample variability.

## 7. Primary outputs

The full design will report, by cell:

- broad-minus-active level contrast;
- broad-minus-active Cramér's \(V\) contrast;
- cross-definition pairwise subgroup-order disagreement;
- strict cross-definition reversal;
- share of right-only added states within the broader positive class;
- project-stage share of broad positives for the present application;
- level sampling, observation and total error;
- association sampling, observation and total error;
- active and broad subgroup-order error against the generating order;
- missing-data share;
- number of undefined association replicates.

For continuous metrics, the report will include the number defined, mean,
standard deviation, median and 5th and 95th percentiles. For event metrics, it
will include the Monte Carlo estimate, the number defined and Monte Carlo
standard error.

## 8. Prespecified interpretation rules

1. A positive \(\Delta V\) does not mean that the broader definition is
   superior.
2. A negative \(\Delta V\) does not mean that the narrower definition is
   superior.
3. Project share within a broad outcome is composition, not error, unless the
   broad outcome is labelled as active use.
4. Rank disagreement matters only when the metric is used for ranking,
   prioritisation or allocation.
5. Every prespecified cell must be reported or its failure documented.
6. Undefined margins must be counted, not silently deleted.
7. ODSA diagnostics must not be collapsed into one scalar score.
8. No universal threshold for material sensitivity will be selected after
   examining the results.
9. Claims about managerial decision quality require a separate decision model
   or experiment.

## 9. Statistical audit required before the full run

Before the full execution:

- decide whether 1,000 replications per cell provide adequate Monte Carlo
  precision;
- run convergence checks using at least two independent seed streams;
- prespecify treatment of sparse and undefined margins;
- decide whether Cramér's \(V\) remains the sole primary association measure
  or is accompanied by pairwise risk differences;
- confirm the tie tolerance for population and observed subgroup rates;
- verify that allocation and sample-size factors are not redundant;
- lock the reporting order before reading full results;
- define graphical summaries before execution;
- record exact dependency versions and runner environment;
- confirm that the simulation contains no human-participant records.

## 10. Reproducibility contract

The simulation engine must produce:

- an exact protocol snapshot;
- a design-validation audit;
- one row per replicate;
- one summary row per cell;
- deterministic outputs for a fixed seed and design;
- a non-zero exit status for invalid probabilities, matrices or factor names;
- an explicit flag that CI output is not manuscript evidence.

## 11. Claims permitted at the end of IM-R2

This phase establishes that:

- the scenario mechanisms are encoded;
- the CI subset is deterministic and executable;
- level, association and subgroup order are distinct diagnostics;
- nested definitions do not constrain association direction or subgroup
  order;
- the full design is specified but not executed as manuscript evidence.

It does not establish final Monte Carlo probabilities, robustness thresholds,
managerial benefit or empirical validation of ODSA.
