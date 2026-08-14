# Ethics, consent and data-governance boundary

## Study 1

The Romanian organisational AI example is based on responses to an open, voluntary LimeSurvey questionnaire. Before accessing the questions, prospective respondents saw an information page describing the academic purpose, the intended processing and publication of resulting data, the treatment of responses as anonymous, applicable GDPR protection and completion-based consent.

No formal prospective ethics committee review was conducted for the original collection. The software and this development branch do not claim approval, exemption, waiver or retrospective ethics status. Any journal-facing statement must use the exact conclusion and reference supplied by the responsible institution, if and when one is obtained.

## Public evidence boundary

The version 3 public workflow is aggregate-only. It must not contain:

- respondent-level rows;
- direct or replacement response identifiers;
- free-text responses or translations of those responses;
- IP addresses;
- precise timestamps;
- paradata;
- raw platform exports;
- private ethics, DPO or editorial correspondence.

Study 1 begins at the aggregate-count layer. It permits verification of registered counts, levels, compositions and low-dimensional association diagnostics. It does not permit independent respondent-level recoding, duplicate adjudication or linkage to unique organisations.

## New empirical work

Any new study involving human participants, including a managerial vignette or decision experiment, must obtain prospective institutional review or a documented formal determination that review is not required before recruitment begins. Consent materials, data-minimisation measures, retention periods and sharing boundaries must be fixed before collection.

## Release rule

A successful computational build does not constitute ethical approval. The final release gate therefore separates:

1. code and output integrity;
2. privacy and disclosure-boundary integrity;
3. institutional ethics status;
4. journal-specific reporting compliance.
