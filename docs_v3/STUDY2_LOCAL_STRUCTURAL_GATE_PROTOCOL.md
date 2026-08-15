# Study 2 local structural gate protocol

## Verified acquisition evidence

The authorised user downloaded the pooled CSV package through the World Bank
Microdata Library browser interface and produced a local sanitised evidence
report.

```text
archive: WLD_2019-2023_FAT_v01_M_CSV.zip
size: 1,752,618 bytes
SHA-256: 6d77d3ffb9dcef2ca4534e1c438ddd2e0b357eb852e6c5b48aa5fa6c3cbe2f0e
container: PASS
members:
  - fat0_raw_data_qje.csv (19,633,172 uncompressed bytes; CRC-32 4418a02b)
  - isic_data.csv (376,982 uncompressed bytes; CRC-32 8b0bff2d)
```

The report states that processing occurred in a local browser tab, no network
upload was performed and no microdata rows or file content were included.

## Structural gate only

The next local browser tool may inspect:

- exact CSV identity, size and SHA-256;
- row and column counts;
- header integrity;
- presence and numeric validity of `country`, `e1` and `base_wt`;
- presence and code-domain consistency of direct `b9b` or a complete `ib9b*`
  MOST-used indicator family;
- candidate denominator size;
- country coverage;
- one-hot or mapping failures.

It must not calculate or disclose:

- state-specific frequencies;
- levels for the three ODSA definitions;
- cross-tabulations between definitions and establishment size;
- Cramér's V;
- subgroup rankings or reversals;
- country-specific outcome results.

The `db9a*` adoption family is not an admissible substitute for the MOST-used
state source because multiple technologies may be adopted simultaneously.

## Gate thresholds

```text
mapping failure share:               <= 0.5%
candidate denominator:               >= 5,000
countries with >=100 valid cases:    >= 10
required descriptor fields:          country, e1, base_wt
```

Only a sanitised structural JSON may be returned for review. Source microdata
remain local and may not be added to GitHub or Zenodo.
