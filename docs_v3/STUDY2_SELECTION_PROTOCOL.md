# Study 2 dataset selection and independent replication protocol

## 1. Purpose

Study 2 is intended to test whether ODSA remains informative outside the Romanian organisational AI response set. It must be independent in data source, substantive setting and analytical provenance. The replication is not a search for a second dataset that reproduces the same numerical pattern.

The selection protocol is fixed before outcome-sensitive results are examined to reduce researcher discretion and confirmation bias.

## 2. Required characteristics

A candidate dataset is eligible only if all of the following conditions are met.

### 2.1 Information Systems relevance

The focal variable must describe engagement with, implementation of or use of an information system, digital technology or data-driven organisational practice.

### 2.2 Multi-state outcome structure

The source must preserve at least three mutually exclusive observable states. A binary adoption variable alone is insufficient because the states that were collapsed cannot be recovered.

Preferred structures distinguish at least:

- pre-adoption or awareness;
- planning or consideration;
- implementation, trial or deployment;
- active use, assimilation or routinisation.

The exact labels need not match Study 1.

### 2.3 Multiple defensible outcome definitions

The state structure must support at least two substantively defensible definitions. At least one pair should be nested. An overlapping pair is desirable but not mandatory.

### 2.4 Grouping or descriptor variable

The dataset must contain at least one documented descriptor suitable for definition-specific association or group-rate analysis. Examples include organisational size, sector, country or region, role, technology class and institutional setting.

The descriptor must not be constructed from the outcome states themselves.

### 2.5 Sample adequacy

The analytical sample must be large enough to support the intended categorical diagnostics. No fixed universal threshold is imposed, but candidates with structural zeroes, pervasive sparse margins or fewer than 100 usable observations require explicit justification.

### 2.6 Documentation

The candidate must provide enough documentation to reconstruct:

- the unit of analysis;
- recruitment or sampling;
- state-variable wording and coding;
- descriptor coding;
- missing-data rules;
- weights, if any;
- collection dates;
- version and provenance.

### 2.7 Legal and ethical reusability

The data must be accessible under terms that permit the intended analysis and publication. The record must not contain an unresolved disclosure risk or a restriction that is incompatible with public reproducibility.

### 2.8 Stable identification

Preference is given to records with a DOI or another persistent identifier, versioned files and a citable data statement.

### 2.9 Independence

The dataset must not be:

- another export of the Romanian LimeSurvey instrument;
- a synthetic transformation of Study 1;
- produced by the same recoding decisions;
- selected because its results were already known to support ODSA.

## 3. Exclusion criteria

A candidate is excluded if any of the following applies:

1. only a binary outcome is available;
2. states are not mutually exclusive and no defensible state allocation is possible;
3. the operationalisation cannot be reconstructed from documentation;
4. access terms prohibit reproducible analysis;
5. privacy or disclosure status is unresolved;
6. the analytical unit is ambiguous in a way that cannot be bounded;
7. the candidate requires inventing state distinctions that are absent from the source;
8. the candidate duplicates Study 1 too closely to constitute independent evidence;
9. the only reason for inclusion is a favourable result.

## 4. Candidate scoring matrix

Eligible candidates are scored from 0 to 3 on seven dimensions.

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| IS relevance | peripheral | indirect | clear | central |
| State granularity | binary/unusable | three weak states | three or four clear states | four or more well-documented states |
| Sample adequacy | unusable | serious sparsity | adequate | strong |
| Documentation | insufficient | partial | adequate | complete |
| Legal and privacy clarity | unresolved | material uncertainty | usable with conditions | explicit and clear |
| Independence from Study 1 | derivative | closely related | substantially independent | different technology and context |
| Reproducibility potential | unavailable | limited | claim-level | end-to-end or near end-to-end |

A candidate proceeds only if:

- the total score is at least 17 out of 21;
- legal and privacy clarity is at least 2;
- state granularity is at least 2;
- documentation is at least 2;
- no exclusion criterion applies.

The score is recorded before ODSA results are generated.

## 5. Candidate search process

The search will be documented through:

- databases and repositories searched;
- search dates;
- exact search strings;
- candidate record identifiers;
- inclusion and exclusion reasons;
- scoring sheets;
- the final selection decision.

Likely sources include institutional repositories, Zenodo, Harvard Dataverse, UK Data Service, ICPSR, open government data portals and supplementary datasets attached to peer-reviewed IS research.

A candidate list will be frozen before any ODSA outcome tables are calculated.

## 6. Analytical plan for the selected dataset

### 6.1 Unit and denominator

The unit of analysis is taken from the source documentation. The primary ODSA comparison uses one locked analytical denominator.

Alternative missing-data rules, weighting and sample restrictions are reported as separate sensitivity layers.

### 6.2 State register

The replication will report:

- original source labels;
- harmonised labels;
- the rationale for any harmonisation;
- states excluded from particular definitions;
- any coarsening imposed by the public source.

No state is relabelled as active use unless the source wording supports that interpretation.

### 6.3 Definition register

Each definition will include:

- a short name;
- its positive states;
- the research question it answers;
- the claims it may support;
- the claims it may not support;
- its relation to every other definition.

### 6.4 Diagnostics

The replication will calculate:

- definition-specific levels and uncertainty intervals;
- positive-class composition;
- definition relations;
- definition-specific associations;
- group rates;
- ranking sensitivity;
- claim admissibility;
- recoverability under any source-level coarsening.

### 6.5 Cross-study synthesis

Study 2 is not required to reproduce the signs or magnitudes observed in Study 1. The cross-study synthesis asks whether:

- definition changes alter the measured phenomenon;
- association monotonicity fails;
- group rankings can change;
- broad definitions support different claims;
- coarsening limits recoverability.

Agreement concerns the operation of the audit, not identical substantive results.

## 7. Robustness and falsification

The independent replication must report findings that weaken ODSA's practical importance if they occur. Examples include:

- negligible level sensitivity;
- identical group rankings;
- nearly invariant associations;
- broad outcomes whose composition is substantively homogeneous;
- definitions that are semantically equivalent for the intended claim.

A dataset in which ODSA adds little is informative and must not be replaced post hoc.

## 8. Public release boundary

The public Study 2 package will include only material allowed by the source licence and disclosure rules. It will contain:

- source citation and persistent identifier;
- acquisition instructions;
- version or checksum where permitted;
- transformation code;
- state and definition registers;
- derived aggregate outputs;
- tests and claim–evidence mappings.

Source data will not be redistributed when the licence does not permit it. Reproducibility may then require the user to obtain the data from the original repository.

## 9. Ethics boundary

Reuse of an open dataset does not automatically remove ethical obligations. The selected record will be assessed for:

- original consent;
- intended reuse;
- identifiability;
- sensitive content;
- jurisdictional restrictions;
- the need for institutional review of secondary analysis.

The study will not describe public availability as proof that every secondary use is ethically unrestricted.

## 10. Decision record

The final release will include:

```text
docs_v3/STUDY2_CANDIDATE_REGISTER.csv
docs_v3/STUDY2_SELECTION_DECISION.md
examples/study2_<short_name>/
tests_v3/test_study2.py
```

The selection decision will state:

- all candidates considered;
- their scores;
- exclusion reasons;
- the chosen record;
- why the choice was made before examining ODSA results.

## 11. Current gate

At the IM-R2 stage this document defines the selection process. No dataset has yet been designated as Study 2 and no independent-replication claim is made.

The next gate is a documented search and scoring phase. The selected dataset must pass the legal, ethical, structural and methodological audit before code or manuscript claims are built around it.
