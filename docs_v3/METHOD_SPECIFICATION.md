# Outcome-Definition Sensitivity Analysis: method specification

## 1. Scope

ODSA audits categorical outcomes for which more than one defensible mapping from observed states to a reported outcome exists. It is intended for settings in which the same label, such as adoption, use, implementation or engagement, may include states with different evidential meanings.

ODSA is not a psychometric validation method, causal estimator or maturity model. It does not identify the universally correct definition. It makes the consequences and inference boundaries of registered definitions inspectable.

## 2. State space

Let

\[
S=\{s_1,\ldots,s_K\}
\]

be a finite register of mutually exclusive observed states. If a source item has already combined substantively different states, that coarsening is recorded as an information-loss boundary.

For observation `i`, the observed state is `s_i ∈ S`.

## 3. Outcome definition

An outcome definition is a non-empty subset

\[
d_j\subseteq S.
\]

It induces the binary indicator

\[
Y_i(d_j)=\mathbb{1}(s_i\in d_j).
\]

Every definition is registered before interpretation with a name, positive-state set, denominator and intended question.

## 4. Diagnostics

### 4.1 Level

\[
L(d_j)=\frac{1}{n}\sum_{i=1}^{n}Y_i(d_j).
\]

For fixed denominators and nested definitions `d_a ⊂ d_b`, level monotonicity follows:

\[
L(d_a)\leq L(d_b).
\]

This arithmetic property does not imply that the definitions support the same claim.

### 4.2 Composition

For `s ∈ d_j`, the positive-class composition is

\[
C_s(d_j)=\frac{\sum_i\mathbb{1}(s_i=s)}{\sum_iY_i(d_j)}.
\]

Composition identifies what entered a broader outcome and prevents the added states from disappearing behind one headline percentage.

### 4.3 Association

For an organisational descriptor `X`, ODSA computes a common association diagnostic

\[
A(d_j;X)=\mathcal{A}(Y(d_j),X).
\]

The current implementation reports Pearson chi-square and Cramér's V for categorical descriptors. Association is not monotone under outcome broadening: newly admitted states may be distributed differently across groups.

### 4.4 Group-rate ranking

For group `g`,

\[
R_g(d_j)=P(Y(d_j)=1\mid G=g).
\]

ODSA compares the order induced by `R_g(d_j)` across definitions. A rank reversal occurs when two definitions imply different group orderings. Rankings remain descriptive unless the design supports population or causal inference.

### 4.5 Claim admissibility

A claim `q` registers the set `E(q) ⊆ S` of states compatible with its wording. The conservative admissibility rule is

\[
\Gamma(q,d_j)=1 \quad\text{only if}\quad d_j\subseteq E(q).
\]

This rule blocks silent interpretive narrowing. It does not certify that the instrument validly measures the claim; it establishes only that no visibly incompatible positive state has been included.

## 5. Definition relations

The implementation classifies pairs of positive-state sets as:

- equal;
- strict subset;
- strict superset;
- disjoint;
- partially overlapping.

Level monotonicity is guaranteed only for nested definitions with a common denominator. Non-nested definitions require direct empirical comparison.

## 6. Six-step audit

1. register the observed state space and lost distinctions;
2. register outcome definitions, denominators and intended questions;
3. compare definition-specific levels;
4. decompose broader positive classes;
5. compare associations, group rates and rankings under the same diagnostics;
6. audit claim admissibility and state the inference boundary.

## 7. Boundary conditions

ODSA adds little when alternative definitions are semantically equivalent and yield materially similar diagnostics. It is inappropriate when the underlying outcome is necessarily continuous and no defensible categorical state register exists. It cannot recover distinctions already lost through coarsening, repair selection bias, establish unique organisational units or substitute for longitudinal and multi-informant evidence.

## 8. RC status

Version `3.0.0-rc1` implements the formal core and a deterministic smoke simulation. The simulation design, independent replication and manuscript-facing reporting standard remain under methodological consolidation before the final `3.0.0` release.
