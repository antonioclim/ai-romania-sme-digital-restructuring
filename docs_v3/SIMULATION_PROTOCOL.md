# ODSA simulation-study protocol

## 1. Purpose

The simulation study evaluates properties of Outcome-Definition Sensitivity Analysis that cannot be established from the Romanian application alone. It is designed to distinguish mathematical invariants from contingent empirical behaviour and to identify conditions under which outcome broadening changes levels, associations, group rankings and recoverable claims.

The simulation is not used to manufacture support for ODSA. Its role is to expose both the method's value and its boundary conditions.

## 2. Research questions

### RQ-S1 — Level sensitivity

How much does the reported level change as positive-state sets are broadened, and does the implementation preserve the common-denominator monotonicity invariant?

### RQ-S2 — Association sensitivity

Under what state distributions does broadening strengthen, weaken or leave unchanged the association between the outcome and an organisational grouping variable?

### RQ-S3 — Ranking sensitivity

How often do defensible alternative definitions imply different group orderings?

### RQ-S4 — Measurement error

How do adjacent-state misclassification and source-item coarsening affect definition-specific levels, associations and rankings?

### RQ-S5 — Denominator drift

How often can definition-dependent analytic availability produce an apparent violation of level monotonicity when the underlying positive-state sets are nested?

### RQ-S6 — Recoverability

Which definitions remain identifiable when implementation, testing and planning are collapsed into one project-stage category?

## 3. Latent state space

The manuscript-grade design uses five mutually exclusive latent states:

1. `active_use` — current operational use;
2. `deployed` — deployed but not established as active routine use;
3. `testing` — testing or pilot activity;
4. `planning` — planning, budgeting or preparation;
5. `no_engagement` — none of the preceding states.

The states are ordered for the purpose of adjacent-stage misclassification, but ODSA does not treat them as a validated scalar maturity scale.

## 4. Registered definitions

| Definition | Positive latent states | Intended question |
|---|---|---|
| `active_use` | active use | Is the technology currently used operationally? |
| `implemented` | active use, deployed | Has implementation reached deployment or use? |
| `tested_or_beyond` | active use, deployed, testing | Has activity reached testing or a later state? |
| `broad_engagement` | active use, deployed, testing, planning | Is there any current organisational engagement? |
| `experimental_activity` | active use, testing | Is there active or experimental activity? |

The final definition is deliberately non-nested relative to `implemented`. It tests whether the software and reporting language correctly distinguish partial overlap from broadening.

## 5. Organisational groups

Three generic groups are simulated. They are labels rather than claims about real firm sizes or sectors:

- Group A;
- Group B;
- Group C.

The group variable supplies the categorical descriptor for Cramér's V and rate-ranking diagnostics.

## 6. Factorial design

The full design crosses the following factors.

| Factor | Levels |
|---|---|
| Nominal sample size per group | 60, 180, 600 |
| Active-use gradient | flat, ascending, descending |
| Added-state gradient | flat, ascending, descending, middle-concentrated |
| Group-size balance | balanced, imbalanced |
| Adjacent-state misclassification rate | 0, 0.05, 0.15 |
| Coarsening | none, project stages collapsed |
| Denominator regime | common, definition-dependent |

The complete factorial contains 864 design cells. The default manuscript run uses 500 replications per cell and a fixed seed. The release-candidate continuous-integration run uses fewer replications per cell but traverses the complete design.

## 7. Probability-generating process

The baseline latent distribution is:

| State | Probability |
|---|---:|
| Active use | 0.12 |
| Deployed | 0.08 |
| Testing | 0.10 |
| Planning | 0.15 |
| No engagement | 0.55 |

The active-use gradient shifts probability between `active_use` and `no_engagement`. The added-state gradient shifts probability between the combined deployed/testing/planning mass and `no_engagement`. Added-state shifts are distributed across deployment, testing and planning using fixed documented weights.

This construction allows active-use and project-stage gradients to align, oppose one another, remain flat or concentrate in the middle group. It therefore creates conditions in which broadening can strengthen, weaken or reverse descriptive patterns.

## 8. Group-size balance

Under the balanced regime, all three groups use the nominal sample size. Under the imbalanced regime, group sizes are approximately:

\[
0.5n,\quad n,\quad 2n.
\]

This factor tests whether unequal precision and group contribution alter the frequency of apparent sensitivity.

## 9. Misclassification

Misclassification is adjacent in the registered state order. With probability \(1-m\), an observation remains in its latent state. With probability \(m\), it moves to an adjacent state; internal states split the error probability equally between their two neighbours.

The rates 0, 0.05 and 0.15 represent no error, modest error and an intentionally adverse stress condition. They are not estimates of error in the Romanian survey.

## 10. Coarsening

Under `project_collapsed`, `deployed`, `testing` and `planning` are mapped to one observed category, `project_stage`.

The simulation reports whether each fine-state definition is identifiable under this map. The expected result follows the fibre criterion:

- active use remains identifiable;
- broad engagement remains identifiable;
- implemented, tested-or-beyond and experimental activity do not remain identifiable.

Coarsening is treated as an information-loss mechanism, not as random measurement error.

## 11. Denominator regimes

### Common denominator

All registered definitions are evaluated on the same observed counts. Nested level monotonicity must hold in every replication.

### Definition-dependent analytic availability

The narrow and broad outcomes are evaluated on deliberately different retained subsets generated by documented state-dependent retention probabilities. This is an adversarial stress test of denominator drift. It demonstrates that apparent monotonicity violations can arise from changing analysis sets even though the underlying definitions remain nested.

These retention probabilities are simulation parameters, not claims about the empirical survey.

## 12. Replication-level outcomes

Each replication records:

- latent, observed and reported levels for active use and broad engagement;
- level bias induced by measurement error;
- latent, observed and reported Cramér's V;
- the difference in Cramér's V between broad and narrow definitions;
- latent, observed and reported rank-reversal indicators;
- disagreement between latent and observed rank-reversal status;
- common-denominator monotonicity violations;
- apparent monotonicity violations under definition-dependent denominators;
- the number and identity of definitions identifiable after coarsening.

## 13. Cell-level summaries

For each design cell, the workflow reports:

- mean levels and biases;
- mean, median and 5th/95th percentiles of the association difference;
- share of replications in which broad association is stronger;
- share in which broad association is weaker;
- share with a group-rank reversal;
- share with measurement-induced rank-reversal disagreement;
- share with an apparent denominator-driven monotonicity violation;
- common-denominator invariant violations;
- mean number of identifiable definitions.

## 14. Global gates

A simulation run passes the implementation gate only if:

1. common-denominator monotonicity violations equal zero;
2. at least one design condition produces a stronger broad association;
3. at least one condition produces a weaker broad association;
4. at least one rank reversal occurs;
5. the definition-dependent regime produces at least one apparent monotonicity violation;
6. coarsening reduces the number of identifiable fine-state definitions as predicted;
7. identical seeds and configurations produce identical outputs.

The first condition is an invariant. Conditions 2–6 confirm that the design traversed the intended stress cases rather than proving a universal empirical frequency.

## 15. Analysis and reporting principles

The simulation will not be reported as evidence that one definition is generally superior. Results will be stratified by design factors and interpreted as boundary-condition evidence.

The article will distinguish:

- deterministic mathematical results;
- Monte Carlo frequencies conditional on the specified generating process;
- empirical findings from Study 1;
- findings from an independent Study 2.

No simulation frequency will be described as a real-world prevalence estimate.

## 16. Reproducibility

The design is stored in `simulations/design.yml`. The executable study is `simulations/run_simulation_study.py`. Outputs include the enumerated design cells, replication-level metrics, cell summaries and a machine-readable gate report. Seeds, dependency versions and command-line parameters are recorded in every run summary.
