# Information & Management manuscript architecture

## 1. Article identity

### Working title

**When outcome definitions change the phenomenon: Outcome-Definition Sensitivity Analysis for Information Systems research**

### Article type

Methodological Information Systems article with:

1. a formal framework;
2. a pre-specified simulation study;
3. an aggregate-only empirical application;
4. an independent replication;
5. cross-study implications for IS measurement and managerial reporting.

The Romanian AI application is Study 1, not the article's sole identity.

## 2. Central problem statement

Information Systems studies frequently compress heterogeneous process states into one categorical or binary outcome. Planning, testing, deployment, operational use and routinisation may all be defensible states to analyse, but they do not answer the same question. A result may therefore be numerically correct for its operationalisation while supporting a claim that is narrower than the states coded positive.

ODSA addresses the pre-model question:

> How sensitive are the reported level, internal composition, association, group ordering and admissible claims to defensible alternative definitions of the categorical outcome?

The method complements rather than replaces construct validation, measurement invariance, multiverse analysis, specification curves and causal sensitivity analysis.

## 3. Proposed section structure

### 1. Introduction — target 1,000–1,200 words

The introduction should:

- establish outcome-definition sensitivity as an IS measurement problem;
- use AI adoption only as a motivating example;
- distinguish model-specification uncertainty from outcome-semantic uncertainty;
- identify the absence of a dedicated audit linking state inclusion to headline levels, associations, rankings and claims;
- state the method, simulation, Study 1 and Study 2 contributions;
- avoid presenting ODSA as a universal score or automatic definition selector.

The final paragraph should state four contributions:

1. a formal state–definition–claim framework;
2. mathematical properties and counterexamples;
3. a reproducible simulation and software implementation;
4. empirical demonstration and independent replication.

### 2. Conceptual foundations — target 1,400–1,700 words

#### 2.1 States, constructs and categorical operationalisation

Cover construct–indicator alignment, state granularity and the consequences of coarsening.

#### 2.2 Adoption, implementation, assimilation and use

Clarify why these labels are related but not interchangeable in IS research.

#### 2.3 Existing sensitivity traditions

Position ODSA relative to robustness checks, multiverse analysis, specification curves, vibration of effects, outcome misclassification analysis, measurement invariance and construct-validity audits.

#### 2.4 Unresolved gap

Explain that existing approaches do not usually require an explicit register of positive states, their internal composition and the claims each definition can support.

### 3. Outcome-Definition Sensitivity Analysis — target 1,800–2,200 words

#### 3.1 State space and definition register

Define \(S\), \(d\) and \(Y_i(d)\). Report pairwise set relations.

#### 3.2 Level and composition diagnostics

Define \(L(d)\) and \(C_s(d)\). Present level monotonicity and the level–composition identity.

#### 3.3 Association and ranking diagnostics

Define \(A(d;X)\), signed group contrasts, rank signatures and normalised rank distance. State that association monotonicity does not follow from nesting.

#### 3.4 Claim admissibility

Define the evidential support set \(E_q\) and \(\Gamma(q,d)=\mathbb{1}\{d\subseteq E_q\}\). Emphasise that the claim register requires substantive judgement.

#### 3.5 Coarsening and recoverability

State the fibre-constancy condition and explain why unrecoverable definitions must be reported rather than imputed silently.

#### 3.6 Misclassification

Show \(p^\ast=pM\) and the expected level bias. Separate misclassification from deliberate broadening.

#### 3.7 ODSA workflow and reporting minimum

Present the algorithm, required inputs, outputs, assumptions, failure conditions and the cases in which ODSA adds little.

### 4. Simulation study — target 1,300–1,600 words

#### 4.1 Objectives and pre-specification

State the questions, profiles, frozen factors and seed policy.

#### 4.2 Data-generating process

Describe fine states, base profiles, group signals, sample sizes, misclassification and coarsening.

#### 4.3 Estimands

Define level inflation, claim-relative contamination, \(\Delta_V\), ranking distance, direction reversal, measurement bias and recoverability.

#### 4.4 Results

Report scenario-level patterns, not p-values on simulation replications.

#### 4.5 Implications for empirical design

Identify when a headline outcome is most vulnerable and what minimum disclosure is required.

### 5. Study 1: organisational AI engagement — target 1,400–1,700 words

#### 5.1 Context and research use

Describe the open Romanian LimeSurvey response set without implying national representativeness.

#### 5.2 Ethics, participant information and data minimisation

Report the participant-facing information, completion-based consent and the institutional ethics status exactly as documented at submission time.

#### 5.3 State and definition register

Explain active use, project stage and broad engagement. State the coarsening that prevents separation of planning, testing and deployment.

#### 5.4 Analysis

Use the locked denominator, Wilson intervals, composition, Cramér's \(V\), group rates and ranking diagnostics. Add bootstrap or exact sensitivity where defensible.

#### 5.5 Results

Present Study 1 as a worked empirical stress test, not validation of national adoption prevalence.

### 6. Study 2: independent replication — target 1,200–1,500 words

#### 6.1 Pre-specified dataset selection

Report the search, scoring and selection process.

#### 6.2 Context and operationalisation

Describe the independent technology, sample, state structure and definitions.

#### 6.3 Replication results

Report the same ODSA core diagnostics and any differences in applicability.

#### 6.4 Cross-study comparison

Compare failure modes and boundary conditions rather than demanding numerical replication.

### 7. General discussion — target 1,300–1,600 words

#### 7.1 Contribution to IS measurement

Explain outcome-semantic sensitivity as a distinct analytical layer.

#### 7.2 Relationship to existing methods

State what ODSA contributes and what it leaves to other approaches.

#### 7.3 Managerial implications

Explain why KPI design should report the definition, composition and inference boundary. Avoid claiming that ODSA improves decisions unless directly tested.

#### 7.4 Boundary conditions

Discuss binary-only data, overlapping states, latent constructs, continuous intensity, non-exclusive states and unrecoverable coarsening.

#### 7.5 Limitations and research agenda

Retain explicit limitations of both empirical studies and the simulation.

### 8. Conclusion — target 250–350 words

State the narrow contribution:

- outcome definitions can change the measured phenomenon;
- nested broadening guarantees level monotonicity but not association or ranking stability;
- claim admissibility and recoverability must be audited;
- ODSA provides a transparent reporting framework, not an automatic truth selector.

## 4. Tables

### Main-text tables

1. **Table 1** — ODSA concepts, diagnostics and interpretation.
2. **Table 2** — Formal propositions and their status.
3. **Table 3** — Simulation factors and estimands.
4. **Table 4** — Study 1 definition register and results.
5. **Table 5** — Study 2 definition register and results.
6. **Table 6** — Cross-study claim-survival and boundary-condition matrix.

### Supplementary tables

- complete scenario registry;
- simulation scenario summaries;
- Study 1 contingency tables;
- Study 1 robustness results;
- Study 2 candidate register;
- Study 2 full diagnostics;
- article–code–output crosswalk;
- AI assistance and validation register.

## 5. Figures

### Main-text figures

1. **Figure 1** — ODSA state–definition–claim architecture.
2. **Figure 2** — Definition relations, coarsening fibres and recoverability.
3. **Figure 3** — Simulation design and primary estimands.
4. **Figure 4** — Simulation results for association and rank sensitivity.
5. **Figure 5** — Study 1 level, composition and group-rate sensitivity.
6. **Figure 6** — Cross-study synthesis.

All quantitative figures must be generated from versioned source data. Any explanatory figure prepared with AI assistance must carry the disclosure required by the applicable Elsevier policy and be independently reviewed by the author.

## 6. Claims that must not appear

The manuscript must not claim that:

- ODSA proves one correct definition;
- broad outcomes are inherently invalid;
- Study 1 estimates Romanian national prevalence;
- employee band causes organisational engagement;
- a completed response is a verified unique firm;
- project-stage engagement is realised use;
- Study 2 was selected because it confirmed Study 1;
- simulation frequencies are mathematical laws;
- public availability removes all ethical obligations;
- the repository reproduces respondent-level recoding when it does not.

## 7. Evidence hierarchy

Every central statement should be labelled internally according to its evidence source:

| Evidence type | Permitted language |
|---|---|
| Mathematical proposition | must, follows, is guaranteed under assumptions |
| Counterexample | can, need not, no general monotonicity |
| Simulation | occurred in X% of simulated replications under the design |
| Study 1 | in this response set |
| Study 2 | in the selected independent dataset |
| Cross-study synthesis | across the two applications |
| Managerial implication | suggests, implies for reporting, warrants audit |

This hierarchy prevents simulation, empirical and theoretical claims from being blended.

## 8. Approximate length

A defensible target is 10,500–12,500 words including the main text and declarations but excluding references and online appendices. The exact journal limit must be reverified in the live submission system before final formatting.

The method should not be compressed to preserve the structure of the previous TASM manuscript. The new article is a substantially different scientific object.

## 9. Submission-facing files

The final package should contain:

```text
IM_Manuscript_With_Author_Details.docx
IM_Manuscript_Anonymous.docx
IM_Title_Page.docx
IM_Highlights.docx
IM_Cover_Letter.docx
IM_Supplementary_Methods.pdf
IM_Supplementary_Tables.xlsx or .docx
Figure_1.tif ... Figure_6.tif
Graphical_Abstract.* only if permitted and not generated by general-purpose AI
```

The reviewer-facing manuscript and all supplements must be anonymised consistently.

## 10. Current status

This document fixes the target architecture. It is not yet the manuscript. Drafting begins only after:

- formal propositions pass audit;
- the simulation protocol is frozen;
- Study 2 is selected;
- the ethics statement is institutionally defensible;
- repository outputs can be mapped one-to-one to article claims.
