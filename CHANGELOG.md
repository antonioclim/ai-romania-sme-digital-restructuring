# Changelog

## 2.0.1

- Corrected the GitHub Actions workflow by replacing an unsupported job-level `${{ runner.temp }}` expression with the fixed `/tmp/matplotlib` path on the declared Ubuntu runner.
- Added an integrity test that rejects reintroduction of the unsupported expression.
- Preserved all aggregate inputs, analytical definitions, generated tables, figures, questionnaire documentation and inferential limits from version 2.0.0.
- Retained DOI `10.5281/zenodo.21586875` for the corrected version prepared before publication of the Zenodo record.

## 2.0.0

- Established version 2.0.0 as the major privacy-preserving rebuild in the existing repository, while treating version 1.0.0 as historical provenance rather than current analytical evidence.
- Rebuilt the public research-software package from aggregate counts and low-dimensional contingency tables.
- Removed respondent-level records from the public release architecture.
- Reframed the analytical contract around outcome-definition sensitivity.
- Preserved the 250+ employee band only for case-flow transparency.
- Limited the association family to four question-linked diagnostics.
- Added the reconstructed Romanian questionnaire, a British-English documentary translation, response-option metadata and a full variable dictionary.
- Added a public explanation of free-text semantics, translation requirements and the public-controlled data boundary.
- Added DOI-aware citation and software metadata for `10.5281/zenodo.21586875`.
- Added deterministic source, output and full-manifest integrity checks.
- Added a fail-closed audit that rejects respondent-level files, hidden document comments, revision markup, local paths and release-workflow debris.
