# Outcome-Definition Sensitivity Analysis (ODSA)

**Development version:** 3.0.0-rc1  
**Target release:** 3.0.0  
**Status:** formal-method and simulation-protocol release candidate  
**Repository:** `antonioclim/ai-romania-sme-digital-restructuring`

## Purpose

Outcome-Definition Sensitivity Analysis audits how substantively defensible
definitions of a categorical outcome change:

- the reported level;
- the internal composition of the positive class;
- association with organisational descriptors;
- subgroup order;
- the claims that the measure can support.

The version 3 line generalises the earlier aggregate reproduction workflow into
a reusable Information Systems methodology. It preserves the aggregate-only
public boundary of version 2.0.2.

## Current evidential status

Version `3.0.0-rc1` is not a final archival release and does not claim a new
DOI. The final `3.0.0` release will be frozen only after the full simulation,
independent replication, article-output crosswalk and journal-facing
documentation pass hostile audit.

The Romanian organisational AI example uses aggregate counts only. Its
empirical unit is one completed response, not a verified unique firm. It does
not estimate national prevalence, identify causal effects, establish verified
deployment or demonstrate realised organisational value.

## Implemented formal diagnostics

Given a finite observed state space \(S\) and a definition \(d\subseteq S\),
the current branch implements:

1. definition relations;
2. exact symmetric-difference level decomposition;
3. definition-specific levels and Wilson intervals;
4. positive-class composition;
5. descriptive total variation between compositions;
6. Pearson chi-square and Cramér's \(V\);
7. association contrasts;
8. subgroup rates and pairwise order disagreement;
9. conservative claim admissibility.

ODSA does not combine these diagnostics into one score.

## Candidate simulation protocol

The branch includes:

- six controlled state-distribution mechanisms;
- balanced and skewed group allocation;
- within-broad and boundary-crossing misclassification;
- state-independent and project-heavy missingness;
- separation of generating population, sampled true and observed values;
- a deterministic CI subset.

CI output verifies software mechanics only. It is not manuscript evidence.

## Quick start

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
python -m pytest -q tests_v3
python scripts/run_study1.py
python simulations/run_simulation.py --replications 2000 --seed 20260813
python simulations/run_factorial_protocol.py --mode ci
```

The command-line interface is available as:

```bash
odsa --help
```

## Repository structure

- `odsa/` — generic ODSA implementation
- `examples/romanian_ai_engagement/` — aggregate-only Study 1 inputs
- `simulations/` — smoke simulation and candidate factorial protocol
- `scripts/` — reproducible study entry points
- `tests_v3/` — regression, formal-property and protocol tests
- `docs_v3/` — formal specification, novelty boundary and reporting guidance
- `outputs_v3/` — generated CI diagnostics; not manuscript-final evidence
- `data/aggregate/`, `metadata/` and `outputs/` — version 2.0.2 compatibility
  material retained during the RC period

## Methodological boundary

ODSA is complementary to construct-validity work, multiverse analysis and
specification-curve analysis. It does not presume that alternative outcome
definitions estimate one unchanged construct. It first asks which states each
definition counts and which claims remain compatible with all positive states.

See:

- `docs_v3/FORMAL_PROPERTIES_AND_PROOFS.md`
- `docs_v3/ADJACENT_METHODS_AND_NOVELTY_BOUNDARY.md`
- `docs_v3/SIMULATION_PROTOCOL.md`
- `docs_v3/REPORTING_CHECKLIST.md`

## Privacy and reproducibility boundary

The version 3 public workflow contains no respondent-level survey rows,
free-text answers, direct identifiers, precise timestamps, IP addresses or
paradata. Study 1 is reproducible from frozen aggregate counts and
low-dimensional group-by-state tables.

Respondent-level recoding, duplicate adjudication and linkage to unique
organisations remain outside the public evidence boundary.

## Version lineage

- `v2.0.2` remains the current published aggregate reproduction package:
  DOI `10.5281/zenodo.21603732`.
- `3.0.0-rc1` is the active development branch for the generic method.
- `v3.0.0` will supersede `v2.0.2` only for the final Information &
  Management methodology article and its aligned reproducibility workflow.

## Citation

Do not cite the RC branch as a final archival release. A version-specific DOI
will be added only after reservation and final release freezing.

## Licence

Software and documentation are distributed under the MIT Licence. The licence
does not override ethical, legal or contractual restrictions applying to
non-public source material.
