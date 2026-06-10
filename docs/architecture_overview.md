# Architecture Overview

This diagram shows the intended document-processing workflow shape. In the current version, the metadata contract, validation layer, CSV/JSON output, export manifest, issue report, and checksum artifacts are implemented with synthetic sample data. The upstream PDF extraction stages are planned for a later implementation phase.

```text
PDF Input
   |
   v
Article Detection
   |
   v
Metadata Extraction
   |
   v
Validation
   |
   v
CSV / JSON Output
   |
   v
Manifest / Report / Checksums
```

## Current Implementation

Implemented now:

- synthetic PDF input generation
- synthetic article metadata fixtures
- metadata model
- validation checks
- CSV and JSON exports
- export manifest
- issue processing report
- checksum artifact
- deterministic invariant validation
- tests and CI

Planned later:

- real PDF text extraction
- article boundary detection
- metadata parsing from extracted text
- reference isolation
- expanded validation reports

## Integrity Verification

The public workflow evidence uses a production-inspired contract without claiming real extraction behavior:

- `export_manifest.json` confirms that expected articles, exported articles, CSV rows, and JSON records agree.
- `issue_processing_report.json` summarizes the synthetic issue run.
- `checksums.sha256` provides deterministic integrity checks for selected sample outputs.
