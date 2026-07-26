# Provenance and evidence boundary

The aggregate inputs were derived from a private canonical analysis of 212 completed survey responses. The principal analytical subset contains 172 responses classified by self-reported employee band as micro, small or medium. Thirty-nine completed responses in the 250+ employee band and one completed response with missing employee-band information are retained only in the case-flow record.

The questionnaire was reconstructed from paired exports of the same survey collection: a coded export preserving platform values and a labelled export preserving Romanian wording and human-readable answer labels. No original LimeSurvey definition file has been located. The supplied questionnaire is therefore a verified documentary reconstruction, not the original platform configuration.

The public package begins at the aggregate-count layer. It does not establish that each response represents a unique firm and it does not make the non-probability response set representative of Romanian SMEs. The input contract is defined in `metadata/analysis_contract.json`. The claim-evidence ledger identifies the wording, scope, output and caveat attached to each reported quantity.

## Repository continuity

The repository contains an earlier release tagged `v1.0.0`, which documents a superseded article framing and public-data architecture. Version 2.0.0 introduced the major aggregate-only rebuild but contained a GitHub Actions configuration defect. Version 2.0.1 corrected the workflow and declared the PyYAML test dependency, although its tag was created before the final dependency commit. Version 2.0.2 establishes the aligned repository, tag, source snapshot and release asset without changing the aggregate inputs, analysis or numerical outputs. DOI `10.5281/zenodo.21603732` identifies the current release, while DOI `10.5281/zenodo.21586875` identifies the immediately preceding version. Historical availability must not be interpreted as endorsement of earlier claims or as permission to restore respondent-level material to the current release.
