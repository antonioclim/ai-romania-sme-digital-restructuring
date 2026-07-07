# Raw data policy

Raw LimeSurvey exports are intentionally **not** included in this public repository.
The uploaded raw exports contained technical metadata and open-text material that require strict access control and manual disclosure review. The public analysis uses `data/processed/public_quantitative_dataset_no_text_no_direct_identifiers.csv`, produced in survey-data reconstruction by removing direct identifiers, excluding open-text fields and retaining only quantitative variables necessary for reproducible analysis.

For audit purposes, the survey-data reconstruction package records the anonymisation log, questionnaire reconstruction, data dictionary and claims-permission matrix in `data/metadata/`.
