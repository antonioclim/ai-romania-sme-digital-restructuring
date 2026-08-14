# Hostile statistical review and simulation freeze

## 1. Executive verdict

The IM-R2 candidate simulation is structurally sound but 1,000 replications per cell would estimate a worst-case event probability near 0.5 with a Monte Carlo standard error of approximately 0.0158. That is too coarse for the planned event summaries if they are to be interpreted beyond one decimal place.

The design is therefore frozen at 4,000 pooled replications per cell, implemented as four independently spawned streams of 1,000 replications. This yields a worst-case event-probability Monte Carlo standard error below 0.008 and an approximate 95% half-width below 0.016.

The freeze concerns the design. Full execution remains prohibited until the engine implements the stream policy and passes the protocol-hash test.

## 2. ADEMP audit

### Aims

The simulation maps method behaviour rather than trying to prove arithmetic identities already established analytically. It asks when alternative definitions change association, subgroup order, composition and sensitivity to missingness or misclassification.

### Data-generating mechanisms

The frozen primary design contains:

- six controlled group-by-state mechanisms;
- four per-group base sample sizes;
- balanced and skewed allocations;
- no misclassification, within-broad swapping and boundary-crossing swapping;
- no missingness, state-independent missingness and project-heavy missingness.

This is a 6 × 4 × 2 × 3 × 3 design with 432 cells.

### Estimands

Generating-population parameters are calculated before sampling and observation error:

- definition-specific level;
- definition-specific group-rate vector;
- Cramér's V for group by binary outcome;
- subgroup order;
- positive-class composition.

### Methods

The same ODSA diagnostics are applied to the generating population, sampled true data and observed data. Cramér's V is retained as the primary omnibus association diagnostic because it matches Study 1's group-by-binary-outcome analysis. Group-rate vectors and pairwise order diagnostics provide the interpretable complement.

### Performance measures

The design separates:

- sampling error;
- observation-process error;
- total error;
- cross-definition contrasts;
- undefined-result frequency;
- Monte Carlo uncertainty.

## 3. Hostile statistical objections and dispositions

### Objection 1 — the simulation merely rediscovers level monotonicity

**Disposition:** level monotonicity is proved analytically and is not the simulation's target. The simulation addresses diagnostics that need not be monotone: association, subgroup order and observation-process error.

### Objection 2 — scenario probabilities are arbitrary

**Disposition:** they are controlled mechanisms, not fitted estimates. Each scenario isolates a specific structural possibility: null, aligned gradients, project-only gradients, compensating gradients, strict reversal or mixed order. The manuscript must not call their frequency realistic population prevalence.

### Objection 3 — Cramér's V differences are hard to interpret

**Disposition:** Cramér's V is the omnibus diagnostic, not a quality score. The frozen report must also show group-rate changes and pairwise order disagreement. A positive ΔV never means that the broader definition is better.

### Objection 4 — one random seed is insufficient

**Disposition:** the full run uses four streams spawned from one recorded SeedSequence root. Each stream must pass completeness checks before pooling.

### Objection 5 — 1,000 replications are conventional rather than justified

**Disposition:** the full design uses 4,000 replications per cell, selected from the worst-case MCSE target. Event estimates must report MCSE.

### Objection 6 — sparse tables create undefined results

**Disposition:** undefined results are counted and never silently deleted or imputed. A cell with more than 1% undefined primary results receives a warning. More than 5% undefined results bars a comparative claim for that diagnostic.

### Objection 7 — missingness and misclassification are oversimplified

**Disposition:** the primary design intentionally uses transparent nondifferential mechanisms. Group-differential observation error is reserved for a supplementary robustness module rather than multiplying the main factorial design. The article must state this boundary.

### Objection 8 — the simulation overstates generality because it uses nested definitions

**Disposition:** the primary simulation is aligned with the nested Study 1 contrast. Non-nested generality is established through exact set identities, counterexamples and tests. The paper must not claim that the primary simulation exhausts every definition relation.

### Objection 9 — simulation replications are treated as data for significance testing

**Disposition:** prohibited. No p-values or null-hypothesis tests across replications or cells will be used. The report presents performance summaries and Monte Carlo uncertainty.

### Objection 10 — post-result selection of visually attractive cells

**Disposition:** the reporting order and figure types are frozen before full execution. Every cell must be represented in the underlying tables or its failure documented.

## 4. Frozen precision decision

For an event probability estimate `p_hat` from `R` replications:

```text
MCSE(p_hat) = sqrt[p_hat(1 - p_hat) / R]
```

The worst case occurs at `p = 0.5`.

| Replications | Worst-case MCSE | Approximate 95% half-width |
|---:|---:|---:|
| 1,000 | 0.01581 | 0.03099 |
| 4,000 | 0.00791 | 0.01550 |
| 10,000 | 0.00500 | 0.00980 |

Four thousand replications strike a defensible balance between precision and a 432-cell design. This is not a materiality threshold for the scientific effect. It is a precision target for the Monte Carlo estimate.

## 5. Frozen design

```text
Scenarios:                         6
Per-group base sample sizes:       50, 100, 250, 500
Allocation profiles:               balanced, skewed
Misclassification profiles:        3
Missingness profiles:              3
Cells:                             432
Replications per cell:             4,000
Independent streams:               4
Replications per stream per cell:  1,000
Total replicate rows:              1,728,000
Root seed entropy:                 20260814
```

## 6. Seed and convergence contract

The full engine must use `numpy.random.SeedSequence` to spawn four independent streams from the recorded root entropy. The following checks are mandatory:

1. each stream contains every prespecified cell;
2. each stream contains exactly 1,000 replications per cell;
3. no stream has an invalid probability or incomplete output;
4. stream-specific event estimates and means are reported for convergence inspection;
5. pooled estimates are produced only after all streams pass;
6. the complete run records package versions, runner image and protocol SHA-256.

A single sequential generator with 4,000 draws per cell does not satisfy the freeze contract.

## 7. Undefined-result contract

For every primary metric and cell, the output must report:

- total replications;
- number defined;
- number undefined;
- undefined fraction;
- summary conditional on defined values.

Rules:

```text
undefined fraction <= 0.01: normal reporting
0.01 < undefined fraction <= 0.05: warning and sparse-cell discussion
undefined fraction > 0.05: no comparative claim for that metric in that cell
```

These are prespecified reporting gates, not significance thresholds.

## 8. Frozen reporting order

1. design validation and run completeness;
2. generating-population parameters;
3. levels and positive-class composition;
4. association contrasts;
5. subgroup-order disagreement;
6. sampling and observation-process error;
7. missingness and misclassification robustness;
8. undefined-result audit.

## 9. Frozen graphical plan

- design map of the factorial structure;
- heatmap of mean broad-minus-active Cramér's V by scenario and observation process;
- strict subgroup-order reversal probability with Monte Carlo uncertainty;
- sampling versus observation-process error decomposition;
- undefined-result frequency and sparse-cell warnings.

No figure may be selected solely because it displays the largest or most attractive difference.

## 10. Claims permitted after the full run

The full run may support statements of the form:

> Under the prespecified generating mechanism and observation process, the definitions produced different associations or subgroup orders in a stated proportion of replications, estimated with the reported Monte Carlo uncertainty.

It cannot support:

- a universal probability that outcome broadening changes conclusions;
- a population estimate for Romanian firms;
- a claim that one definition is inherently superior;
- a claim that ODSA improves managerial decision quality;
- a threshold that was chosen after inspecting the full results.

## 11. Execution gate

```text
Design hostile review:              PASS WITH BOUNDARIES
ADEMP structure:                    PASS
Replication precision:              FROZEN AT 4,000/CELL
Reporting order:                    FROZEN
Figure plan:                        FROZEN
Current engine stream compliance:   NOT YET VERIFIED
Full simulation execution:          NO-GO
Next phase:                         IM-R4 engine conformance and full run
```
