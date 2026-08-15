# Study 2 weighted unresolved-row sensitivity protocol

## Status

This protocol was frozen after the corrected primary results had been rendered
but before the distribution of sampling weight among the 986 unresolved rows
was inspected. It is therefore a transparent post-outcome hostile sensitivity,
not a preregistered primary analysis.

## Analytical purpose

The corrected Study 2 analysis uses 20,069 mapped rows and excludes 986 rows
whose `ib9b1`–`ib9b5` state cannot be established. The primary estimates remain
within-source-stratum complete-case weighted rates. IM-R7C asks how far those
rates could move if every unresolved row with a valid positive `base_wt` were
assigned to a negative or positive state.

## Weight notation

For source stratum *s* and definition *d*:

- `D_s` is the positive-weight mass among mapped rows;
- `U_s` is the positive-weight mass among unresolved rows;
- `P_sd` is the positive-weight mass among mapped positive rows.

The frozen marginal bounds are:

```text
lower    = P_sd / (D_s + U_s)
primary  = P_sd / D_s
upper    = (P_sd + U_s) / (D_s + U_s)
width    = U_s / (D_s + U_s)
```

The marginal extrema are intentionally conservative. They are calculated
separately for each definition and are not claimed to be jointly attainable
across nested definitions.

## Coherent scenarios

Four state-coherent extreme assignments are also calculated:

1. all unresolved rows are handwritten;
2. all unresolved rows use standard software, representing a broad-only
   positive assignment;
3. all unresolved rows use specialised software;
4. all unresolved rows use ERP.

These scenarios preserve the nested definition architecture exactly.

## Summaries and diagnostics

The tool reports disclosure-screened source-stratum rates and equal-stratum
summaries. It checks:

- the original corrected aggregate fingerprint;
- lower ≤ complete-case ≤ upper;
- upper − lower = unresolved positive-weight share;
- nested monotonicity in every coherent scenario;
- summary support;
- pairwise ordering determinacy under interval overlap;
- broad-lower versus narrow-upper separation counts.

## Disclosure boundary

The downloadable report contains no microdata rows, identifiers, exact
source-level respondent counts, exact source-level unresolved counts or exact
source-level weight sums. Any definition suppressed in the corrected primary
analysis remains suppressed. The complete report is an internal audit object
and is not a public GitHub or Zenodo artefact.

## Interpretation boundary

Passing the local gate establishes computational validity only. Substantive
interpretation remains blocked until IM-R7D. No global prevalence, causal,
inferential, size-based or standalone country-ranking claim is permitted.

## Frozen identifiers

```text
corrected internal report SHA-256:
020902d6242b2f801cc613de0e1dd0e86fc189a6d6d18b4d1ae8b871791820d0

corrected aggregate fingerprint:
b18fa495616d28bcb315634c6247e2c8c94aa10724759e82cabed19a03251fe0

IM-R7C freeze SHA-256:
b36347ac18c77790a57ae4d1cac3c5917005a31f35030afcf9b68f57f23e09fc
```
