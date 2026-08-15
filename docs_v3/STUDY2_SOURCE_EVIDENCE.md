# Study 2 source-evidence dossier

## Status

This dossier records the evidence used to select the independent Study 2 source
before downloading its microdata or calculating any ODSA result. Search and
verification date: **15 August 2026**.

The dossier distinguishes verified source facts from acquisition-stage
conditions. It does not report outcome frequencies from the selected dataset.

## 1. Selected source

### 1.1 Record identity

- **Title:** *Technology Sophistication Across Establishments*
- **Provider:** World Bank Microdata Library
- **Survey reference:** `WLD_2019-2023_FAT_v01_M`
- **Dataset DOI:** https://doi.org/10.48529/assd-3j65
- **Version date:** 30 January 2026
- **Version note:** edited, anonymised datasets for public distribution
- **Collection period:** June 2019 to December 2023
- **Unit of analysis:** establishments
- **Documented cases:** 21,055
- **Documented variables in the main file:** 723
- **Geographic coverage:** 15 countries

The source metadata states that the surveys are nationally representative for
formal establishments with five or more workers, except that Brazil and India
cover specified states. Sampling is stratified by establishment size, sector
and geographic region. Country-specific response rates and sampling weights are
documented by the provider.

### 1.2 Associated publication and reproducibility package

- Cirera, X., Comin, D., and Cruz, M. (2026). *Technology Sophistication Across
  Establishments*. *The Quarterly Journal of Economics, 141*(3), 2025–2085.
  https://doi.org/10.1093/qje/qjag018
- World Bank reproducibility package:
  https://doi.org/10.60572/xw8f-0k41
- Reproducibility package reference: `PP_WLD_2025_516`

The World Bank records the reproducibility package as computationally verified.
The package does not redistribute all underlying source data and requires
replicators to obtain the restricted source files separately.

## 2. Focal business function

The locked Study 2 business function is **production planning**. The original
FAT instrument documents the following mutually exclusive categories for the
most-used production-planning method:

1. handwritten processes;
2. computers with standard software;
3. mobile apps or digital platforms;
4. specialised software;
5. enterprise resource planning (ERP);
6. other.

The pooled data dictionary independently confirms:

- the `country` field;
- establishment identifier `firmid`;
- sampling weight `base_wt`;
- employment field `e1`;
- production-planning adoption indicators `db9a1` to `db9a5`;
- a pooled-file most-used specialised-software indicator labelled `ib9b4`.

The direct categorical field `b9b` is documented in country-level FAT records.
The complete representation of the most-used production-planning field in the
pooled download must therefore be verified against the acquired dictionary
before analysis. No unverified field family is treated as present merely
because its name would be plausible.

## 3. Access and legal boundary

The Microdata Library requires a free registered-user login for access to this
record. Its general microdata terms require attribution and prohibit
redistribution or sale of source microdata without prior written agreement.
Use is limited to statistical and scientific research and to aggregate
reporting. The version 3 public repository will therefore contain:

- source citation and access instructions;
- source version and checksum where permitted;
- transformation code;
- state and definition registers;
- derived aggregate outputs;
- tests and claim–evidence mappings.

It will **not** contain the downloaded FAT microdata.

## 4. Structural suitability for ODSA

The source is suitable in principle because it combines:

- an explicit finite state register;
- mutually exclusive most-used-method categories;
- at least three substantively defensible nested definitions;
- employment size and country descriptors;
- a large, multi-country establishment sample;
- documented weights, questionnaire and implementation material;
- persistent identifiers for the dataset and reproducibility package;
- substantive independence from Study 1.

Selection is conditional on the acquisition checks in
`selection_registry.yml`. A failure of those checks activates the prespecified
reserve sequence rather than a post-result search for a favourable dataset.

## 5. Candidate evidence

### 5.1 United States Census Bureau — 2018 Annual Business Survey

The Digital Technology Module provides official, disclosure-reviewed aggregate
tables by employment size, geography and industry. It is retained as the first
reserve because the public aggregate structure is less suitable than FAT for
record-level state reconstruction and positive-class composition.

### 5.2 Eurostat — Digital Intensity Index

The Digital Intensity Index classifies enterprises into four mutually
exclusive levels:

- very low: 0–3 technologies;
- low: 4–6;
- high: 7–9;
- very high: 10–12.

“At least basic” is the union of low, high and very high. Eurostat also warns
that the twelve component technologies vary between survey years, limiting
longitudinal comparability. The source is retained as the second reserve.

### 5.3 Flash Eurobarometer 486

- **GESIS study:** `ZA7637`, version 2.0.0
- **DOI:** https://doi.org/10.4232/1.13639
- **Units:** 16,365 organisations
- **Variables:** 385

The survey includes multiple digital-technology items, but they are not one
preserved mutually exclusive process-state variable. Deriving a count or
maturity ladder would create rather than recover the required state structure.
The candidate is excluded.

### 5.4 United States Census Bureau — BTOS AI supplement

The public material distinguishes current AI use from expected use in six
months. Published marginal estimates do not directly recover the joint states
current-only, planned-only, both and neither. The candidate is excluded.

## 6. Official source locations

- World Bank dataset:
  https://microdata.worldbank.org/catalog/8209
- World Bank metadata JSON:
  https://microdata.worldbank.org/metadata/export/8209/json
- World Bank data dictionary:
  https://microdata.worldbank.org/catalog/8209/download/356712
- World Bank questionnaire:
  https://microdata.worldbank.org/catalog/8209/download/356714
- World Bank reproducibility package:
  https://reproducibility.worldbank.org/catalog/463
- World Bank Microdata Library terms:
  https://microdata.worldbank.org/terms-of-use
- QJE publication:
  https://doi.org/10.1093/qje/qjag018
- US Census ABS technology methodology:
  https://www.census.gov/data/tables/2018/econ/abs/technology-tables-methodology.html
- Eurostat digital economy and society information:
  https://ec.europa.eu/eurostat/web/digital-economy-and-society/information-data
- GESIS Flash Eurobarometer 486:
  https://doi.org/10.4232/1.13639
- US Census BTOS:
  https://www.census.gov/programs-surveys/btos.html

## 7. Evidence boundary

This dossier supports **selection and acquisition planning only**. It does not
support any claim about:

- the frequency of any production-planning state;
- the sign or magnitude of definition sensitivity;
- country rankings;
- firm-size associations;
- global technology prevalence;
- causal effects;
- the superiority of ERP or any other state.

Those claims remain prohibited until the source is lawfully acquired, the
structural gate passes and the locked analysis is executed.
