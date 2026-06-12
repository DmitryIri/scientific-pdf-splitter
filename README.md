# scientific-pdf-splitter

**Turn scientific journal issues into clean, validated, article-level data — a reliable, auditable foundation for publishing and research workflows.**

Per-article records with correct page ranges, structured metadata, and verifiable checksums — built so the output can be trusted downstream for indexing, review, or processing, instead of re-checked by hand.

[![CI](https://github.com/DmitryIri/scientific-pdf-splitter/actions/workflows/ci.yml/badge.svg)](https://github.com/DmitryIri/scientific-pdf-splitter/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## The Problem

Scientific journals ship as long, multi-article PDF issues. Before any indexing, review, archiving, or data processing can start, each issue has to be split into article-level records — with the right page ranges, metadata, and verified integrity.

Done by hand, this is slow, repetitive, and easy to get wrong — and it has to happen for **every issue, every time**. A single mismatched page range or dropped article quietly corrupts everything downstream.

This project shows the automated, verifiable alternative: a clean pipeline that turns an issue into structured, checked, reproducible article-level data.

---

## What It Does

```text
Journal issue (PDF)
        │
        ▼   extraction backend — synthetic in the demo, real PDF parsing in a production adaptation
Article metadata  (title, authors, page ranges)
        │
        ▼
[Validate]   enforce rules on IDs, page ranges, authors, titles
        │
        ▼
[Export]     CSV + JSON  +  manifest + processing report + SHA-256 checksums
```

The repository implements the **validation, export, and verification foundation** end to end; the extraction backend that feeds it is a clean integration point (synthetic data in the public demo).

---

## Engineered for Trust

Downstream work depends on this data being correct, so correctness is built into the pipeline, not assumed:

- **Validated** — every article record is checked: IDs, page ranges, authors, titles, and SHA-256 hashes.
- **Verifiable** — each export ships with a manifest and per-file SHA-256 checksums.
- **Reproducible** — deterministic output: the same issue produces the same result.
- **Auditable** — an issue-level processing report records what was detected, exported, and validated.

These are the properties that let a publishing or research team rely on the output instead of re-checking it by hand.

---

## Quick Start

```bash
python -m pip install -e ".[dev]"
python tools/generate_sample.py
python examples/quickstart.py
```

The demo writes a sample journal issue to `data/sample/input/` and article exports to `data/sample/output/` — `articles.csv`, `articles.json`, plus workflow-evidence artifacts (`export_manifest.json`, `issue_processing_report.json`, `checksums.sha256`).

Sample output:

```text
article_id,title,page_start,page_end,sha256
SPLIT-001,Synthetic Cohort Study of Editorial Workflow Timing,1,4,aff9...
SPLIT-002,Rule-Based Detection of Article Headers in Journal Issues,5,8,357e...
SPLIT-003,Integrity Checks for Article-Level CSV and JSON Exports,9,12,29a9...
```

---

## Output Format

| Field | Description |
| --- | --- |
| `article_id` | Stable article identifier for downstream processing |
| `title` | Article title |
| `authors` | Semicolon-separated author list in CSV; list of strings in JSON |
| `page_start` | First page of the article block |
| `page_end` | Last page of the article block |
| `sha256` | Deterministic SHA-256 digest for metadata integrity checks |

---

## Workflow Evidence

The pipeline does not just emit data — it emits **proof the data is correct**. Each run produces a manifest recording the core output invariant:

```json
{
  "issue_id": "ISSUE-2026-01",
  "articles_expected": 3,
  "articles_exported": 3,
  "csv_rows": 3,
  "json_records": 3,
  "validation_status": "passed"
}
```

An issue-level processing report summarizes the run:

```json
{
  "issue_id": "ISSUE-2026-01",
  "pages_total": 12,
  "articles_detected": 3,
  "articles_exported": 3,
  "csv_rows": 3,
  "json_records": 3,
  "validation_status": "passed"
}
```

And `checksums.sha256` records deterministic SHA-256 values for `articles.csv`, `articles.json`, and `export_manifest.json` — so any later change is detectable.

---

## Potential Business Applications

The same pattern — *turn a messy source document into validated, traceable, structured output* — applies wherever teams process documents at scale:

- Scientific and medical journal processing
- Research archive digitization
- Regulatory and compliance document processing
- Structured metadata extraction pipelines
- Pre-indexing and RAG data preparation

---

## Architecture

```text
Journal issue + metadata
        │
        ▼
ArticleMetadata models  (typed contracts)
        │
        ▼
Validator → CSV/JSON writers → manifest / report / checksums → downstream workflow
```

Each stage has a typed contract, so real extraction backends can be added without changing the public output format.

See `docs/architecture.md` (implemented data flow), `docs/architecture_overview.md` (intended pipeline shape), and `docs/roadmap.md` (phases).

---

## Running Tests

```bash
pytest tests/ -v
ruff check src/ tests/ examples/ tools/
```

CI runs on GitHub Actions. All tests use synthetic sample data — no private data required.

---

## Project Background

**Problem.** Scientific journal PDFs must be split into reliable, article-level exports before editorial, indexing, or data work can begin — a repetitive, error-prone manual task that recurs for every issue.

**Solution.** A clean pipeline that produces validated, checksummed article-level data with manifests and reproducibility built in, so downstream teams can trust the output instead of re-verifying it.

**Result.** A reliable, auditable foundation for document-processing workflows — designed so real PDF extraction can be added without changing the output contract that downstream systems depend on.

**Role.** Sole engineer — architecture, data contract, validators, CI, and the public-safe framing that keeps the repository shareable without exposing internal systems or private data.

---

## Current Scope

This public repository demonstrates the **data contract and verification foundation** on synthetic samples:

- **Synthetic sample data** — no real publications or authors; safe to run in seconds with no setup.
- **Implemented:** typed article-metadata models, CSV/JSON export contracts, manifest/report/checksum artifacts, validation rules, and CI.
- **The integration layer:** real PDF text extraction and article boundary detection are the stages a production adaptation adds — this repo demonstrates the reliable export and validation foundation those stages feed into.

The contract, validation, and verification pattern are real; the production extraction backend is the layer left open for adaptation to a specific publisher's sources.

---

## Stack

- Python 3.11+
- CSV / JSON export with manifest, report, and checksum artifacts
- pytest — testing · ruff — linting
- GitHub Actions CI

---

## License

MIT
