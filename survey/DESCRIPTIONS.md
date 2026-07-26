# Survey instrument and aggregate response documentation

## 1. Research object and evidential boundary

This directory documents a cross-sectional, online and self-administered survey concerned with reported engagement with artificial intelligence among responses classified by employee band. The accompanying public data are aggregate counts and low-dimensional contingency tables. They support transparent reconstruction of the reported descriptive estimates, figures and exploratory association diagnostics. They do not establish a population frame, a probability sample or a verified register of unique firms. The empirical unit is one completed response. The principal analytical set must therefore be described as 172 *SME-classified responses*, not as 172 independently verified small and medium-sized enterprises.

The analysis is organised around outcome-definition sensitivity. It distinguishes a category reporting active AI use from a heterogeneous project-stage category covering planning, testing or implementation. Those response categories are empirically consequential but are not interchangeable measures of routine operational deployment. Their union is retained as a sensitivity indicator, not as a superior adoption construct. The data support response-set description and exploratory association analysis. They do not support national prevalence estimates, causal effects, firm-level determinants, verified organisational restructuring or claims that a technology has been embedded in routine production.

## 2. Instrument provenance

The instrument was reconstructed from two locked exports of the same survey collection. One export preserves stable platform codes and stored response values. The other preserves Romanian wording and human-readable option labels. The exports contain the same 289 platform attempts, the same 139 columns and the same logical row order. Their representational differences are deterministic: multiple-response selections are encoded as binary values, single-choice answers are encoded as `AOxx` categories and timestamps differ in precision.

No original LimeSurvey definition file in `.lss`, `.lsa`, `.lsq` or `.lsg` format has been located. The questionnaire supplied here is therefore a verified documentary reconstruction from paired exports rather than the original platform definition. Display logic, mandatory status and validation rules are reported only where the exports provide direct evidence.

## 3. Case flow

The source contains 289 platform attempts. A response is classified as complete when a submission timestamp is present and the recorded last page equals 20. Both criteria identify the same 212 rows. Among the completed responses, 36 report 1–9 employees, 57 report 10–49 employees and 79 report 50–249 employees. These 172 rows form the principal SME-classified analytical set. A further 39 completed responses report 250 or more employees and one completed response lacks an employee-band category. Those 40 rows are retained only for case-flow transparency.

The public release does not include any of the 289, 212 or 172 respondent-level extracts. It includes the case-flow counts required to understand the transition between those scopes.

## 4. Questionnaire architecture

The reconstructed instrument contains nine sections and 20 substantive questions. Its 101 substantive source columns comprise 50 structured response fields and 51 narrative or comment fields. The remaining 38 source columns are administrative fields, exact timestamps or timing paradata. None of the administrative fields, timestamps, paradata or narrative responses is included in the public release.

The instrument uses four broad response formats:

1. **Single-choice categorical or ordinal items.** Twelve questions store one `AOxx` code. Some answer sets have an approximate order, but an ordered answer set is not by itself a validated scale.
2. **Multiple-response checklists.** Thirty-eight binary fields indicate whether an option was selected. The source distinguishes `1`, `0` and blank. Blank is not silently converted to zero when a response was incomplete or no value was stored.
3. **Option-linked comments.** Several checklists allow comments associated with an option. A comment is analytically distinct from the corresponding selection flag and cannot substitute for it.
4. **Open-text responses.** Two questions invite broader narrative answers. Such material requires contextual semantic interpretation and disclosure review. It is not public in this release.

The instrument is not described as a validated Likert scale. A Likert-type item is an individual ordered statement-response item, whereas a psychometric scale ordinarily combines several items intended to measure a common latent construct and requires evidence concerning dimensionality and reliability. The present instrument contains categorical, ordinal, multiple-response and narrative items, but it does not demonstrate a validated multi-item latent scale.

## 5. Structured response coding

The variable dictionary records each source code, clean variable name, question, response format, measurement level, stored-value semantics and reporting limitation. Multiple-response fields retain the three-state logic of the source:

- `1` means that the option was selected
- `0` means that the option was not selected where a value was stored
- blank means that no value was stored

Single-choice options are documented through their `AOxx` codes and English semantic labels. This dual representation avoids two opposing errors: replacing the source with an undocumented interpretation and forcing later users to work with opaque codes alone.

## 6. Outcome definitions

The central AI-engagement item contains five categories: no familiarity, slight familiarity, familiarity without organisational use, projects at budgeting, testing or implementation stages and reported active use. The public aggregate inputs support three distinct indicators:

- reported active AI use: 54/172 responses
- project-stage category: 51/172 responses
- active use or project-stage engagement: 105/172 responses

The combined indicator is a sensitivity construction. It shows how the reported result changes when active use is merged with a category containing different stages of organisational engagement. It must not be relabelled as verified adoption, routine deployment or operational integration.

The workforce-preparation item permits a logically tense overlap between one or more positive measures and the statement that no specific measures have yet been introduced. The release therefore preserves a permissive indicator, an overlap count and a conservative indicator that excludes overlapping rows. This approach exposes the response structure instead of resolving it through an unstated coding preference.

## 7. Narrative answers and semantic interpretation

The private source contains 6,669 non-empty narrative or comment cells across all 289 attempts, of which 5,710 occur in completed responses. Narrative material is analytically richer than a fixed response code but it is also more vulnerable to disclosure and interpretive error. A free answer may clarify a selection, qualify it, contradict it, describe an intention rather than an implemented practice or shift between personal experience and an organisational claim.

Open answers must therefore be read in the context of their question and associated structured response. Word frequencies, sentiment scores and keyword hits are not adequate substitutes for semantic interpretation. References to *planning*, *testing*, *piloting*, *implementation* and *active use* require attention to tense, modality, negation and organisational level. Statements such as “we are considering”, “we have budgeted”, “we tested” and “we use routinely” describe different evidential states.

Narrative responses and their translations are not included in this public package. The translation protocol supplied here records the standards that must govern any authorised qualitative use. It requires the source language to be identified at cell level, direct and indirect identifiers to be reviewed before translation and the English rendering to preserve negation, uncertainty and the distinction between intention, experiment and routine use. No analytical category should be assigned solely through automated translation.

## 8. Romanian-language material and documentary translation

All platform attempts opened the Romanian-language survey interface. This establishes the interface language but not the language of every narrative cell because respondents may use English technical expressions, product names, job titles or complete English statements.

The Romanian questionnaire is the source-faithful reconstruction. The English questionnaire is a documentary translation prepared for inspection and reuse. It was not administered to respondents and must not be represented as an independently fielded instrument. Any future publication of translated respondent narratives requires an explicit author verification record. This release does not claim that the private narrative corpus has already been translated or certified.

## 9. Aggregate public data

The `data/aggregate` directory contains only aggregate counts and low-dimensional contingency tables. These files reproduce:

- 212 completed responses and 172 SME-classified analytical responses
- 54 responses reporting active AI use
- 51 responses in the project-stage category
- 105 responses in the combined sensitivity indicator
- 150 responses reporting high implementation costs
- 137 responses reporting lack of technical expertise
- 122 responses selecting both constraints
- 134 responses with at least one positive workforce-preparation measure under the permissive definition
- 13 overlapping responses that also selected “no specific measures”
- 121 responses under the conservative workforce-preparation definition

The employee-band Cramér’s V values reproduced from the contingency counts are 0.134 for active use, 0.350 for the project-stage category, 0.428 for the combined indicator and 0.503 for workforce preparation.

Reproduction of these values does not remove the measurement limitations. A correctly reproduced statistic may still depend on a heterogeneous category, a non-probability response set or an ambiguous item. Reproducibility is a condition of transparent inquiry, not a guarantee of construct validity or external validity.

## 10. Missing values

Missingness is not silently imputed. Within incomplete attempts, a blank checklist field may indicate that the question was not reached, that no value was stored or that no response was provided. It should not automatically be interpreted as an explicit non-selection. The reported analysis uses completed responses and the documented employee-band classification.

## 11. Public and controlled-access boundary

This public release contains the questionnaire, dictionaries, coding documentation, aggregate inputs, analysis code, generated tables, figure-source data and figures. It contains no respondent-level rows, native response identifiers, replacement response identifiers, IP addresses, exact timestamps, paradata, open-text responses or editorial correspondence.

Removal of direct identifiers did not make the full structured profiles suitable for unrestricted distribution. Combinations of employee band, sector, role, AI engagement and other responses leave many rows highly distinctive, while narrative answers increase linkage and singling-out risk. Respondent-level material is therefore maintained separately under controlled handling. It must not be reconstructed from historical public surfaces or redistributed through this repository.

## 12. Reuse and citation

Reuse should preserve the distinction between a completed response and a verified firm, between an employee-band classification and a full legal SME classification and between reported engagement categories and observed operational deployment. Derived claims should be traced to the aggregate input and canonical output named in the claim-evidence ledger.

Version 2.0.2 is identified by DOI `10.5281/zenodo.21603732`. Cite the versioned software release and cite the associated article separately when it becomes available.
