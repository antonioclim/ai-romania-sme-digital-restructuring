# Study 2 browser-only acquisition and non-redistribution protocol

## Purpose

This protocol governs acquisition of the selected World Bank FAT source before
any Study 2 outcome is inspected.

## Locked source

- title: Technology Sophistication Across Establishments
- reference ID: `WLD_2019-2023_FAT_v01_M`
- DOI: `10.48529/assd-3j65`
- selected function: Production Planning — MOST-used method

## User environment

All user-side actions must be possible through a web browser. No terminal,
desktop Git client or local Python installation is assumed.

## Access and confidentiality boundary

The source record requires login. The user must read and personally accept the
terms displayed by the World Bank Microdata Library. The microdata must not be
redistributed, uploaded to this repository, deposited in Zenodo, attached to
email or supplied to an AI service without prior written permission from the
source repository.

Public version 3 materials may include only:

- source citation and acquisition instructions;
- exact version, filename and checksum where permitted;
- transformation code;
- state and definition registers;
- tests;
- derived aggregate and non-disclosive outputs;
- claim–evidence mappings.

## Acquisition evidence

Before extraction or opening, a local browser tool must record:

- exact downloaded filename;
- file size;
- SHA-256;
- browser-reported MIME type;
- ZIP member names, sizes and CRC-32 values when the package is a standard ZIP.

Only the sanitised metadata report may be shared for verification. The original
microdata and extracted members remain under the user's control.

## Stop rule

No percentage, association, subgroup ranking or ODSA result may be calculated
until the structural acquisition gate verifies the pooled file, relevant fields,
state mapping, denominator and country coverage.

If the logged-in interface shows licensed access, an application workflow or
terms incompatible with the planned analysis, acquisition stops and the
displayed access state is documented before any file is downloaded.
