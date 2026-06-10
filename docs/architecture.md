# Architecture

This repository is a synthetic demo and production-inspired architecture for article-level metadata exports from scientific journal issue PDFs.

## Scope

The current version implements the portfolio skeleton only:

- typed article metadata model
- deterministic synthetic sample data
- minimal synthetic PDF generation
- CSV and JSON writers
- validation rules for article IDs, page ranges, authors, titles, and SHA-256 format
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
```

## Future Implementation Layer

A later phase can add these modules without changing the public output contract:

- PDF text extraction using PyMuPDF or pdfplumber
- article boundary detection
- metadata header parsing
- reference section isolation
- issue-level validation reports

This staged approach keeps the portfolio project reviewable while preserving a path toward a fuller document-processing pipeline.