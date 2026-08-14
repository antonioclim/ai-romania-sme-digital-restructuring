# Outcome-Definition Sensitivity Analysis: method specification

## 1. Scope

Outcome-Definition Sensitivity Analysis (ODSA) is a non-scalar audit for categorical outcomes. It examines how defensible alternative definitions alter:

1. the reported outcome level;
2. the internal composition of the positive class;
3. association with a declared descriptor;
4. group-rate ordering;
5. the claims the measure can support;
6. the definitions that remain recoverable after state coarsening.

ODSA does not select one universally correct definition and does not replace construct validation, reliability assessment, measurement invariance, causal identification or substantive theory.

## 2. Required inputs

### 2.1 State space

A finite set of mutually exclusive recorded states

\[
S=\{s_1,\ldots,s_K\}.
\]

The state register must preserve the original wording or provide an auditable harmonisation.

### 2.2 Definition register

Each definition \(d_j\subseteq S\) includes:

- a unique name;
- its positive states;
- a human-readable label;
- the research question it answers;
- the claims it may support;
- its relation to every other definition.

### 2.3 Locked analytical denominator

All primary definition comparisons use the same analytical cases. Alternative sample restrictions or missing-data rules are separate sensitivity layers.

### 2.4 Optional descriptor

A categorical descriptor \(X\) enables association, group-rate and ranking diagnostics.

### 2.5 Optional claim register

Each claim \(q\) declares an evidential support set \(E_q\). The current admissibility rule is:

\[
\Gamma(q,d)=\mathbb{1}\{d\subseteq E_q\}.
\]

### 2.6 Optional coarsening register

A map \(g:S\rightarrow T\) records how fine states were collapsed into reported states.

## 3. Core diagnostics

### 3.1 Definition relation

For each pair, ODSA reports equal, strict subset, strict superset, disjoint or overlap. A definition is called broader only under a superset relation.

### 3.2 Level

\[
L_n(d)=\frac{1}{n}\sum_{i=1}^{n}\mathbb{1}\{Z_i\in d\}.
\]

For nested definitions, level monotonicity is guaranteed when the denominator is locked.

### 3.3 Composition

For \(s\in d\):

\[
C_{n,s}(d)=
\frac{\sum_i\mathbb{1}\{Z_i=s\}}
{\sum_i\mathbb{1}\{Z_i\in d\}}.
\]

Composition identifies which states contribute to a broader headline.

### 3.4 Association

For categorical descriptors, the reference implementation reports Pearson's chi-square and bias-unadjusted Cramér's \(V\). The method does not assume that association is monotone under definition nesting.

### 3.5 Group-rate and ranking sensitivity

ODSA reports definition-specific group rates, deterministic rank signatures, rank-reversal indicators and a normalised Kendall inversion distance.

### 3.6 Claim admissibility

A positive class may support claim \(q\) only if every state coded positive is within \(E_q\). This is a semantic audit and depends on a defensible claim register.

### 3.7 Recoverability

A fine-state definition is recoverable after coarsening only when membership is constant within every fibre of the coarsening map. Non-recoverable definitions are reported, not silently imputed.

### 3.8 Misclassification

With true state-probability vector \(p\) and row-stochastic transition matrix \(M\), expected recorded probabilities are \(pM\). ODSA separates this measurement process from deliberate outcome broadening.

## 4. Minimum workflow

1. Freeze the analytical sample and denominator.
2. Register observed states without conflating them with claims.
3. Register all substantively defensible definitions before inspecting their results.
4. Record pairwise definition relations.
5. Compute definition-specific levels and uncertainty intervals.
6. Decompose every multi-state positive class.
7. Compute descriptor associations and group rates.
8. Audit rankings and signed group contrasts.
9. Audit claims against positive-state membership.
10. Audit definition recoverability under any coarsening.
11. Report results that remain stable and results that change.
12. State what ODSA cannot recover or establish.

## 5. Interpretation rules

### 5.1 Broader does not mean less valid

A broad definition may be appropriate for a broad question, such as any organisational engagement. The problem arises when it is interpreted as evidence of a narrower state such as active operational use.

### 5.2 Stability is not validity

A result that is stable across definitions may still rest on an invalid state measure. A result that changes may reveal a genuine difference in the phenomenon represented.

### 5.3 Statistical significance is secondary

ODSA focuses on the definition-specific estimand, magnitude, composition, ranking and claim boundary. It does not use p-value changes as the sole criterion of sensitivity.

### 5.4 Non-recoverability is a result

When coarsening prevents an exact definition from being reconstructed, the correct output is an explicit recoverability failure.

## 6. Formal properties

The method relies on the following proved or counterexample-supported properties:

1. nested definitions guarantee level monotonicity;
2. level differences equal the mass of added states;
3. broad composition explains the narrow-to-broad level ratio;
4. association is not monotone under nesting;
5. group rankings can reverse;
6. claim admissibility is a subset condition;
7. recoverability is equivalent to membership constancy within coarsening fibres;
8. misclassification changes levels through net flows across a definition boundary;
9. overlapping definitions require pairwise difference-set interpretation;
10. denominator locking is required to attribute sensitivity to definition choice.

Complete statements and proofs are in `docs_v3/FORMAL_PROPOSITIONS.md`.

## 7. Output contract

A complete ODSA implementation should produce:

```text
definition_levels.csv
definition_composition.csv
definition_relations.csv
claim_admissibility.csv
group_rates.csv
association_diagnostics.csv
ranking_sensitivity.csv
recoverability_audit.csv
odsa_run_summary.json
```

Files that are not applicable may be omitted only when the run summary states why.

## 8. Failure conditions

An ODSA run must fail or return an explicit non-estimable status when:

- the state register is incomplete;
- state counts are negative;
- definitions contain unknown states;
- the primary denominator changes across definitions;
- a group has no observations;
- a contingency table has an empty margin;
- a coarsening map omits or adds fine states;
- a non-recoverable definition is requested as if it were exact;
- output provenance or version metadata are missing.

## 9. Boundary conditions

ODSA adds little when:

- only one substantively defensible definition exists;
- candidate definitions are semantically equivalent;
- all diagnostics are stable and claims remain admissible;
- the outcome is intrinsically continuous and categorisation is unnecessary;
- the focal construct is latent and cannot be represented as declared observable states.

Additional caution is required for non-exclusive states, repeated observations, hierarchical outcomes, survey weights, severe missingness, very sparse groups and definitions chosen after results are known.

## 10. Relationship to the simulation and empirical studies

The formal propositions specify what must or need not occur. The simulation estimates how frequently different forms of sensitivity occur under controlled conditions. Study 1 provides an aggregate-only empirical application and Study 2 will provide an independently selected replication.

The three evidence types are reported separately.
