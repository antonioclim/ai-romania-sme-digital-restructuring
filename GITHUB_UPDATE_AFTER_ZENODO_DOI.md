# GitHub metadata update after Zenodo software publication

Software DOI: https://doi.org/10.5281/zenodo.21245180

Repository: https://github.com/antonioclim/ai-romania-sme-digital-restructuring

Release tag: `v1.0.0`

## Important

Do not edit or retag the already archived `v1.0.0` release unless you intentionally create a new Zenodo version. The files in this patch are intended for the repository default branch. They add the published Zenodo software DOI to public-facing metadata and add a GitHub Actions reproducibility smoke-test workflow.

## Files to replace

- `README.md`
- `CITATION.cff`
- `.zenodo.json`
- `codemeta.json`
- `pyproject.toml`
- `DATA_ACCESS.md`
- `REPRODUCIBILITY.md`
- `CHECKSUM_POLICY.md`
- `CHANGELOG.md`
- `REPRODUCTION_CERTIFICATE.md`
- `docs/zenodo_deposit_notes.md`
- `zenodo/zenodo_metadata.json`
- `SHA256SUMS.txt`
- `FILE_MANIFEST.tsv`

## File to add

- `.github/workflows/reproducibility-smoke-test.yml`

## Browser-only update sequence

1. Open the private GitHub repository.
2. Stay on the default branch, normally `main`.
3. Upload or edit the files above, preserving the exact paths.
4. Commit with this message: `Add published Zenodo software DOI and reproducibility workflow`.
5. Do not create a new release unless you want a new Zenodo version.
6. Open the `Actions` tab.
7. Select `Reproducibility smoke test`.
8. Press `Run workflow`.
9. Wait until the workflow is green.

## Expected result

The repository homepage should show the Zenodo software DOI badge, the software DOI, the associated dataset DOI and the private/public repository URL. The workflow should verify the packaged snapshot, run the analysis pipeline and run the tests.
