# ODSA formal properties and proof sketches

## Status and evidential scope

This document fixes the mathematical core of the `3.0.0-rc1` development
branch. Outcome-Definition Sensitivity Analysis (ODSA) is not presented as a
new estimator, psychometric model, causal method or method for selecting one
universally correct outcome. Its role is narrower: it makes the consequences
and inference boundaries of alternative categorical outcome maps explicit,
separable and executable.

The results below require a finite observed state register. Results involving
level contrasts also require a common analytical denominator. None of the
properties repairs selection bias, ambiguous source categories, measurement
error, unobserved clustering or a weak research design.

## 1. Notation

Let

\[
S=\{s_1,\ldots,s_K\}
\]

be a finite set of mutually exclusive observed states. Observation \(i\)
occupies one state \(s_i\in S\). An outcome definition is a non-empty subset
\(d\subseteq S\), inducing

\[
Y_i(d)=\mathbb{1}(s_i\in d).
\]

For a fixed set of \(n\) retained observations, define

\[
L(d)=\frac{1}{n}\sum_{i=1}^{n}Y_i(d).
\]

For state \(s\in d\), positive-class composition is

\[
C_s(d)=\frac{n_s}{\sum_{u\in d}n_u},
\]

provided that the positive total is non-zero.

For a prespecified descriptor \(X\),

\[
A(d;X)=\mathcal{A}(Y(d),X),
\]

where \(\mathcal{A}\) is an explicitly selected association diagnostic. The
current implementation uses Pearson's chi-square and bias-unadjusted Cramér's
\(V\) for a categorical descriptor.

A claim \(q\) has an allowed-state set \(S_q\subseteq S\). Conservative
semantic admissibility is

\[
\Gamma(q,d)=1 \iff d\subseteq S_q.
\]

This condition certifies only that no registered positive state contradicts
the wording. It does not establish construct validity, causal identification,
truth or external generalisability.

## 2. P1 — nested-level monotonicity

**Statement.** If \(d_a\subseteq d_b\) and the denominator is fixed, then

\[
L(d_a)\leq L(d_b).
\]

**Proof.** For every observation,

\[
\mathbb{1}(s_i\in d_a)\leq\mathbb{1}(s_i\in d_b).
\]

Summing over \(i\) and dividing by the positive constant \(n\) preserves the
inequality. \(\square\)

**Boundary.** This is an arithmetic consequence of nesting. It is not evidence
that \(d_a\) and \(d_b\) measure the same construct or support the same claim.

## 3. P2 — exact symmetric-difference decomposition

**Statement.** For any two definitions \(d_a,d_b\subseteq S\) under a common
denominator,

\[
L(d_b)-L(d_a)
=
P(d_b\setminus d_a)-P(d_a\setminus d_b).
\]

**Proof.** Decompose both sets into their shared part and their disjoint
remainders:

\[
d_a=(d_a\cap d_b)\cup(d_a\setminus d_b),
\]

\[
d_b=(d_a\cap d_b)\cup(d_b\setminus d_a).
\]

The shared mass cancels in the difference. \(\square\)

**Consequence.** For nested definitions \(d_a\subseteq d_b\), the second term
is zero and the increase in level is exactly the mass of the states added by
\(d_b\). For non-nested definitions, a signed difference without this
decomposition can conceal simultaneous additions and removals.

## 4. P3 — association is not monotone under broadening

**Statement.** Even when \(d_a\subset d_b\), neither

\[
A(d_a;X)\leq A(d_b;X)
\]

nor the reverse inequality is guaranteed.

**Constructive counterexamples.** Consider two equally sized groups with
states `active`, `project` and `other`. Let \(d_a=\{\text{active}\}\) and
\(d_b=\{\text{active},\text{project}\}\).

First:

| Group | active | project | other |
|---|---:|---:|---:|
| G1 | 10 | 0 | 90 |
| G2 | 10 | 80 | 10 |

Active use has \(V=0\), while broad engagement has \(V=0.8\).

Second:

| Group | active | project | other |
|---|---:|---:|---:|
| G1 | 90 | 0 | 10 |
| G2 | 10 | 80 | 10 |

Active use has \(V=0.8\), while broad engagement has \(V=0\).

**Consequence.** Broadening may strengthen, weaken or leave unchanged a
prespecified association. A larger \(V\) is not evidence that a definition is
more valid.

## 5. P4 — subgroup order is not invariant

**Statement.** Nested definitions do not guarantee the same subgroup ordering.

**Reason.** For groups \(g\) and \(h\),

\[
R_g(d_b)-R_h(d_b)
=
[R_g(d_a)-R_h(d_a)]
+
[R_g(d_b\setminus d_a)-R_h(d_b\setminus d_a)].
\]

The added-state contrast can reinforce, cancel or reverse the original
contrast.

**Reporting implication.** ODSA distinguishes strict reversals from tie
changes. It reports pairwise disagreement rather than forcing a complete order
through arbitrary lexical tie-breaking.

## 6. P5 — coarsening is not invertible without additional information

**Statement.** If an observed category merges two or more underlying states,
the constituent counts cannot in general be recovered from the coarsened count
alone.

**Proof sketch.** Suppose the source instrument records one project category
with total \(m\), but the intended fine states are planning, testing and
deployment. Every non-negative integer triple \((a,b,c)\) satisfying

\[
a+b+c=m
\]

maps to the same observed count. Because several fine-state vectors have the
same image, the mapping is many-to-one and has no unique inverse. \(\square\)

**Consequence.** ODSA can expose the inferential cost of coarsening but cannot
reconstruct distinctions that the instrument did not preserve.

## 7. P6 — claim admissibility is downward closed

**Statement.** If \(\Gamma(q,d)=1\) and \(d'\subseteq d\), then
\(\Gamma(q,d')=1\).

**Proof.** \(\Gamma(q,d)=1\) implies \(d\subseteq S_q\). By transitivity,
\(d'\subseteq d\subseteq S_q\), hence \(\Gamma(q,d')=1\). \(\square\)

**Asymmetry.** The converse does not hold. A narrow definition may support a
claim while a broader definition fails because it admits an incompatible
state.

## 8. P7 — equal maps are diagnostically equivalent

**Statement.** If \(d_a=d_b\), then under the same retained observations,
descriptor and diagnostic implementation, their levels, compositions,
associations and subgroup rates are identical.

**Consequence.** Merely renaming an unchanged state map creates no ODSA
sensitivity. Any semantic difference between labels remains a reporting issue,
not a numerical one.

## 9. P8 — total variation is descriptive, not a validity score

For two non-empty positive classes, define their full-state composition
vectors \(C(d_a)\) and \(C(d_b)\). The implementation reports

\[
TV(d_a,d_b)
=
\frac{1}{2}\sum_{s\in S}|C_s(d_a)-C_s(d_b)|.
\]

The value is symmetric and lies in \([0,1]\). It describes how different the
positive classes are internally. It does not rank definitions by validity and
no universal materiality threshold is asserted.

For the Romanian aggregate example, comparing active use with broad engagement
gives

\[
TV=\frac{51}{105}=0.4857,
\]

because project-stage responses make up 51 of the 105 broad positives. This
identity is descriptive and response-set specific.

## 10. P9 — the current claim audit is necessary but not sufficient

The rule \(d\subseteq S_q\) blocks visible semantic narrowing. It remains only
a necessary compatibility condition. A passing pair can still fail because of
poor item wording, invalid construct representation, response error,
selection bias or unsupported external inference.

The implementation therefore uses the word `admissible`, not `valid`, and
returns the incompatible states when a pair fails.

## 11. Observation-process invariance inside one positive set

If a misclassification mechanism only swaps states within a definition's
positive set, the definition's positive count is preserved exactly after
retention. For example, swapping `active_use` and `project_stage` does not
change `broad_engagement = {active_use, project_stage}`. It can still bias the
two narrow outcomes and their compositions.

This property depends on the registered set boundary. Swapping
`project_stage` and `other` crosses the broad boundary and can bias the broad
outcome.

## 12. Stopping rule, not theorem

ODSA adds little when registered alternatives:

- contain the same states;
- answer the same question;
- produce materially indistinguishable diagnostics for the intended use;
- support the same claims.

“Materially” must be defined from the decision context or prespecified
statistical criterion. ODSA supplies no universal threshold and no scalar
score.

## 13. Executable mapping

| Formal object | Implementation |
|---|---|
| \(S\) | `StateSpace` |
| \(d\) | `OutcomeDefinition` |
| set relation | `definition_relation` |
| symmetric difference | `definition_difference` |
| exact level decomposition | `definition_level_contrast` |
| \(L(d)\) | `definition_level` |
| \(C_s(d)\) | `definition_composition` and `composition_vector` |
| composition distance | `composition_total_variation` |
| \(A(d;X)\) | `association_diagnostics` |
| \(\Delta V\) | `association_contrast` |
| subgroup rates | `group_rate_diagnostics` |
| order sensitivity | `pairwise_order_disagreement` |
| \(\Gamma(q,d)\) | `audit_claims` |

## 14. Assertions prohibited by this formal core

The propositions do not support claims that:

- ODSA identifies the correct outcome;
- broad outcomes are intrinsically invalid;
- a larger association is better;
- the claim audit establishes construct validity;
- the Romanian example validates a universal method;
- simulation alone establishes managerial benefit;
- a scalar ODSA score is justified.
