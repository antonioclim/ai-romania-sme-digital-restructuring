# Release notes — version 2.0.2

Version 2.0.2 is the current aligned release of the privacy-preserving reproducibility package associated with the analysis of reported AI engagement among Romanian SME-classified responses.

## Release-integrity correction

Version 2.0.1 corrected the GitHub Actions workflow and declared the PyYAML dependency required by the release-integrity tests. The final dependency declaration was committed after the `v2.0.1` tag had already been created. Consequently, the branch and attached release asset were correct, but GitHub's automatic source archives for that tag did not contain the final dependency declaration.

Version 2.0.2 creates a new, immutable alignment point in which the repository state, tag snapshot, automatic source archives and attached release asset contain the same tested files. The correction does not alter the aggregate inputs, analytical definitions, generated tables, figures, questionnaire documentation or reported numerical results.

## Version lineage

- `v1.0.0` belongs to the superseded article framing and public-data architecture and is retained only as historical provenance.
- `v2.0.0` introduced the aggregate-only rebuild but contained an invalid GitHub Actions expression.
- `v2.0.1` corrected the workflow and dependency declaration, but its tag preceded the final dependency commit.
- `v2.0.2` is the release to cite and archive for the current analysis.

## What is included

- aggregate counts and low-dimensional contingency tables
- deterministic analysis and validation code
- generated tables, figure-source data and figures
- the reconstructed Romanian questionnaire
- a British-English documentary translation of the questionnaire
- question, response-option and variable dictionaries
- coding, translation and semantic-review protocols
- a claim-evidence ledger and explicit inferential limits
- versioned citation metadata for DOI `10.5281/zenodo.21603732`

## What is not included

- respondent-level rows
- open-text answers or translations of those answers
- direct or replacement response identifiers
- IP addresses, precise timestamps or paradata
- raw platform exports
- editorial correspondence or private governance material

The empirical unit is one completed response. The release does not support national-prevalence, causal, firm-level determinant or verified-deployment claims.
