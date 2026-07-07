# Checksum policy

`SHA256SUMS.txt` is a stable source-and-metadata manifest. It excludes generated outputs, volatile logs, Python bytecode, caches and local runtime artefacts. It should pass before and after running the analysis.

`SHA256SUMS_GENERATED_OUTPUTS.txt` records generated non-log outputs after a full current reproduction run. It should be regenerated whenever analysis scripts are rerun intentionally.

Volatile logs are preserved for audit where useful but are not part of the stable source checksum gate.
