# Response coding guide

## Paired source representations

The reconstructed instrument is based on two aligned representations of the same collection. The coded representation preserves stable platform codes, binary option flags and `AOxx` single-choice values. The labelled representation preserves the Romanian wording and human-readable option labels. Neither raw export is included in the public release.

## Case flow

The source contains 289 platform attempts, 212 completed responses and 172 completed responses in the 1–249 employee bands. The reported analysis uses the 172 SME-classified responses. The 39 completed responses in the 250+ band and the one completed response without employee-band information are retained only for case-flow transparency.

## Multiple-response fields

Multiple-response options preserve three states: `1` for selected, `0` for not selected where a value was stored and blank when no value was stored. A blank value in an incomplete attempt must not be silently interpreted as an explicit non-selection.

## Single-choice fields

Single-choice items retain their platform category codes and documented English meanings. The codes are source values. The English labels are documentary interpretations, not newly observed responses.

## AI-engagement outcomes

- reported active AI use: the active-use category only
- project-stage category: the category combining budgeting, testing or implementation
- combined indicator: active use or project-stage engagement

The combined indicator is a sensitivity construction. It is not a verified measure of routine deployment.

## Workforce-preparation sensitivity

The questionnaire permits simultaneous selection of one or more positive preparation measures and “no specific measures”. The permissive indicator retains those overlapping responses, while the conservative indicator excludes them. The overlap is reported rather than resolved through an undocumented coding preference.

## Narrative fields

Option-linked comments and open-text responses are not included in the public release. Any authorised qualitative use requires question-specific semantic review, disclosure control, language identification and documented translation where needed.
