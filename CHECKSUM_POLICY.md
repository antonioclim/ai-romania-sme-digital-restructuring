# Checksum policy

`SHA256SUMS.txt` records the packaged repository snapshot. It should pass immediately after cloning or downloading the release archive, before regeneration.

After `python scripts/run_all.py`, deterministic data tables and figures should be regenerated from the cleaned dataset. Some runtime files, especially logs and generation manifests with run-specific fields, may be refreshed by the pipeline. In that case, rerun `python scripts/verify_sha256sums.py SHA256SUMS.txt` only before regeneration, or regenerate the manifest intentionally for a new release.

The GitHub Actions workflow follows this order: verify the packaged snapshot, run the pipeline, compile sources and execute tests.
