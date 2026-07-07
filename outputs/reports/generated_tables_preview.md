# Generated table index

## Key recomputed values

| metric                          |   value |
|:--------------------------------|--------:|
| full_completed_n                |   212   |
| sme_only_n                      |   172   |
| large_comparator_n              |    39   |
| unknown_firm_size_n             |     1   |
| full_active_ai_use_n            |    73   |
| full_active_ai_use_percent      |    34.4 |
| sme_active_ai_use_n             |    54   |
| sme_active_ai_use_percent       |    31.4 |
| full_active_or_planning_percent |    64.6 |
| sme_active_or_planning_percent  |    61   |


## Exploratory association tests

| test_label                                      | row_variable                         | column_variable                    |   n |   rows |   columns |   chi_square |   df |   p_value |   cramers_v |   min_expected | method_note                                                                                                               |
|:------------------------------------------------|:-------------------------------------|:-----------------------------------|----:|-------:|----------:|-------------:|-----:|----------:|------------:|---------------:|:--------------------------------------------------------------------------------------------------------------------------|
| Active AI use by firm size, full sample         | firm_size_category                   | adoption_binary_active             | 211 |      4 |         2 |       7.1549 |    3 |  0.06712  |      0.1841 |        12.455  | chi-square; exploratory; no causal inference; p-value computed from chi-square survival function without scipy dependency |
| Active or planning AI by firm size, full sample | firm_size_category                   | adoption_binary_active_or_planning | 211 |      4 |         2 |      37.4446 |    3 |  0        |      0.4213 |        12.7962 | chi-square; exploratory; no causal inference; p-value computed from chi-square survival function without scipy dependency |
| Active AI use by SME size strata                | firm_size_category                   | adoption_binary_active             | 172 |      3 |         2 |       3.0875 |    2 |  0.213579 |      0.134  |        11.3023 | chi-square; exploratory; no causal inference; p-value computed from chi-square survival function without scipy dependency |
| Active AI use by any upskilling measure         | has_any_upskilling_measure           | adoption_binary_active             | 212 |      2 |         2 |       8.2475 |    1 |  0.004081 |      0.1972 |        13.7736 | chi-square; exploratory; no causal inference; p-value computed from chi-square survival function without scipy dependency |
| Active AI use by stricter-regulation support    | governance_support_strict_regulation | adoption_binary_active             | 212 |      2 |         2 |       0.3817 |    1 |  0.536685 |      0.0424 |        22.0377 | chi-square; exploratory; no causal inference; p-value computed from chi-square survival function without scipy dependency |
| Active AI use: SME versus large comparator      | sme_vs_large                         | adoption_binary_active             | 211 |      2 |         2 |     nan      |  nan |  0.061058 |      0.1414 |       nan      | Fisher exact odds ratio=2.0759; exploratory; no causal inference; exact p-value computed by hypergeometric enumeration    |