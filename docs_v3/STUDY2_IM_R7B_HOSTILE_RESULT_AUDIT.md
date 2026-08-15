# IM-R7B — hostile result and disclosure audit

## Verdict

```text
Corrected execution E1–E13:                 PASS
Protected payload equals quarantined run:   PASS
Source-level arithmetic:                    PASS
Cross-stratum summaries:                    PASS
Pairwise reversal counts:                   PASS
Weighting-sensitivity summaries:            PASS
Single-file suppression contract:           PASS
Internal corrected result:                  GO
Full internal JSON for public release:      NO-GO
Public hardened summary:                    GO
Manuscript integration:                     CONDITIONAL GO
Submission:                                 NO-GO
Next phase:                                 IM-R7C
```

## 1. Provenance and correction integrity

The corrected report has SHA-256:

```text
020902d6242b2f801cc613de0e1dd0e86fc189a6d6d18b4d1ae8b871791820d0
```

All E1–E13 gates pass. The protected aggregate sections are exactly identical
to the quarantined first run, with fingerprint:

```text
b18fa495616d28bcb315634c6247e2c8c94aa10724759e82cabed19a03251fe0
```

The correction therefore changed the excluded-row taxonomy only. It did not
change any substantive result.

## 2. Main empirical result

Across the eligible source strata, the weighted median levels are:

```text
ERP as most-used method:                         3.78%
specialised software or ERP:                   10.66%
computer- or platform-enabled rather than
handwritten:                                    73.22%
```

The median weighted contrasts are:

```text
integrated → specialised:                        8.14 percentage points
specialised → digitally enabled:                50.97 percentage points
integrated → digitally enabled:                 68.94 percentage points
```

The result is not a global prevalence estimate. It is the distribution of
source-stratum estimates.

## 3. Positive-class composition

For the specialised definition, the median weighted positive class contains:

```text
specialised software:                           72.65%
ERP:                                            27.35%
```

For the broad digitally enabled definition, the median weighted positive
class contains:

```text
standard software:                              78.13%
mobile apps or digital platforms:                2.31%
specialised software:                           14.75%
ERP:                                             4.80%
```

Thus the broad category is principally a standard-software category in the
median eligible stratum. It must not be described as integrated or advanced
planning.

## 4. Ordering sensitivity

Under the frozen exact-order rule, weighted strict reversals affect:

```text
integrated → specialised:                       21/91 pairs  = 23.08%
specialised → digitally enabled:                31/120 pairs = 25.83%
integrated → digitally enabled:                 33/91 pairs  = 36.26%
```

A post hoc hostile check treating differences of at most one percentage point
as practical ties still leaves:

```text
integrated → specialised:                       15 strict reversals
specialised → digitally enabled:                27 strict reversals
integrated → digitally enabled:                 26 strict reversals
```

The ranking-sensitivity conclusion is therefore not an artefact of
machine-precision tie handling. The practical-tie check is an audit
sensitivity, not a replacement for the frozen estimator.

## 5. Weighting sensitivity

The median weighted-minus-unweighted differences are:

```text
integrated planning:                            −1.54 percentage points
specialised planning:                           −2.40 percentage points
digitally enabled planning:                     −0.36 percentage points
```

The maximum absolute source-stratum differences reach approximately 13–15
percentage points. Weighting is therefore not ignorable, even though the
cross-stratum broad-definition medians are similar.

## 6. Missingness and denominator risk

The common mapped denominator is 20,069 from 21,055 rows. The 986 unresolved
rows represent 4.68% overall, and the unresolved share
reaches 16.18% in the most affected source stratum.

An aggregate-only worst-case audit assigns every unresolved row as negative or
positive. Even under that deliberately extreme check:

```text
broad lower bound > strict upper bound:          16/16 source strata
broad lower bound > middle upper bound:          16/16 source strata
middle lower bound > strict upper bound:         13/16 source strata
```

This strongly protects the broad-versus-narrow finding. It does not replace a
weighted missingness sensitivity, which remains mandatory in IM-R7C.

## 7. Disclosure audit

The internal JSON passes its own suppression rules. However, an ecosystem-level
audit found that combining exact source totals from the pre-analysis record
with exact mapped denominators from the result report can recover excluded-row
cells of size 1–4 in 2 source strata.

Therefore:

- the full corrected JSON remains private and authoritative;
- it must not be committed to the public repository or Zenodo;
- the public summary omits source-level mapped denominators, respondent counts,
  excluded-status counts and full ranking arrays;
- only the hardened cross-stratum summary may be released.

## 8. Additional hostile observations

1. The total-variation measures are mathematically linked to the added-state
   composition under nested definitions. They are useful summaries but not
   independent validation statistics.
2. The ranking arrays in the internal report use different eligible sets when
   the strict ERP outcome is suppressed. Pairwise reversal counts are valid,
   but full ranking arrays should not appear in the article or public output.
3. Source strata are not interchangeable with countries. The two India waves
   remain separate.
4. No design-based confidence intervals or p-values are available. The results
   are descriptive and must remain so.
5. Study 2 generalises the measurement argument to production planning; it
   does not estimate Romanian AI adoption and cannot be pooled with Study 1.

## Final decision

The corrected Study 2 result is scientifically usable as an independent,
descriptive replication of outcome-definition sensitivity. Before manuscript
integration, IM-R7C must provide a frozen weighted missingness sensitivity for
the 986 unresolved rows.
