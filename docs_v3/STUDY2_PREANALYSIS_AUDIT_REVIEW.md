# Study 2 pre-analysis audit review

## Scope and confidentiality boundary

The authorised user executed the IM-R6C browser-only audit on the unmodified
World Bank pooled file `fat0_raw_data_qje.csv`. The resulting report was
produced locally, no network upload was performed and the tool read only
`country`, `s1b`, `s7`, `e1` and `base_wt`. No production-planning technology
field, state-specific outcome count, ODSA rate, association or country-level
technology outcome was read or calculated.

## Verified file and source identity

```text
reference ID: WLD_2019-2023_FAT_v01_M
DOI:          10.48529/assd-3j65
file:         fat0_raw_data_qje.csv
size:         19,633,172 bytes
SHA-256:      f61a2c6e09f4763818ae1d4db8b330e97bffd8bb0824c2d833b79d728152bd17
CRC-32:       4418a02b
rows:         21,055
columns:      723
```

The local report itself has SHA-256
`f1a2197a8a60e37ffa6664f3e512beea448c875ddc9c86d60cadda1fa5250e8f`.

## Mechanical decision

Ten of the eleven frozen pre-analysis gates passed. The failed gate is P7:

```text
criterion: at most 1% of valid s7 values are below five
observed:  1,538 / 21,055 = 7.305%
status:    FAIL
```

Under the prespecified rule, the primary numeric employee-size descriptor is
therefore disabled. The threshold must not be relaxed after seeing the audit.
No technology outcome had been inspected when this decision was made.

## Why the P7 failure is substantive

The World Bank FAT collection defines its target population as formal firms
with five or more employees and documents firm-size strata of 5–19, 20–99 and
100 or more employees. Nevertheless, the below-five `s7` values are strongly
concentrated in a small number of source strata:

```text
Poland:    1,172
Cambodia:    265
Kenya:        93
Georgia:       7
Ghana:         1
Total:     1,538
```

This pattern is incompatible with treating pooled `s7` as an unquestionably
harmonised numeric worker count across all sixteen source strata. The present
evidence does not establish whether the concentration reflects disclosure
transformation, country-specific coding, frame deviations or another
source-specific processing rule. The analysis must therefore not repair,
recode or exclude these values by assumption.

## The other size fields do not provide an automatic fallback

### `e1`

`e1` is available for only 13,399 rows and is absent for 7,656 rows. It is
entirely unavailable in Bangladesh, the first India source stratum, Senegal and
Viet Nam, and is sparse in Brazil and Chile. It must not be promoted to the
primary cross-source-stratum descriptor after `s7` failed. A restricted
complete-case sensitivity remains conceptually possible, but it cannot be
presented as a full fifteen-country replication.

### `s1b`

`s1b` is complete and has the observed codes 1, 2 and 3. The source describes
it as `Sampling size`, while the FAT collection documents small, medium and
large sampling strata. This makes `s1b` a plausible candidate for a categorical
**sampling-frame size-stratum** audit, not a numeric worker-count substitute.

It is not authorised automatically. Before any outcome is inspected, IM-R6D
must verify from official documentation that the pooled codes map consistently
to the documented small, medium and large strata and must audit whether the
mapping is invariant across all source strata. If that verification fails,
all size-based Study 2 results remain disabled.

## Source-stratum decision

The file contains sixteen source labels representing fifteen documented
countries. `India` and `India_Wave2_New` remain separate analytical source
strata and map to one reporting country. No primary India merge is permitted.

## Weight decision

`base_wt` is positive and numeric for 21,054 rows and missing for one. This
supports within-source-stratum weighted descriptive estimates after the final
analysis freeze. It does not authorise a pooled global prevalence or a pooled
cross-country association.

## Current gate

```text
IM-R6C local audit:                  COMPLETE
s7 primary numeric descriptor:       DISABLED
s7 threshold amendment:              PROHIBITED
e1 promotion to primary descriptor:  PROHIBITED
s1b categorical descriptor:          PENDING OFFICIAL LABEL AUDIT
Study 2 outcome calculation:         NO-GO
Information & Management submission: NO-GO
```

## Next phase

IM-R6D will perform an official-documentation and non-outcome harmonisation
audit of `s1b`. It may end in one of two locked decisions:

1. `s1b` accepted only as a categorical sampling-frame size stratum, with
   explicit language that it is not a current measured employee count; or
2. all size-based Study 2 diagnostics disabled, with source-stratum level and
   definition-sensitivity analyses retained.

No technology outcome may be calculated until that decision is frozen and
hash-locked.
