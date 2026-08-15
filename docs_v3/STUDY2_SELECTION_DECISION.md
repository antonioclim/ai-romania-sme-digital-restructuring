# Study 2 selection decision

## Decision status

```text
Phase:                   IM-R5
Decision date:           15 August 2026
Selection status:        FROZEN BEFORE MICRODATA ACQUISITION
Selected candidate:      World Bank FAT production-planning MOST-used method
Dataset reference:       WLD_2019-2023_FAT_v01_M
Dataset DOI:             https://doi.org/10.48529/assd-3j65
ODSA outcomes inspected: no
Microdata acquired:      no
Replication executed:    no
```

## Decision

The independent replication source is conditionally fixed as the World Bank
*Technology Sophistication Across Establishments* pooled Firm Adoption of
Technology dataset. Study 2 will examine the most-used production-planning
method if the structural acquisition gate passes.

Selection used source metadata, documentation, access terms and state
architecture. No Study 2 level, composition, association or ranking result was
calculated or inspected.

## Rationale

The selected source provides:

- an establishment-level unit independent of Study 1;
- a different technology context;
- a finite most-used-method state register;
- nested definitions that do not require a latent maturity scale;
- employment size and country descriptors;
- a large versioned multi-country record;
- a questionnaire, dictionary and implementation documentation;
- persistent identifiers for the dataset and official reproducibility package.

The United States Census 2018 Annual Business Survey technology tables are
Reserve 1. Eurostat's Digital Intensity Index is Reserve 2. The reserve order
was fixed before Study 2 outcome inspection.

## Locked state register

```text
handwritten_processes
standard_software
mobile_apps_or_digital_platforms
specialised_software
erp
other
```

The source-field priority is:

1. use a documented direct categorical `b9b` field if it exists in the acquired
   pooled file;
2. otherwise use only a complete documented pooled MOST-used indicator family
   that passes a one-state-per-valid-row invariant;
3. never reconstruct the most-used state from adopted-any indicators
   `db9a1` to `db9a5`;
4. never switch business function after viewing results.

The primary denominator contains categories 1–5. `other`, missing,
don't-know, not-applicable and structurally ineligible records are excluded and
reported separately.

## Locked definitions

```text
integrated_planning
    = {erp}

specialised_planning
    = {specialised_software, erp}

digitally_enabled_planning
    = {standard_software, mobile_apps_or_digital_platforms,
       specialised_software, erp}
```

The definitions are nested and answer different questions. The broadest
definition does not support claims that every positive establishment uses
specialised software, ERP or an integrated architecture.

## Descriptor and weighting policy

Employment size is derived from `e1`:

```text
small:   5–19 workers
medium: 20–99 workers
large:  100 or more workers
```

Country is a secondary synthesis dimension. The primary analysis will be
country-specific and use `base_wt` where documented and valid. The article
will not report one naïve pooled world-prevalence estimate. Cross-country
synthesis will use the number of eligible countries, median, interquartile
range, minimum, maximum and counts of association or ranking patterns.

## Structural acquisition gate

Analysis may begin only if:

```text
G1  The record matches WLD_2019-2023_FAT_v01_M.
G2  Version and checksum are recorded.
G3  country, e1 and base_wt are present and interpretable.
G4  A direct b9b field or complete documented MOST-used equivalent exists.
G5  Valid rows map to exactly one locked state.
G6  Mapping failures are no more than 0.5% of otherwise eligible rows.
G7  The primary denominator contains at least 5,000 establishments.
G8  At least 10 countries contain at least 100 valid cases.
G9  Labels match the official questionnaire and dictionary.
G10 Public reproducibility does not require source-data redistribution.
```

If the gate fails, no ODSA outcomes are calculated. The failure is recorded
and Reserve 1 is assessed.

## Reuse and ethics boundary

The source requires registration and acceptance of the World Bank Microdata
Library terms. Source microdata will not be committed to GitHub or deposited
in Zenodo. The public workflow will contain source identifiers, acquisition
instructions, transformation code, derived aggregates and tests.

Study 2 secondary-use documentation must address the anonymised public-
distribution status, access conditions, absence of re-identification,
aggregate reporting and any applicable institutional requirement. Study 2
cannot be used to alter the documented ethics status of Study 1.

## Prohibited claims

Before locked replication, do not claim:

- any production-planning state frequency;
- global technology prevalence;
- a causal firm-size effect;
- that ERP is universally best;
- that the FAT countries represent all countries;
- that an unweighted pooled estimate is a population estimate;
- that public access permits redistribution;
- that Study 2 confirms ODSA.

The selected source will be retained if the structural gate passes even when
ODSA sensitivity is negligible. It will not be replaced for producing an
unfavourable or uninteresting pattern.

## Gate

```text
Candidate search:            complete
Candidate scoring:           complete
Selected source:             frozen conditionally
Outcome inspection:          none
Structural acquisition gate: pending
Replication:                 not started
IM-R5 gate:                  GO
Submission gate:             NO-GO
```
