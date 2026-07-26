# Reproducibility scope

## Reproduced from public aggregate inputs

The package recomputes the public tables, figures, descriptive percentages, Wilson intervals and exploratory association statistics from frozen aggregate counts and low-dimensional contingency tables. These inputs preserve the quantities required for the reported analysis without distributing respondent rows.

## Not reproduced publicly

The public package does not reproduce respondent-level recoding, duplicate adjudication, free-text interpretation or the transformation from the original survey exports to aggregate counts. Those operations require controlled source material and institutional authority. Their absence is an explicit evidence boundary rather than an unreported gap.

## Deterministic workflow

The canonical entry point is `scripts/build_aggregate.py`. `make all` verifies the aggregate inputs, checks generated metadata, validates the installed environment, rebuilds outputs, verifies output checksums, audits the public-release boundary, runs the test suite and checks the full manifest.

## Reference environment

The certified build uses Python 3.13 and the versions recorded in `requirements.lock.txt`. The release relies on exact package version pinning, deterministic input files and SHA-256 verification of source and generated outputs.
