# Official `s1b` source audit — pre-local stage

## Findings

1. The pooled catalogue labels `s1b` as **Sampling size**.
2. The pooled record contains 21,055 cases and 723 variables.
3. The World Bank provides a public Data Dictionary XLSX described as a
   detailed description of `FAT0_raw_data_qje`.
4. The FAT collection covers formal firms with five or more employees and
   stratifies by firm size.
5. Country designs differ:
   - Croatia documents three strata: 5–19, 20–99 and 100+;
   - Poland documents six strata: 5–9, 10–19, 20–49, 50–99, 100–249 and 250+;
   - Burkina Faso documents a country-specific lower band.
6. Therefore, country study descriptions cannot establish the pooled code
   labels by themselves.

## Current conclusion

The candidate mapping `1/2/3 → small/medium/large` is plausible but not yet
accepted. The official pooled Data Dictionary XLSX is the decisive semantic
source. The local audit provides structural and falsification evidence only.
