# Branch status — `im-v3.0.0-rc1`

This branch is the active development branch for Outcome-Definition
Sensitivity Analysis version `3.0.0-rc1`.

## Current phase

IM-R7D is complete. The weighted unresolved-row sensitivity passed M1–M14 and
the hostile audit independently reproduced the bounds, cross-stratum
summaries, robust-separation counts and interval-ordering determinacy.

The complete IM-R7C report remains private. A hardened cross-stratum-only
public summary is registered.

IM-R8 manuscript integration is open.

## Study 2 status

```text
authoritative IM-R7C report SHA-256: be55bcbe804768136abe18ef64aa87df6267d9b7dfd4271a2a989711f7f1c9f3
IM-R7C M1–M14:                      PASS
primary aggregate fingerprint:       b18fa495616d28bcb315634c6247e2c8c94aa10724759e82cabed19a03251fe0
mapped common denominator:           20,069
unresolved rows:                         986
source strata / countries:           16 / 15
median unresolved-weight share:      4.16%
maximum unresolved-weight share:     19.08%
broad > specialised robust strata:   15 / 16
broad > ERP robust strata:           13 / 14
specialised > ERP robust strata:      9 / 14
internal weighted sensitivity:       GO
full internal JSON public release:   NO-GO
public weighted summary SHA-256:     a78301a4d75adbb462bd7d9a596eefac8a5c6ef81d1fff99c254f32de08c845c
public weighted contract SHA-256:    4dd2e4540d3e8609beb4e4929bf6dc9a27a87f920d35517e2004a254faa8c4c4
manuscript integration:              GO WITH CONDITIONS
submission gate:                     NO-GO
```

## Interpretation boundary

- the complete-case result remains primary;
- weighted bounds are deterministic worst-case assignment bounds, not
  confidence intervals;
- marginal extrema are not jointly attainable across definitions;
- joint cross-definition interpretation uses only coherent scenarios;
- no global prevalence, causal effect or standalone country ranking;
- the complete IM-R7C JSON is not a public or supplementary artefact.

## Open gates

- IM-R8 Information & Management manuscript integration;
- article–code–table–figure parity;
- final GitHub and Zenodo release audit;
- Elsevier submission preflight.

## Isolation

- default branch `main`: unchanged;
- final tag `v3.0.0`: not created;
- final GitHub release and Zenodo version: not created;
- no World Bank source microdata are present in the repository.
