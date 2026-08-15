# IM-R7A failed-run audit and corrective implementation amendment 01

## Status

The first IM-R7A execution is **quarantined**. Its report has SHA-256:

```text
c2331d544a131d414736aa049ba13fbce723b56c3889030ef2fb069ea9c777ae
```

The execution passed E1–E3 and E5–E12 but failed E4. It mapped the expected
20,069 complete one-hot rows, yet reported the remaining 986 rows as invalid
rather than unresolved or structurally missing.

The prior structural gate had already established:

```text
mapped complete one-hot rows:        20,069
mapping failures:                    0
unmapped or structurally missing:       986
```

## Root cause

The first browser tool parsed a missing or special value as `status=missing`,
then applied a pre-classification test that treated every status other than
`valid` as invalid. The classifier therefore never reached the unresolved-row
branch for rows containing missing one-hot fields.

This is an implementation defect in the **classification metadata and E4
gate**, not evidence of corrupted source data.

## Outcome-exposure safeguard

Aggregate outcome values were rendered during the failed run. Therefore this
correction is not presented as pre-outcome. No scientific choice may change
after that exposure.

The following remain exactly unchanged:

- source fields;
- three positive-state definitions;
- common mapped denominator membership;
- source strata;
- weighting;
- estimands;
- quantile method;
- suppression thresholds;
- prohibited size and pooled-global analyses;
- claim boundaries.

## Corrected classifier

The corrected runner distinguishes:

1. complete one-hot mapping;
2. all-zero unresolved rows;
3. structurally missing unresolved rows;
4. one positive plus missing fields, which remains ambiguous and excluded;
5. multiple-positive rows;
6. non-missing non-binary invalid rows.

The corrected E4 gate requires:

```text
mapped:                       20,069
unresolved total:                986
ambiguous positive+missing:        0
multiple-positive:                 0
invalid non-binary:                0
```

## Non-substantive result fingerprint

The failed run's aggregate-only sections were canonicalised and hashed:

```text
b18fa495616d28bcb315634c6247e2c8c94aa10724759e82cabed19a03251fe0
```

The corrected tool adds E13. It must reproduce this fingerprint exactly.
Consequently, the rerun cannot silently alter any source-stratum result,
cross-stratum synthesis, order diagnostic, weighting-sensitivity result or
claim boundary.

## Freeze and amendment hashes

```text
original outcome-analysis freeze:
2491149bcc41596d8dbb9e509ee731447da70100de380d909daf45a4c46603be

implementation amendment 01:
03244a3761052b294ab122999ff061b8f5932b4332b2ad7bd713e5f2f255e1ef

effective corrected contract:
f096825efd95c0afc699410d174517e3797ee4610b8a392c5809bdfd20789d87
```

## Decision

The first report is invalid for interpretation, release and manuscript use.
Only a corrected E1–E13 PASS report may proceed to IM-R7B.
