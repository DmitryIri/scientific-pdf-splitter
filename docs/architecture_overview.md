# Architecture Overview

This diagram shows the intended document-processing workflow shape. In the current version, the metadata contract, validation layer, and CSV/JSON output are implemented with synthetic sample data. The upstream PDF extraction stages are planned for a later implementation phase.

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
```

## Current Implementation

Implemented now:

- synthetic PDF input generation
- synthetic article metadata fixtures
- metadata model
- validation checks
- CSV and JSON exports
- tests and CI

Planned later:

- real PDF text extraction
- article boundary detection
- metadata parsing from extracted text
- reference isolation
- expanded validation reports