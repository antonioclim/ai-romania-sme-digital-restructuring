# Outcome-Definition Sensitivity Analysis: method specification

## 1. Scope

ODSA audits categorical outcomes for which more than one substantively
defensible mapping from observed states to a reported outcome exists. It is
intended for settings in which labels such as adoption, use, implementation or
engagement may include states with different evidential meanings.

ODSA is not a psychometric validation method, causal estimator, maturity model
or automatic selector of one correct definition. It makes the consequences
and inference boundaries of registered definitions inspectable.

## 2. Required inputs

A complete audit requires:

1. a finite observed state register;
2. a count for every registered state;
3. one or more named outcome definitions;
4. the intended question for each definition;
5. a common denominator or an explicit explanation of denominator changes;
6. an optional group-by-state table for association and order diagnostics;
7. optional claim wording and allowed-state sets.

Irrecoverable source coarsening must be recorded rather than silently
reconstructed.

## 3. Formal core

Let \(S=\{s_1,\ldots,s_K\}\) be mutually exclusive observed states and let a
definition be a non-empty subset \(d\subseteq S\). It induces

\[
Y_i(d)=\mathbb{1}(s_i\in d).
\]

ODSA keeps five dimensions separate:

- **level**: \(L(d)\);
- **composition**: \(C_s(d)\);
- **association**: \(A(d;X)\);
- **subgroup order**: pairwise ordering of \(R_g(d)\);
- **claim admissibility**: \(\Gamma(q,d)\).

The proofs and counterexamples are given in
`FORMAL_PROPERTIES_AND_PROOFS.md`.

## 4. Definition relations and level decomposition

Pairs are classified as equal, strict subset, strict superset, disjoint or
partially overlapping.

For any pair under a common denominator,

\[
L(d_b)-L(d_a)
=
P(d_b\setminus d_a)-P(d_a\setminus d_b).
\]

This identity prevents a non-nested contrast from being reported as if it only
added states.

## 5. Composition

Positive-class composition reports which states constitute each positive
outcome. ODSA may also report total variation distance between two composition
vectors. This is descriptive and must not be interpreted as a validity score.

## 6. Association and subgroup order

The current implementation reports Pearson's chi-square and bias-unadjusted
Cramér's \(V\) for a categorical descriptor. The same diagnostic must be used
across definitions.

Association is not monotone under broadening. Subgroup order is also not
invariant. Pairwise-order diagnostics separate strict reversals from tie
changes and avoid forcing ties through lexical ordering.

## 7. Claim admissibility

A claim \(q\) registers the set \(S_q\) of observed states compatible with its
wording. The conservative rule is

\[
\Gamma(q,d)=1 \iff d\subseteq S_q.
\]

A passing result is necessary but not sufficient for construct validity. A
failure identifies the positive states that make the wording too narrow.

## 8. Six-step protocol

1. register observed states and lost distinctions;
2. register definitions, denominators and intended questions;
3. compare levels and decompose level contrasts;
4. decompose positive classes;
5. compare association and subgroup order using common diagnostics;
6. audit claims and state the inference boundary.

## 9. Simulation role

The candidate factorial simulation separates generating population
parameters, sampled true values and observed values after missingness and
misclassification. CI mode is a mechanics test only. Full simulation results
must not enter the manuscript before the design is frozen and executed.

## 10. Boundary conditions

ODSA cannot:

- recover states erased by coarsening;
- repair selection bias or possible duplicate units;
- establish a sampling frame;
- prove causal effects;
- replace longitudinal or multi-informant evidence;
- validate readiness, capability or maturity scales;
- justify one scalar sensitivity score.

ODSA adds little when alternatives contain the same states, answer the same
question and produce decision-irrelevant diagnostic differences.

## 11. RC status

Version `3.0.0-rc1` now contains the formal-property tests and a candidate
factorial protocol. Independent replication, full simulation execution and
journal-facing manuscript integration remain open.
