# Architecture

This repository is a synthetic demo and production-inspired architecture for article-level metadata exports from scientific journal issue PDFs.

## Scope

The current version implements the portfolio skeleton only:

- typed article metadata model
- deterministic synthetic sample data
- minimal synthetic PDF generation
- CSV and JSON writers
- export manifest writer
- issue processing report writer
- checksum artifact writer
- validation rules for article IDs, page ranges, authors, titles, and SHA-256 format
- invariant validation for expected articles, exported articles, CSV rows, and JSON records
- pytest and ruff checks in CI

It does not include production extraction heuristics or private source logic.

## Data Flow

```text
data/sample/input/articles_metadata.json
        |
        v
pdf_splitter.models.ArticleMetadata
        |
        v
pdf_splitter.validator.validate_articles
        |
        v
pdf_splitter.output.write_outputs
        |
        v
data/sample/output/articles.csv + articles.json
        |
        v
pdf_splitter.workflow.write_workflow_artifacts
        |
        v
export_manifest.json + issue_processing_report.json + checksums.sha256
```

## Deterministic Output Contracts

The sample workflow writes three client-facing evidence artifacts:

- `export_manifest.json` records `articles_expected`, `articles_exported`, `csv_rows`, `json_records`, and `validation_status`.
- `issue_processing_report.json` records issue-level summary fields including `issue_id`, `pages_total`, detected articles, exported articles, and validation status.
- `checksums.sha256` records SHA-256 checksums for `articles.csv`, `articles.json`, and `export_manifest.json`.

The invariant is:

```text
articles_expected = articles_exported = csv_rows = json_records
```

If the invariant is violated, the workflow fails fast with `ValueError`.

## Future Implementation Layer

A later phase can add these modules without changing the public output contract:

- PDF text extraction using PyMuPDF or pdfplumber
- article boundary detection
- metadata header parsing
- reference section isolation
- issue-level validation reports

This staged approach keeps the portfolio project reviewable while preserving a path toward a fuller document-processing pipeline.
