# Provenance and evidence boundary

The aggregate inputs were derived from a private canonical analysis of 212 completed survey responses. The principal analytical subset contains 172 responses classified by self-reported employee band as micro, small or medium. Thirty-nine completed responses in the 250+ employee band and one completed response with missing employee-band information are retained only in the case-flow record.

The questionnaire was reconstructed from paired exports of the same survey collection: a coded export preserving platform values and a labelled export preserving Romanian wording and human-readable answer labels. No original LimeSurvey definition file has been located. The supplied questionnaire is therefore a verified documentary reconstruction, not the original platform configuration.

The public package begins at the aggregate-count layer. It does not establish that each response represents a unique firm and it does not make the non-probability response set representative of Romanian SMEs. The input contract is defined in `metadata/analysis_contract.json`. The claim-evidence ledger identifies the wording, scope, output and caveat attached to each reported quantity.

## Repository continuity

The repository also contains an earlier release tagged `v1.0.0`. That release documents a superseded article framing and public-data architecture. The `v2.0.0` tree introduced the major rebuild from aggregate inputs but contained a GitHub Actions configuration defect. The present `v2.0.1` tree corrects that workflow without changing the aggregate inputs, analysis or numerical outputs and is the release intended to support the current article. Historical availability must not be interpreted as endorsement of the earlier claims or as permission to restore respondent-level material to the current release.
