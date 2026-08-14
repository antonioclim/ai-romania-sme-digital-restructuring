# Outcome-Definition Sensitivity Analysis (ODSA)

**Development version:** 3.0.0-rc1  
**Target release:** 3.0.0  
**Status:** release candidate for methodological consolidation and independent validation  
**Repository:** https://github.com/antonioclim/ai-romania-sme-digital-restructuring

## Purpose

Outcome-Definition Sensitivity Analysis (ODSA) audits how defensible alternative definitions of a categorical outcome change its reported level, internal composition, association with organisational descriptors and the claims that the measure can support.

The version 3 line generalises the earlier aggregate reproduction workflow into a reusable Information Systems methodology. It preserves the privacy-protective, aggregate-only architecture of version 2.0.2 while adding a formal state-space model, definition relations, claim-admissibility checks, group-ranking diagnostics, simulation support and reusable command-line tooling.

## Current evidential status

Version `3.0.0-rc1` is a development release candidate. It is not the final Zenodo release and it does not claim a new DOI. The final `3.0.0` release will be frozen only after the simulation design, independent replication, article-output crosswalk and journal-facing documentation pass the complete hostile audit.

The Romanian organisational AI example uses aggregate counts only. The empirical unit is one completed response, not a verified unique firm. The example does not estimate national prevalence, identify causal effects, establish verified deployment or demonstrate realised organisational value.

## Quick start

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
python -m pytest -q
python scripts/run_study1.py
python simulations/run_simulation.py --replications 2000 --seed 20260813
```

The command-line interface is available as:

```bash
odsa --help
```

## Repository structure

- `odsa/` — generic ODSA implementation
- `examples/romanian_ai_engagement/` — aggregate-only Study 1 inputs
- `simulations/` — deterministic methodological simulation
- `scripts/` — reproducible study and release entry points
- `tests_v3/` — methodological and regression tests for the version 3 line
- `docs_v3/` — method specification, reporting guidance and governance documentation
- `data/aggregate/`, `metadata/` and `outputs/` — preserved version 2.0.2 compatibility material during the RC period

## Core diagnostics

Given an observed state space `S` and an outcome definition `d ⊆ S`, ODSA reports:

1. the definition register and relations among definitions;
2. definition-specific outcome levels;
3. the state composition of broader outcomes;
4. definition-specific associations with a descriptor;
5. group-rate ordering and rank reversals;
6. claim admissibility and explicit inference boundaries.

ODSA does not select one universally correct definition. A definition is evaluated against the question and claim it is intended to support.

## Privacy and reproducibility boundary

The public version 3 workflow contains no respondent-level survey rows, free-text answers, direct identifiers, precise timestamps, IP addresses or paradata. Study 1 is reproducible from frozen aggregate counts and low-dimensional group-by-state tables. Respondent-level recoding, duplicate adjudication and linkage to unique organisations are outside the public evidence boundary.

## Version lineage

- `v2.0.2` remains the current published aggregate reproduction package and is identified by DOI `10.5281/zenodo.21603732`.
- `3.0.0-rc1` is the development branch for the generic ODSA methodology.
- `v3.0.0` will supersede `v2.0.2` only for the final Information & Management methodology article and its aligned reproducibility workflow.

## Citation

Do not cite the RC branch as a final archival release. Citation metadata are provided in `CITATION.cff`; a version-specific DOI will be added only after reservation and final release freezing.

## Licence

Software and documentation are distributed under the MIT Licence. The licence does not override ethical, legal or contractual restrictions applying to non-public source material.
