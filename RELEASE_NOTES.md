# Release notes — ODSA 3.0.0-rc1

## Status

`3.0.0-rc1` is a development release candidate for the generic Outcome-Definition Sensitivity Analysis methodology. It is not the final Zenodo release and does not claim a new DOI.

## Major change from v2.0.2

Version 2.0.2 is an aggregate reproduction package for one survey analysis. The version 3 line develops a reusable Information Systems method with formal properties, generic software, simulation support and independent-replication controls.

## Implemented in the RC line

### Generic method engine

- explicit finite state spaces;
- named outcome definitions;
- equal, nested, disjoint and overlapping definition relations;
- definition-specific levels and Wilson intervals;
- positive-class composition;
- Pearson chi-square and Cramér's V;
- group-rate and ranking diagnostics;
- rank-reversal detection;
- conservative claim-admissibility audit;
- CLI and reproducible CSV/JSON outputs.

### Formal consolidation added in IM-R2

- exact nested-level increment diagnostics;
- executable common-denominator monotonicity check;
- state-coarsening transformation;
- definition identifiability based on complete mapping fibres;
- formal propositions and proofs;
- constructive examples showing association strengthening, association weakening and rank reversal;
- explicit separation of mathematical invariants, empirical diagnostics, information-loss findings and interpretive judgements.

### Simulation study added in IM-R2

- five-state latent Information Systems engagement model;
- five registered definitions, including one non-nested definition;
- complete 864-cell factorial design;
- sample-size, gradient, imbalance, misclassification, coarsening and denominator factors;
- latent, observed and reported diagnostics;
- measurement-bias and rank-disagreement metrics;
- apparent denominator-driven monotonicity violations;
- cell-level summaries and machine-readable global gates;
- deterministic seeds and CI-scale replication settings.

### Empirical compatibility

- aggregate-only Romanian Study 1 input files;
- exact reproduction of active-use, project-stage and broad-engagement levels;
- exact reproduction of the locked employee-band association diagnostics;
- claim-admissibility checks aligned to the registered state meanings.

### Governance and reporting

- formal method specification;
- simulation protocol;
- Study 2 selection protocol;
- Information & Management manuscript architecture;
- reporting checklist;
- ethics and data-governance boundary;
- AI-assistance disclosure;
- explicit RC branch status.

## Reproducibility gate

GitHub Actions must pass all of the following before the RC is considered technically coherent:

1. package installation;
2. version 3 tests;
3. Study 1 reproduction;
4. constructive counterexample generation;
5. deterministic smoke simulation;
6. complete factorial simulation gate;
7. version consistency;
8. diagnostic artifact generation.

## Data boundary

The public RC contains no respondent-level survey rows, free-text responses, direct identifiers, precise timestamps, IP addresses or paradata. Study 1 uses aggregate counts. Simulation outputs are wholly synthetic.

## Known limitations and hard gates

The following remain unresolved and prevent a final `v3.0.0` release:

- the manuscript-grade 500-replication-per-cell simulation run has not been frozen;
- no independent Study 2 has yet passed the selection protocol;
- the manuscript and article-output crosswalk are not final;
- the institutional ethics determination remains external to the software release;
- the final DOI has not been reserved;
- the final hostile audit and submission preflight have not been completed.

## Version lineage

- `v2.0.2` remains the current published aggregate package with DOI `10.5281/zenodo.21603732`.
- `3.0.0-rc1` is a non-archival development branch.
- `v3.0.0` will supersede `v2.0.2` only for the final methodological article and aligned release workflow.
