# Release notes — version 2.0.1

Version 2.0.1 is the corrected current release of the privacy-preserving reproducibility package associated with the analysis of reported AI engagement among Romanian SME-classified responses.

## Patch correction

Version 2.0.1 corrects the GitHub Actions configuration included in version 2.0.0. The earlier workflow used the `runner` context inside `jobs.<job_id>.env`, where that context is not available during workflow validation. The corrected workflow uses `/tmp/matplotlib` on the declared Ubuntu runner and adds a regression test for this condition.

The same patch declares `PyYAML==6.0.3` in every supported environment specification because the release-integrity test parses the CFF citation metadata. This resolves the CI collection failure caused by an undeclared test dependency.

The correction does not alter the aggregate inputs, analytical definitions, generated tables, figures, questionnaire documentation or reported numerical results.

## Relationship to earlier releases

- `v1.0.0` belongs to the superseded article framing and public-data architecture and is retained only as historical provenance.
- `v2.0.0` introduced the aggregate-only rebuild but is superseded by `v2.0.1` because of the workflow configuration defect.
- `v2.0.1` is the release to cite and archive for the current analysis.

## What is included

- aggregate counts and low-dimensional contingency tables
- deterministic analysis and validation code
- generated tables, figure-source data and figures
- the reconstructed Romanian questionnaire
- a British-English documentary translation of the questionnaire
- question, response-option and variable dictionaries
- coding, translation and semantic-review protocols
- a claim-evidence ledger and explicit inferential limits
- versioned citation metadata for DOI `10.5281/zenodo.21586875`

## What is not included

- respondent-level rows
- open-text answers or translations of those answers
- direct or replacement response identifiers
- IP addresses, precise timestamps or paradata
- raw platform exports
- editorial correspondence or private governance material

The empirical unit is one completed response. The release does not support national-prevalence, causal, firm-level determinant or verified-deployment claims.
