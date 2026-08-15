# Branch status — `im-v3.0.0-rc1`

This branch is the active development branch for Outcome-Definition
Sensitivity Analysis version `3.0.0-rc1`.

## Current phase

IM-R7B is complete. The corrected Study 2 execution passed E1–E13 and the
hostile result audit validated the internal result. A hardened cross-stratum
public summary is registered, while the complete internal corrected report
remains private because of complementary disclosure risk.

IM-R7C is open. Its post-outcome weighted unresolved-row sensitivity was frozen
before the distribution of `base_wt` among the 986 unresolved rows was
inspected. Local browser-only execution is pending.

## Study 2 status

```text
corrected internal report SHA-256: 020902d6242b2f801cc613de0e1dd0e86fc189a6d6d18b4d1ae8b871791820d0
corrected aggregate fingerprint:   b18fa495616d28bcb315634c6247e2c8c94aa10724759e82cabed19a03251fe0
corrected E1–E13:                  PASS
IM-R7B internal result gate:       GO
full internal JSON public release: NO-GO
R7B public summary SHA-256:        f656b1049d5e21e9a950ddb6bdcfe748ce06671e84d72aa979f1b58599d1aad3
R7B public contract SHA-256:       bb9fd7f65b9323c76c7362a4d4c39a24500d1ac1e97ee90b0dcda93c4a6ca018
IM-R7C freeze SHA-256:             b36347ac18c77790a57ae4d1cac3c5917005a31f35030afcf9b68f57f23e09fc
IM-R7C browser execution:          PENDING USER
manuscript integration:            NO-GO pending IM-R7D
submission gate:                   NO-GO
```

## Frozen IM-R7C sensitivity

Within each source stratum, let `D` be mapped positive-weight mass, `U` be
unresolved positive-weight mass and `P` be mapped positive weight for the
outcome definition.

```text
lower    = P / (D + U)
primary  = P / D
upper    = (P + U) / (D + U)
width    = U / (D + U)
```

Four coherent assignments are retained: all handwritten, all broad-only, all
specialised and all ERP. The corrected complete-case analysis remains primary.

## Public-data boundary

- no World Bank microdata are present in the repository;
- the complete corrected IM-R7A-C1 report is not public;
- the complete IM-R7C sensitivity report will not be public;
- only separately hardened cross-stratum summaries may enter a release;
- source-level exact respondent counts, unresolved counts and weight sums are
  prohibited from public sensitivity artefacts.

## Open gates

- local browser-only IM-R7C execution;
- IM-R7D hostile weighted-missingness audit;
- Information & Management manuscript reconstruction;
- article–code–table–figure parity;
- final GitHub and Zenodo release;
- Elsevier submission preflight.

## Isolation

- default branch `main`: unchanged;
- final tag `v3.0.0`: not created;
- final GitHub release and Zenodo version: not created.
