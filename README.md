# scientific-pdf-splitter

[![CI](https://github.com/DmitryIri/scientific-pdf-splitter/actions/workflows/ci.yml/badge.svg)](https://github.com/DmitryIri/scientific-pdf-splitter/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A portfolio project that demonstrates a synthetic demo and production-inspired architecture for converting scientific journal issue metadata into validated article-level CSV and JSON exports.

```text
article_id,title,page_start,page_end,sha256
SPLIT-001,Synthetic Cohort Study of Editorial Workflow Timing,1,3,9c5b...
SPLIT-002,Rule-Based Detection of Article Headers in Journal Issues,4,7,9f44...
SPLIT-003,Integrity Checks for Article-Level CSV and JSON Exports,8,10,31a2...
```

## What It Solves

Scientific journal issues are often distributed as long PDF files where article boundaries, page ranges, metadata, and export integrity need to be tracked consistently. This repository is a synthetic demo of the data contract and validation layer for that workflow. It is designed as a portfolio project, not as a claim of production readiness.

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

The current skeleton focuses on the normalized metadata layer, output contract, and validation behavior. A later implementation layer can add article boundary detection, metadata parsing, reference isolation, and PDF text extraction on top of this structure.

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