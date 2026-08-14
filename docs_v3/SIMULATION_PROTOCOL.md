# Frozen manuscript simulation protocol

## Status

This protocol was frozen in IM-R3 before any full manuscript simulation results were generated. The continuous-integration execution remains a mechanics check and is not manuscript evidence.

```text
Protocol schema:              2.0
Protocol SHA-256:             157bc88f41ff68261253fb19e79cc2c0aeebe63a4687d1f1073edd25ecc0b8f3
Freeze date:                  2026-08-14
Full cells:                   432
Replications per cell:        4,000
Independent streams:          4
Replications per stream:      1,000 per cell
Total full replicate rows:    1,728,000
Full execution authorised:    NO
```

The design will be changed only through a versioned amendment recording the reason, old and new hashes and whether any full results had already been viewed.

## 1. ADEMP structure

### Aims

The simulation maps the conditions under which alternative categorical outcome definitions change:

- reported level;
- positive-class composition;
- association with a grouping variable;
- subgroup order;
- sensitivity to missingness and state misclassification.

It separates generating-population values, sampled true values and observed values.

### Data-generating mechanisms

The primary design crosses:

- six controlled group-by-state mechanisms;
- four per-group base sample sizes;
- two group-allocation profiles;
- three misclassification profiles;
- three missingness profiles.

The scenarios are mechanisms, not fitted estimates of the Romanian population.

### Estimands

For each definition, the generating population provides:

- overall level;
- group-specific rates;
- Cramér's V for group by binary outcome;
- subgroup order;
- positive-class composition.

### Methods

The same registered ODSA diagnostics are applied at three layers:

1. generating population;
2. sampled true data;
3. observed data after missingness and misclassification.

### Performance measures

The design reports definition contrasts, sampling error, observation-process error, total error, subgroup-order disagreement, undefined-result frequency and Monte Carlo standard errors.

## 2. Simulation questions

### SQ1 — association

Under which state distributions does broadening strengthen, weaken or leave unchanged Cramér's V?

### SQ2 — subgroup order

When do active-use and broad-engagement definitions imply different pairwise subgroup orders?

### SQ3 — composition

How does the project-stage share of the broad positive class vary across mechanisms and observation processes?

### SQ4 — within-broad misclassification

How does active/project swapping affect narrow outcomes while preserving the broad boundary conditional on retention?

### SQ5 — boundary-crossing misclassification

How does project/other swapping affect the level and association of broad engagement?

### SQ6 — missingness

How do state-independent and project-heavy missingness change the diagnostics?

### SQ7 — error decomposition

How much observed deviation is attributable to finite sampling and how much to the observation process?

## 3. Controlled mechanisms

| Scenario | Active-use mechanism | Project-stage mechanism | Diagnostic role |
|---|---|---|---|
| `null_same_mixture` | equal across groups | equal across groups | finite-sample baseline |
| `aligned_gradient` | increases | increases | definitions agree in broad direction |
| `project_only_gradient` | constant | increases | broad association emerges while active association remains null |
| `compensating_gradient` | decreases | increases equally | active association remains while broad association is null |
| `rank_reversal` | decreases | increases strongly | active and broad subgroup orders reverse |
| `mixed_order` | non-monotone | non-monotone | partial disagreement and a generating tie |

## 4. Full design

```text
6 scenarios
× 4 per-group base sample sizes
× 2 allocation profiles
× 3 misclassification profiles
× 3 missingness profiles
= 432 cells

432 cells × 4,000 replications = 1,728,000 replicate rows
```

The primary simulation is aligned with the nested active-use versus broad-engagement contrast in Study 1. Non-nested generality is addressed through exact identities and counterexamples rather than by introducing substantively artificial labels into the main factorial design.

## 5. Monte Carlo precision

For an event probability from 4,000 pooled replications, the worst-case Monte Carlo standard error at `p=0.5` is approximately 0.00791 and the approximate 95% half-width is 0.01550.

Event probabilities and continuous means must be accompanied by Monte Carlo standard errors. Replication count is justified by precision, not by convention.

## 6. Seed streams

The full run must use `numpy.random.SeedSequence` with root entropy `20260814` to spawn four independent streams. Each stream must contain exactly 1,000 replications for every cell.

Pooling is permitted only after each stream passes:

- cell completeness;
- replication-count completeness;
- valid-probability checks;
- output-schema checks;
- convergence inspection.

The current engine has not yet been certified against this full stream contract, so the full run remains prohibited.

## 7. Observation model

For each group and replicate:

1. draw true state counts from the scenario-specific multinomial distribution;
2. calculate sampled true diagnostics;
3. apply state-specific missingness;
4. apply a row-stochastic misclassification matrix to retained cases;
5. calculate observed diagnostics.

The active/project swap remains within the broad positive set. The project/other swap crosses the broad boundary.

## 8. Error decomposition

```text
sampling error = sampled true value - population value
observation-process error = observed value - sampled true value
total error = observed value - population value
```

## 9. Primary outputs

- broad-minus-active level contrast;
- broad-minus-active Cramér's V contrast;
- cross-definition pairwise subgroup-order disagreement;
- strict cross-definition reversal;
- share of added states in the broader positive class;
- project-stage share of broad positives;
- level and association error decomposition;
- missing-data share;
- undefined-association fraction.

Secondary outputs include definition-specific group-rate vectors and maximum and mean absolute group-rate changes.

## 10. Undefined-result policy

Undefined outcomes are never silently removed or imputed.

```text
undefined fraction <= 1%:            normal reporting
undefined fraction >1% and <=5%:     warning
undefined fraction >5%:              no comparative claim for that metric/cell
```

Summaries are conditional on defined values and must report the defined denominator.

## 11. Reporting and graphical lock

The reporting order is frozen before the full run:

1. completeness;
2. generating-population parameters;
3. levels and composition;
4. association contrasts;
5. subgroup order;
6. error decomposition;
7. observation-process robustness;
8. undefined-result audit.

The figure plan is also frozen. No cell may be selected because it looks unusually dramatic.

## 12. Interpretation rules

1. Positive ΔV does not imply a better broad definition.
2. Negative ΔV does not imply a better narrow definition.
3. Project share within a broad outcome is composition, not error, unless the broad outcome is mislabelled as active use.
4. Order disagreement matters when a metric is used for ranking or allocation.
5. Every prespecified cell is reported or its failure documented.
6. No p-values are calculated across simulation replications or cells.
7. No post-result universal materiality threshold is selected.
8. ODSA diagnostics are not collapsed into one scalar score.
9. Managerial decision quality requires separate evidence.

## 13. Full-execution gate

Before IM-R4 execution, the engine must:

- implement the four-stream SeedSequence policy;
- verify the frozen protocol SHA-256;
- calculate MCSE for continuous means as well as events;
- produce stream-specific and pooled audit files;
- stop on any incomplete cell;
- record the exact dependency and runner environment.

```text
Design frozen:                    YES
Full results viewed:              NO
Protocol hash locked:             YES
Engine stream compliance:         PENDING
Full execution:                   NO-GO
```
