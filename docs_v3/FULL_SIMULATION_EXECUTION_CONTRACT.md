# Frozen full-simulation execution contract

## Status

This document governs IM-R4 execution of the simulation protocol frozen in IM-R3. It does not alter `simulations/manuscript_protocol.yml`.

## Evidence boundary

The full simulation is computational evidence conditional on the frozen data-generating design. It is not human-participant data, empirical prevalence evidence or proof that one outcome definition is universally superior.

## Frozen design identity

```text
Protocol: simulations/manuscript_protocol.yml
SHA-256: 157bc88f41ff68261253fb19e79cc2c0aeebe63a4687d1f1073edd25ecc0b8f3
Factorial cells: 432
Pooled replications per cell: 4,000
Pooled replicate rows: 1,728,000
```

## Independent streams

The execution uses `numpy.random.SeedSequence` with root entropy `20260814`. Four child streams are spawned before any full results are examined. Each stream executes 432 cells × 1,000 replications = 432,000 rows.

A stream is not manuscript evidence by itself. Pooled evidence is created only after all four streams pass protocol-hash, cell-count, row-count, file-hash and seed-independence checks.

## Required outputs

Each stream must produce:

- `factorial_replicates.csv`;
- `factorial_cell_summary.csv`;
- `protocol_run_audit.json`;
- `full_stream_audit.json`.

The pooled job must produce:

- `factorial_replicates_pooled.csv.gz`;
- `factorial_cell_summary_pooled.csv`;
- `stream_convergence.csv`;
- `undefined_diagnostics.csv`;
- `pooled_execution_audit.json`;
- `manuscript_simulation_core_results.csv`;
- `hostile_full_simulation_audit.json`;
- `HOSTILE_FULL_SIMULATION_AUDIT.md`;
- prespecified PNG and SVG figures.

## Convergence audit

Stream-specific means are compared with pooled means after accounting for their Monte Carlo standard errors. Convergence is classified as `PASS`, `WARNING` or `FAIL`. These are execution diagnostics, not tests of empirical hypotheses.

## Undefined-result audit

For every cell and primary diagnostic:

- undefined share ≤ 1%: normal reporting;
- >1% and ≤5%: warning and explicit sparsity discussion;
- >5%: no comparative manuscript claim for that cell and diagnostic.

Undefined results are never silently deleted or imputed.

## Prespecified hostile checks

The pooled audit verifies that:

1. the project-only gradient creates a positive broad-minus-active association contrast under the no-error, large-sample condition;
2. the compensating gradient creates a negative contrast;
3. the null same-mixture scenario does not create a material systematic contrast;
4. the rank-reversal mechanism recovers a high probability of strict reversal at the largest sample size;
5. active/project swapping preserves the broad positive count exactly in the absence of missingness;
6. all streams, hashes, cells and pooled replicate identifiers are complete.

Failure does not authorise post hoc modification of the frozen design. It requires diagnosis and transparent reporting.

## Release boundary

Full simulation completion does not authorise selection of Study 2 after inspecting candidate results, merging the RC branch into `main`, creating tag `v3.0.0`, publishing a GitHub release, creating or publishing Zenodo version 3.0.0 or submitting the manuscript before ethics and article–output gates close.
