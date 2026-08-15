# Study 2 `s1b` dictionary review and final decision

## Decision

The candidate mapping

```text
1 → small sampling-frame size stratum
2 → medium sampling-frame size stratum
3 → large sampling-frame size stratum
```

is **rejected for the current Study 2 analysis**.

All Study 2 size-based diagnostics are disabled before any production-planning outcome is inspected.

## Evidence reviewed

### Local non-outcome audit

The local audit used only `country`, `s1b`, `s7` and `e1`. It did not read an outcome field. Codes 1, 2 and 3 were complete, no invalid code was found and no source-stratum median-order reversal was detected against either `s7` or `e1`.

These findings establish structural plausibility but not semantic value labels.

### Official pooled Data Dictionary XLSX

```text
file: data_dictionary_fat_qje_final.xlsx
size: 114,881 bytes
SHA-256: bf26b87b4801f4f6e64df90bcc7a2738f3c674683b2b3b2045ef0410b59af8ac
```

The workbook contains two sheets:

1. `Data Dictionary`
2. `Categorical variables_ polan`

The main sheet documents `s7` as `Number of workers (screener)` but contains no row for `s1b` and no occurrence of `Sampling size`. The Poland-specific categorical sheet documents `s7` categories but also contains no `s1b` row. A raw OOXML search likewise found no occurrence of `s1b` or `Sampling size`.

The online pooled catalogue identifies `s1b` only by the label `Sampling size`. Neither the catalogue page nor the official XLSX supplies value labels for codes 1, 2 and 3.

## Hostile methodological interpretation

High agreement with a worker-count field cannot create an official semantic label. The same code order could represent harmonised broad size strata, country-specific collapsed frame strata or another derived sampling classification. Accepting the candidate labels would therefore depend on an unstated assumption.

The prespecified IM-R6D rule required explicit official value labels. That condition failed after external review. The correct consequence is to disable the diagnostic, not to weaken the rule.

## Frozen consequences

- `s1b` is not used as a numeric worker count.
- `s1b` is not used as a categorical size descriptor.
- `s7` remains disabled as a cross-source primary numeric descriptor.
- `e1` is not restored as a primary or secondary size analysis.
- No size-band rates, size-based Cramér's V or size-effect claims are produced.
- No threshold is relaxed and no label is changed after outcomes are viewed.
- The local audit remains valuable as provenance and a falsification check.

## Study 2 scope retained

Study 2 proceeds without a size variable. The next specification may include:

- weighted and unweighted outcome-definition levels within source stratum;
- positive-class composition;
- exact contrasts between the frozen definitions;
- source-stratum ordering and ordering changes across definitions;
- cross-stratum descriptive synthesis without a pooled global prevalence.

## Freeze

```text
decision file:
examples/study2_fat_production_planning/s1b_final_decision.yml

SHA-256:
b2a89a389ea24508c40a1ea4d08577c0393fce170129557c708487866ac6a09b
```

No production-planning outcome was inspected before this decision.
