# Formal properties of Outcome-Definition Sensitivity Analysis

## 1. Purpose and assumptions

This document separates mathematical properties of ODSA from reporting conventions and empirical choices. The statements below concern a finite register of mutually exclusive observed states and deterministic mappings from those states to binary outcome definitions.

Let

\[
S=\{s_1,\ldots,s_K\}
\]

be the observed state space. For observation \(i\), let \(s_i\in S\). An outcome definition \(d\) is a non-empty subset of \(S\), inducing

\[
Y_i(d)=\mathbb{1}(s_i\in d).
\]

Unless stated otherwise, comparisons use the same observations and the same denominator. ODSA does not assume that the states form a validated maturity scale, that transitions are monotone or that a broader definition is substantively preferable.

## 2. Proposition 1: level monotonicity under nesting

**Statement.** If \(d_a\subseteq d_b\) and both definitions are evaluated on the same observations, then

\[
L(d_a)\leq L(d_b).
\]

**Proof.** For every observation,

\[
\mathbb{1}(s_i\in d_a)\leq\mathbb{1}(s_i\in d_b)
\]

because membership in \(d_a\) implies membership in \(d_b\). Summing over observations and dividing by the common positive denominator preserves the inequality. □

This is an arithmetic property. It does not imply that the two definitions have the same meaning or support the same claim.

## 3. Corollary 1: exact level increment

For \(d_a\subseteq d_b\),

\[
L(d_b)-L(d_a)=\frac{1}{n}\sum_{i=1}^{n}
\mathbb{1}(s_i\in d_b\setminus d_a).
\]

The increase is exactly the observed mass of the added states. It is therefore not a free-standing discovery. The substantive questions are what those added states mean, how they are distributed and what claims remain admissible after their inclusion.

## 4. Proposition 2: composition identity

For any definition \(d\) with at least one positive observation,

\[
\sum_{s\in d} C_s(d)=1.
\]

**Proof.** The numerators partition the positive observations by mutually exclusive state. Their sum equals the positive-class denominator. □

Composition is thus a decomposition, not an additional estimand. Its role is to prevent substantively different positive states from disappearing behind one headline percentage.

## 5. Proposition 3: no general association monotonicity

**Statement.** Even when \(d_a\subset d_b\), no general ordering exists between

\[
A(d_a;X)
\quad\text{and}\quad
A(d_b;X).
\]

The association may strengthen, weaken or remain unchanged.

### Constructive case in which broadening strengthens association

Consider two groups of 100 observations each with states `active`, `project` and `other`:

| Group | Active | Project | Other |
|---|---:|---:|---:|
| A | 10 | 0 | 90 |
| B | 10 | 40 | 50 |

For \(d_a=\{active\}\), both groups have a 10% rate, so the group association is zero. For \(d_b=\{active,project\}\), the rates are 10% and 50%, so the association is positive.

### Constructive case in which broadening weakens association

| Group | Active | Project | Other |
|---|---:|---:|---:|
| A | 50 | 0 | 50 |
| B | 10 | 40 | 50 |

The narrow rates are 50% and 10%, whereas the broad rates are both 50%. Broadening therefore removes the association.

These counterexamples prove that association monotonicity cannot be inferred from level monotonicity.

## 6. Proposition 4: rank order is not invariant

Let

\[
R_g(d)=P(Y(d)=1\mid G=g).
\]

For nested definitions, group ordering can reverse. For example:

| Group | Active | Project | Other |
|---|---:|---:|---:|
| A | 30 | 0 | 70 |
| B | 10 | 40 | 50 |

Under \(d_a=\{active\}\), Group A ranks above Group B. Under \(d_b=\{active,project\}\), Group B ranks above Group A.

For \(d_a\subset d_b\), define the added-state rate

\[
Q_g=P(s\in d_b\setminus d_a\mid G=g).
\]

Then

\[
R_g(d_b)=R_g(d_a)+Q_g.
\]

A sufficient condition for preservation of all strict rankings is that \(Q_g\) is constant across groups. This condition is not necessary. In general, rankings are preserved only when the added-state differences are too small to overturn the pairwise margins under the narrow definition.

## 7. Proposition 5: downward closure of claim admissibility

Let a claim \(q\) register the set \(E(q)\subseteq S\) of positive states compatible with its wording. Under the conservative rule

\[
\Gamma(q,d)=1 \quad\text{only if}\quad d\subseteq E(q),
\]

claim admissibility is downward closed.

**Statement.** If \(d_a\subseteq d_b\) and \(\Gamma(q,d_b)=1\), then \(\Gamma(q,d_a)=1\).

**Proof.** \(d_b\subseteq E(q)\) and \(d_a\subseteq d_b\) imply \(d_a\subseteq E(q)\). □

The converse does not hold. A narrow definition may support a claim that a broader definition cannot support.

## 8. Proposition 6: no general level ordering for non-nested definitions

If neither \(d_a\subseteq d_b\) nor \(d_b\subseteq d_a\), set inclusion provides no level ordering. Either definition can have the higher level, depending on the observed mass assigned to their non-overlapping states.

Non-nested definitions must therefore be compared directly. They must not be described as progressively broader unless an explicit partial order justifies that language.

## 9. Proposition 7: denominator comparability is necessary

The monotonicity result in Proposition 1 requires a common analysis set. If definition-specific missingness, exclusions or filters create different denominators, observed proportions can violate the expected ordering even when the positive-state sets are nested.

For example, a narrow estimate of 9/10 equals 90%, whereas a broader estimate of 50/100 equals 50%. This apparent reversal does not refute set-theoretic monotonicity. It shows that the two estimands were evaluated on different observation sets.

ODSA therefore treats denominator locking as a precondition for direct level comparison. When denominators differ, the report must distinguish semantic sensitivity from analytic-sample sensitivity.

## 10. Proposition 8: identifiability under coarsening

Let

\[
h:S\rightarrow O
\]

be a many-to-one mapping from fine states to observed coarse categories. The fibre of observed category \(o\) is

\[
h^{-1}(o)=\{s\in S:h(s)=o\}.
\]

**Statement.** A fine-state definition \(d\subseteq S\) is identifiable from the coarsened categories if and only if \(d\) is a union of complete fibres of \(h\).

**Proof.** If \(d\) is a union of complete fibres, membership in \(d\) can be determined from the observed category. Conversely, if any fibre contains both a state in \(d\) and a state outside \(d\), observations in that coarse category cannot be classified without additional information. □

This establishes a precise information-loss boundary. No statistical model can recover a split fibre from the coarsened counts alone without additional assumptions or data.

### Example

Suppose `deployment`, `testing` and `planning` are collapsed into `project_stage`.

- `active_use = {active}` remains identifiable.
- `broad_engagement = {active, deployment, testing, planning}` remains identifiable.
- `implemented = {active, deployment}` is not identifiable because the `project_stage` fibre is split.
- `tested_or_beyond = {active, deployment, testing}` is not identifiable for the same reason.

## 11. Proposition 9: claim admissibility is not construct validity

The condition \(d\subseteq E(q)\) is a conservative compatibility test. It can identify visibly incompatible positive states, but it cannot establish that:

- the source item validly measures the construct;
- the registered states are exhaustive;
- respondents interpreted the categories consistently;
- the data identify causal or population quantities;
- an apparently compatible label is free from measurement error.

Passing the claim-admissibility gate is therefore necessary under the registered semantics, not sufficient for construct validity.

## 12. Reporting implications

A defensible ODSA report should distinguish four classes of result:

1. **mathematical invariants**, such as level monotonicity under common denominators;
2. **empirical diagnostics**, such as definition-specific Cramér's V values;
3. **information-loss findings**, such as non-identifiability after coarsening;
4. **interpretive judgements**, such as the wording of a claim register.

Conflating these classes would overstate the method. The simulation study is designed to stress-test the empirical diagnostics while preserving the formal invariants above.
