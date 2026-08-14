# Contributing to the ODSA version 3 line

Version `3.0.0-rc1` is a controlled methodological release candidate. Contributions should be proposed against the `im-v3.0.0-rc1` branch and must preserve the aggregate-only public-data boundary.

## Required checks

```bash
python -m pip install -e ".[test]"
python -m pytest -q tests_v3
python scripts/run_study1.py
python simulations/run_simulation.py --replications 2000 --seed 20260813
```

A contribution must:

- include tests for new methodological behaviour;
- preserve Study 1 regression values unless a documented scientific change is authorised;
- avoid respondent-level data, free text, identifiers, precise timestamps and paradata;
- update the method specification and changelog when behaviour changes;
- distinguish evidence from interpretation;
- disclose material use of generative AI in code, documentation or explanatory figures.

Do not open a pull request containing private survey exports, respondent-level rows, ethics correspondence or access credentials. Security or disclosure-boundary concerns should be reported privately to the repository owner.
