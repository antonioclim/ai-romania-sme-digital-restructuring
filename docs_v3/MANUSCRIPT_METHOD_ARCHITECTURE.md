# Information & Management manuscript architecture for ODSA

## 1. Article identity

The final article is a methodological Information Systems contribution with empirical demonstrations. The Romanian AI survey is Study 1, not the sole basis of the contribution.

Provisional title:

> Outcome-Definition Sensitivity Analysis: Auditing categorical outcomes in Information Systems research

## 2. Contribution logic

The manuscript must establish four linked contributions.

1. **Conceptual contribution:** outcome broadening is distinguished from engagement-state conflation.
2. **Formal contribution:** ODSA provides a state–definition–claim framework with explicit invariants, non-invariants and coarsening boundaries.
3. **Methodological contribution:** a reproducible audit compares levels, composition, associations, rankings and claim admissibility across prespecified definitions.
4. **Empirical contribution:** simulation, Study 1 and an independent Study 2 show when the diagnostics matter and when they add little.

## 3. Proposed main-text structure

### 1. Introduction

- establish outcome operationalisation as a source of inferential sensitivity in IS;
- explain why binary adoption labels can combine states with different evidential meanings;
- distinguish the problem from ordinary model-specification sensitivity;
- state the four contributions;
- preview the multi-study design.

### 2. Conceptual foundations

#### 2.1 Adoption, implementation, assimilation and use

Clarify why these terms cannot be treated as automatically interchangeable.

#### 2.2 Construct–indicator–inference alignment

Explain the difference between a defensible measure and a defensible claim based on that measure.

#### 2.3 Related sensitivity frameworks

Position ODSA relative to multiverse analysis, specification curves, robustness checks, construct-validity audits, misclassification analysis and measurement invariance.

#### 2.4 Outcome broadening versus state conflation

Develop the conceptual distinction and its implications for IS research and managerial metrics.

### 3. Outcome-Definition Sensitivity Analysis

#### 3.1 State space and definitions

Introduce \(S\), \(d_j\) and \(Y_i(d_j)\).

#### 3.2 Level and composition

Introduce \(L(d_j)\), the exact increment and \(C_s(d_j)\).

#### 3.3 Association and ranking sensitivity

Introduce \(A(d_j;X)\), group rates and rank reversals.

#### 3.4 Claim admissibility

Introduce \(E(q)\) and the conservative rule \(\Gamma(q,d_j)\).

#### 3.5 Coarsening and identifiability

State and explain the fibre-union condition.

#### 3.6 Six-step workflow and boundary conditions

Separate mathematical guarantees from empirical diagnostics and interpretive registration.

### 4. Simulation study

#### 4.1 Design

Report the five-state latent space, definitions, groups, factorial factors, replications and seed.

#### 4.2 Evaluation metrics

Report level bias, association differences, rank reversals, apparent denominator violations and definition identifiability.

#### 4.3 Results

Organise results by mechanism rather than listing all factorial cells. Report the complete cell table in supplementary material.

#### 4.4 Simulation implications

State which ODSA properties are invariant, which are contingent and which failure modes require explicit reporting.

### 5. Study 1: organisational AI engagement

#### 5.1 Context and sample boundary

Preserve the current disclosure regarding open recruitment, completed responses, the SME-eligible analytical subset and the inability to verify unique firms.

#### 5.2 Instrument and state register

Present active use, project stage and other engagement states without treating them as a validated maturity scale.

#### 5.3 ODSA results

Report levels, composition, employee-band associations, rankings and claim admissibility.

#### 5.4 Robustness and limitations

Add bootstrap or exact sensitivity diagnostics where defensible, and preserve all sampling and coarsening limitations.

### 6. Study 2: independent IS replication

#### 6.1 Dataset selection and prespecification

Report the candidate protocol and why the selected dataset passed it.

#### 6.2 State and definition register

Freeze the mapping before reporting subgroup results.

#### 6.3 Replication results

Apply the same ODSA core while allowing domain-specific claim wording.

#### 6.4 Cross-study synthesis

Compare types of sensitivity, not only effect magnitudes.

### 7. General discussion

#### 7.1 Contribution to IS measurement

Explain how ODSA complements, rather than replaces, construct validation and model-specification sensitivity methods.

#### 7.2 Contribution to adoption and use research

Show how stage-sensitive operationalisation changes the phenomenon represented by an outcome.

#### 7.3 Managerial implications

Connect headline metrics to distinct intervention problems without claiming that ODSA has already improved decisions unless a managerial validation study is added.

#### 7.4 Boundary conditions

Report conditions under which ODSA adds little, definitions are non-identifiable or a continuous/latent model is preferable.

### 8. Conclusion

State the method's narrowest defensible contribution and avoid prevalence, causal or universal-performance claims.

## 4. Main-text display plan

| Display | Role |
|---|---|
| Figure 1 | ODSA state–definition–claim architecture |
| Figure 2 | Simulation mechanisms and principal sensitivity regions |
| Figure 3 | Study 1 level and composition results |
| Figure 4 | Study 1 group-rate and association sensitivity |
| Figure 5 | Study 2 cross-definition results |
| Table 1 | ODSA notation and formal properties |
| Table 2 | Simulation design factors |
| Table 3 | Study 1 definition register and claim boundaries |
| Table 4 | Study 1 principal diagnostics |
| Table 5 | Study 2 principal diagnostics |
| Table 6 | Cross-study boundary-condition synthesis |

The final number of displays will be reduced if journal economy requires it. Every numerical display must be generated from the release workflow.

## 5. Supplementary material plan

- complete formal proofs and constructive counterexamples;
- full simulation cell register and summaries;
- candidate audit matrix for Study 2;
- complete definition and claim registers;
- extended Study 1 diagnostic tables;
- extended Study 2 diagnostic tables;
- computational environment and article–output crosswalk;
- ethics, consent and data-governance documentation appropriate for editorial review.

## 6. Claim allocation by evidence source

| Claim type | Formal framework | Simulation | Study 1 | Study 2 |
|---|---:|---:|---:|---:|
| Nested definitions guarantee level monotonicity with a common denominator | primary | verification | illustration | illustration |
| Association need not be monotone | proof/counterexample | primary stress test | illustration | replication |
| Rankings can reverse | proof/counterexample | primary stress test | illustration | replication |
| Coarsening makes some definitions non-identifiable | primary | stress test | direct boundary | replication boundary |
| ODSA is useful beyond AI engagement | insufficient alone | insufficient alone | insufficient alone | primary |
| ODSA improves managerial decisions | not established | decision-loss proxy only | not established | not established unless separately tested |

## 7. Writing controls

The final manuscript must:

- use British English consistently;
- avoid describing the Romanian response set as nationally representative;
- avoid treating completed responses as verified unique firms;
- avoid treating planning, testing, deployment and active use as a validated scalar sequence;
- distinguish statistical significance from managerial meaning;
- distinguish simulation frequencies from empirical prevalence;
- distinguish claim compatibility from construct validity;
- cite data, software and archival releases as research objects;
- state AI assistance in Methods, captions and the final declaration where required.

## 8. Current gate

The architecture is ready for section-level drafting only after the formal properties and simulation engine pass CI. Study 2 and the institutional ethics determination remain hard gates before final submission.
