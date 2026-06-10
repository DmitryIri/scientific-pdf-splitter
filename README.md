# scientific-pdf-splitter

[![CI](https://github.com/DmitryIri/scientific-pdf-splitter/actions/workflows/ci.yml/badge.svg)](https://github.com/DmitryIri/scientific-pdf-splitter/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A portfolio project that demonstrates a synthetic demo and production-inspired architecture for scientific PDF article extraction workflows: metadata contracts, validation, CSV/JSON exports, CI, and testing.

```text
article_id,title,page_start,page_end,sha256
SPLIT-001,Synthetic Cohort Study of Editorial Workflow Timing,1,3,9c5b...
SPLIT-002,Rule-Based Detection of Article Headers in Journal Issues,4,7,9f44...
SPLIT-003,Integrity Checks for Article-Level CSV and JSON Exports,8,10,31a2...
```

## Current Scope

This repository is currently a synthetic demo, portfolio project, production-inspired architecture, and proof-of-concept for document processing workflows.

The implemented layer focuses on:

- typed article metadata models
- deterministic synthetic sample data
- CSV and JSON export contracts
- validation rules for article IDs, page ranges, authors, titles, and SHA-256 hashes
- pytest, ruff, and GitHub Actions checks

It does not include real article boundary detection or production extraction heuristics yet. The README, samples, and tests are intentionally framed to avoid overstating the current implementation.

## What It Solves

Scientific journal issues are often distributed as long PDF files where article boundaries, page ranges, metadata, and export integrity need to be tracked consistently. This project shows the public skeleton of that workflow: a clean data contract, reproducible sample outputs, automated checks, and a staged path toward a fuller document-processing pipeline.

## Potential Business Applications

- Scientific publishing workflows
- Medical journal processing
- Research archive digitization
- Regulatory document processing
- Structured metadata extraction pipelines
- Academic ETL systems

## Quick Start

```bash
python -m pip install -e ".[dev]"
python tools/generate_sample.py
python examples/quickstart.py
```

The demo writes a synthetic PDF to `data/sample/input/sample_journal_issue.pdf` and article exports to `data/sample/output/articles.csv` and `data/sample/output/articles.json`.

## Output Format

| Field | Description |
| --- | --- |
| `article_id` | Stable article identifier for downstream processing |
| `title` | Article title |
| `authors` | Semicolon-separated author list in CSV; list of strings in JSON |
| `page_start` | First page of the article block |
| `page_end` | Last page of the article block |
| `sha256` | Deterministic SHA-256 digest for metadata integrity checks |

## Architecture

```text
Synthetic PDF + metadata
        |
        v
ArticleMetadata models
        |
        v
Validator -> CSV/JSON writers -> downstream editorial workflow
```

See also:

- `docs/architecture.md` for the implemented data flow
- `docs/architecture_overview.md` for the intended document-processing pipeline shape
- `docs/roadmap.md` for completed and planned phases

## Next Implementation Layer

The next implementation layer can add these capabilities without changing the public output contract:

- Article boundary detection
- PDF text extraction
- Metadata parsing
- Reference isolation
- Validation pipeline expansion

These are planned directions, not claims about the current version.

## Running Tests

```bash
pytest tests/ -v
ruff check src/ tests/ examples/ tools/
```

## Project Background

**Problem:** Scientific journal PDFs can require repeatable article-level exports before editorial, indexing, or data processing work can begin.

**Stack:** Python 3.11+, PyMuPDF dependency placeholder, CSV/JSON output, pytest, ruff, GitHub Actions.

**Role:** Sole engineer for the portfolio project structure, synthetic demo, metadata contract, validators, CI, and README framing.

**Outcome:** A clean public repository that demonstrates engineering hygiene for document-processing workflows without exposing internal systems, private data, or production code.