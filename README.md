# Outcome-Definition Sensitivity Analysis (ODSA)

**Development version:** 3.0.0-rc1  
**Target release:** 3.0.0  
**Status:** release candidate for methodological consolidation and independent validation  
**Repository:** https://github.com/antonioclim/ai-romania-sme-digital-restructuring

## Purpose

Outcome-Definition Sensitivity Analysis audits how defensible alternative definitions of a categorical outcome change its reported level, internal composition, association with organisational descriptors, group ordering and the claims that the measure can support.

The version 3 line generalises the earlier aggregate reproduction workflow into a reusable Information Systems methodology. It preserves the privacy-protective, aggregate-only architecture of version 2.0.2 while adding:

- a formal state–definition–claim model;
- mathematical propositions and executable counterexamples;
- definition-relation and claim-admissibility diagnostics;
- coarsening and exact-recoverability audits;
- state-misclassification simulation;
- group-ranking and direction-reversal diagnostics;
- deterministic simulation profiles;
- reusable command-line tooling.

## Evidential status

Version `3.0.0-rc1` is not the final Zenodo release and it does not claim a new DOI. Final version `3.0.0` will be frozen only after:

1. the simulation design and output schema pass the hostile audit;
2. the article simulation is completed;
3. an independently selected Study 2 is integrated;
4. the article–code–table–figure crosswalk is exact;
5. the journal-facing ethics and AI disclosures are defensible.

The Romanian organisational AI example uses aggregate counts only. The empirical unit is one completed response, not a verified unique firm. The example does not estimate national prevalence, identify causal effects, establish verified deployment or demonstrate realised organisational value.

## Quick start

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
python -m pytest -q tests_v3
python scripts/run_study1.py
python simulations/run_simulation.py --replications 2000 --seed 20260813
python simulations/run_article_simulation.py --profile ci --replications 25
```

The command-line interface is available as:

```bash
odsa --help
```

The command examples are for automated environments and computational reproducibility. Project coordination with the author is browser-only.

## Repository structure

- `odsa/` — generic ODSA implementation
- `examples/romanian_ai_engagement/` — aggregate-only Study 1 inputs
- `simulations/` — smoke, CI and pre-specified article simulations
- `scripts/` — reproducible study and release entry points
- `tests_v3/` — formal, methodological and empirical-regression tests
- `docs_v3/` — method, simulation, replication and governance documentation
- `data/aggregate/`, `metadata/` and `outputs/` — preserved version 2.0.2 compatibility material during the RC period

## Core diagnostics

Given an observed state space \(S\), an outcome definition \(d\subseteq S\) and an optional descriptor \(X\), ODSA reports:

1. the definition register and pairwise set relations;
2. definition-specific outcome levels;
3. state composition of multi-state positive classes;
4. definition-specific associations;
5. group-rate ordering, rank distance and reversals;
6. claim admissibility;
7. recoverability after coarsening;
8. sensitivity to state misclassification.

ODSA does not select one universally correct definition. A definition is evaluated against the question and claim it is intended to support.

## Formal and simulation documentation

- `docs_v3/METHOD_SPECIFICATION.md`
- `docs_v3/FORMAL_PROPOSITIONS.md`
- `docs_v3/SIMULATION_STUDY_PROTOCOL.md`
- `docs_v3/STUDY2_SELECTION_PROTOCOL.md`
- `docs_v3/IM_MANUSCRIPT_ARCHITECTURE.md`
- `docs_v3/REPORTING_CHECKLIST.md`

The article simulation contains 972 pre-specified core scenarios. The final frozen run will use 1,000 replications per scenario. A separate 144-scenario profile examines robustness to the number of groups. CI uses a much smaller replication count and must not be cited as journal evidence.

## Privacy and reproducibility boundary

The public version 3 workflow contains no respondent-level survey rows, free-text answers, direct identifiers, precise timestamps, IP addresses or paradata. Study 1 is reproducible from frozen aggregate counts and low-dimensional group-by-state tables.

Respondent-level recoding, duplicate adjudication and linkage to unique organisations are outside the public evidence boundary.

## Version lineage

- `v2.0.2` remains the current published aggregate reproduction package and is identified by DOI `10.5281/zenodo.21603732`.
- `3.0.0-rc1` is the development branch for the generic ODSA methodology.
- `v3.0.0` will supersede `v2.0.2` only for the final Information & Management methodology article and its aligned reproducibility workflow.

## Citation

Do not cite the RC branch as a final archival release. Citation metadata are provided in `CITATION.cff`; a version-specific DOI will be added only after it has been reserved and the final release has been frozen.

## Licence

Software and documentation are distributed under the MIT Licence. The licence does not override ethical, legal or contractual restrictions applying to non-public source material.
