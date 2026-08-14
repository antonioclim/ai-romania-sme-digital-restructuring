# Formal propositions and counterexamples for ODSA

## 1. Purpose and status

This document states the mathematical properties claimed for Outcome-Definition Sensitivity Analysis (ODSA). The propositions concern observable categorical states, deterministic outcome definitions and diagnostics computed on a locked analytical sample. They do not establish construct validity by themselves and they do not select a universally correct operationalisation.

The distinction between a theorem, a reporting convention and an empirical regularity is maintained throughout:

- a **theorem** follows from the stated definitions;
- a **counterexample** proves that a proposed monotonicity or invariance property does not hold in general;
- a **reporting convention** is an auditable rule adopted to isolate the source of sensitivity;
- an **empirical regularity** must be estimated in a dataset or simulation and is not guaranteed mathematically.

## 2. Objects

Let the finite observed state space be

\[
S=\{s_1,\ldots,s_K\}.
\]

For observation \(i\), let \(Z_i\in S\) denote its recorded state. An outcome definition is a non-empty subset \(d\subseteq S\). It induces the binary indicator

\[
Y_i(d)=\mathbb{1}\{Z_i\in d\}.
\]

For a locked analytical sample of size \(n\), the definition-specific outcome level is

\[
L_n(d)=\frac{1}{n}\sum_{i=1}^{n}Y_i(d).
\]

For any state \(s\in d\), the internal composition of the positive class is

\[
C_{n,s}(d)=
\frac{\sum_{i=1}^{n}\mathbb{1}\{Z_i=s\}}
{\sum_{i=1}^{n}Y_i(d)}
\]

when the positive-class denominator is non-zero.

Let \(X\) denote an organisational descriptor or grouping variable. An association diagnostic is written abstractly as

\[
A_n(d;X)=\mathcal{A}\{Y(d),X\}.
\]

The reference implementation currently uses Pearson's chi-square and bias-unadjusted Cramér's \(V\) for categorical \(X\), but the formal logic does not require that particular association measure.

A substantive claim \(q\) has an evidential support set \(E_q\subseteq S\): the set of observed states for which the claim is semantically defensible. ODSA defines claim admissibility as

\[
\Gamma(q,d)=\mathbb{1}\{d\subseteq E_q\}.
\]

This is a necessary semantic condition. It does not guarantee that the underlying state labels are themselves valid or that causal language is warranted.

## 3. Proposition 1: level monotonicity under nesting

**Proposition 1.** If \(d_1\subseteq d_2\), then

\[
L_n(d_1)\leq L_n(d_2).
\]

Moreover,

\[
L_n(d_2)-L_n(d_1)
=
\frac{1}{n}
\sum_{i=1}^{n}
\mathbb{1}\{Z_i\in d_2\setminus d_1\}.
\]

**Proof.** For every observation,

\[
\mathbb{1}\{Z_i\in d_1\}
\leq
\mathbb{1}\{Z_i\in d_2\}
\]

because membership in \(d_1\) implies membership in \(d_2\). Summation and division by the common positive denominator \(n\) preserve the inequality. Subtracting the two indicators yields the indicator for \(d_2\setminus d_1\). \(\square\)

**Interpretation.** A broader nested definition cannot reduce the reported level when the denominator is locked. This result is arithmetic, not empirical. It does not imply that the broader definition is preferable.

## 4. Proposition 2: the level–composition identity

**Proposition 2.** If \(d_1\subseteq d_2\) and \(L_n(d_2)>0\), then

\[
\frac{L_n(d_1)}{L_n(d_2)}
=
\sum_{s\in d_1}C_{n,s}(d_2).
\]

**Proof.** The numerator on the left is the count of observations in \(d_1\) divided by \(n\). The denominator is the count in \(d_2\) divided by \(n\). Their ratio is therefore the share of the \(d_2\) positive class contributed by states in \(d_1\), which equals the sum of the corresponding composition shares. \(\square\)

**Interpretation.** A headline-level difference and the internal composition of a broad outcome are not separate phenomena. The composition register explains exactly what the broader headline adds.

## 5. Proposition 3: association is not monotone under nesting

**Proposition 3.** The nesting relation \(d_1\subseteq d_2\) imposes no general ordering on \(A_n(d_1;X)\) and \(A_n(d_2;X)\). In particular, Cramér's \(V\) for the broader definition may be greater than, less than or equal to the value for the narrower definition.

**Proof by counterexample.** Consider two equally sized groups and three states: active use, project stage and other.

In the first table, the active-use rates are 0.20 and 0.10 while the broad rates are 0.20 and 0.60:

| Group | Active use | Project stage | Other |
|---|---:|---:|---:|
| 1 | 20 | 0 | 80 |
| 2 | 10 | 50 | 40 |

The broader definition has the stronger association.

In the second table, the active-use rates are 0.20 and 0.05 while both broad rates are 0.60:

| Group | Active use | Project stage | Other |
|---|---:|---:|---:|
| 1 | 20 | 40 | 40 |
| 2 | 5 | 55 | 40 |

The broader definition has zero association although the narrower definition does not. Equality is obtained whenever the additional states are distributed so that the chosen association measure is unchanged. Therefore no monotone ordering exists. \(\square\)

**Interpretation.** The effect of broadening depends on how the added states are distributed across groups, not only on their overall frequency.

## 6. Proposition 4: group rankings may reverse

**Proposition 4.** Nested definitions can imply different orderings of group rates.

**Proof by counterexample.** Let Group 1 have 30 active-use cases and no project-stage cases out of 100 observations. Let Group 2 have 10 active-use cases and 50 project-stage cases out of 100. Group 1 ranks above Group 2 under active use (0.30 versus 0.10), but Group 2 ranks above Group 1 under broad engagement (0.60 versus 0.30). \(\square\)

**Interpretation.** A definition change can alter not only the magnitude of an association but the identity of the group described as leading or lagging.

## 7. Proposition 5: claim admissibility is a subset condition

**Proposition 5.** Under the stated semantics, a claim \(q\) is admissible for definition \(d\) only if \(d\subseteq E_q\).

**Proof.** If \(d\not\subseteq E_q\), there exists at least one state \(s\in d\setminus E_q\). An observation in state \(s\) is coded positive by \(d\) although the evidential condition for \(q\) is not met. Consequently the positive class cannot uniformly support the claim. \(\square\)

**Boundary.** This proposition is semantic and conditional on a defensible specification of \(E_q\). ODSA cannot establish that specification automatically. The claim register must therefore be authored, justified and reported.

## 8. Proposition 6: exact recoverability after coarsening

Let a reporting or measurement process apply a map

\[
g:S\rightarrow T,
\]

where \(T\) is a coarser observed state space. The fibre associated with \(t\in T\) is \(g^{-1}(t)\).

**Proposition 6.** A fine-state definition \(d\subseteq S\) is exactly recoverable from \(g(Z)\) if and only if membership in \(d\) is constant within every fibre of \(g\).

**Proof.**

- **Sufficiency.** If membership is constant within each fibre, define a reported-state outcome \(d_T\subseteq T\) by including \(t\) whenever the states in \(g^{-1}(t)\) are positive under \(d\). Then \(\mathbb{1}\{Z\in d\}=\mathbb{1}\{g(Z)\in d_T\}\).
- **Necessity.** If one fibre contains both a positive fine state and a negative fine state, both produce the same reported state \(t\). No function of \(t\) alone can assign different binary memberships to them.

Therefore the condition is necessary and sufficient. \(\square\)

**Interpretation.** Once planning, testing and deployment are collapsed into one project-stage category, a definition that includes testing and deployment but excludes planning cannot be recovered without an additional assumption or new data.

## 9. Proposition 7: misclassification changes levels linearly in expectation

Let the true state-probability row vector be \(p\) and let \(M\) be a row-stochastic misclassification matrix, where \(M_{jk}\) is the probability that true state \(s_j\) is recorded as \(s_k\). The expected recorded probability vector is

\[
p^\ast=pM.
\]

For definition vector \(v_d\), whose entries indicate membership in \(d\),

\[
\mathbb{E}\{L_n^\ast(d)\}=pMv_d.
\]

The expected level bias is therefore

\[
p(M-I)v_d.
\]

**Interpretation.** Misclassification can increase, decrease or leave a definition-specific level unchanged. Its direction is governed by net flows across the definition boundary. Association and ranking effects are not generally linear because they depend on group-specific transition processes and nonlinear diagnostics.

## 10. Proposition 8: denominator locking is required for attribution

Suppose two reported levels are computed on analytical samples \(\mathcal{I}_1\) and \(\mathcal{I}_2\). If the samples differ, then

\[
L_{\mathcal{I}_2}(d_2)-L_{\mathcal{I}_1}(d_1)
\]

combines outcome-definition sensitivity with sample-composition sensitivity.

**Reporting convention.** ODSA therefore requires a locked denominator for the primary comparison. Analyses with alternative missing-data rules or sample restrictions must be reported as separate sensitivity layers.

This is a design rule rather than a theorem about the data-generating process. Its purpose is attribution: it prevents a definition difference from being confounded with a change in the cases being analysed.

## 11. Proposition 9: overlapping definitions require pairwise interpretation

If neither \(d_1\subseteq d_2\) nor \(d_2\subseteq d_1\), the difference in levels decomposes as

\[
L_n(d_2)-L_n(d_1)
=
L_n(d_2\setminus d_1)-L_n(d_1\setminus d_2).
\]

There is no general sign restriction. ODSA must therefore report the set relation and both asymmetric difference sets. Treating overlapping definitions as if one were a broader version of the other is invalid.

## 12. What the propositions do not establish

The formal results do not establish that:

- the observed states exhaust the construct domain;
- state labels correspond to verified organisational practice;
- one definition is substantively correct for every research question;
- an association is causal;
- a statistically stable definition is semantically adequate;
- a semantically adequate definition has acceptable reliability;
- a broad measure is intrinsically inferior to a narrow one.

The propositions instead specify what follows once states, definitions, claims, grouping variables and denominators have been declared.

## 13. Executable verification

The repository verifies the propositions through:

- deterministic identities for nested levels and compositions;
- explicit counterexamples for association monotonicity;
- explicit counterexamples for group-ranking stability;
- tests of coarsening recoverability;
- tests of row-stochastic misclassification matrices;
- deterministic simulation registries and seed handling.

The executable tests are evidence that the implementation conforms to the stated propositions. They are not a substitute for mathematical argument or external empirical validation.
