"""Workflow evidence artifacts for the synthetic issue-processing demo."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from pdf_splitter.models import ArticleMetadata

DEFAULT_ISSUE_ID = "ISSUE-2026-01"


def count_csv_rows(path: Path) -> int:
    """Count article rows in the CSV export."""

    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def count_json_records(path: Path) -> int:
    """Count article records in the JSON export."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    return len(payload["articles"])


def validate_export_invariant(
    *,
    articles_expected: int,
    articles_exported: int,
    csv_rows: int,
    json_records: int,
) -> None:
    """Fail fast unless all public workflow counts agree."""

    counts = {
        "articles_expected": articles_expected,
        "articles_exported": articles_exported,
        "csv_rows": csv_rows,
        "json_records": json_records,
    }
    if len(set(counts.values())) != 1:
        raise ValueError(f"Export invariant failed: {counts}")


def build_export_manifest(
    *,
    issue_id: str,
    articles_expected: int,
    articles_exported: int,
    csv_rows: int,
    json_records: int,
) -> dict[str, int | str]:
    """Build the deterministic export manifest payload."""

    validate_export_invariant(
        articles_expected=articles_expected,
        articles_exported=articles_exported,
        csv_rows=csv_rows,
        json_records=json_records,
    )
    return {
        "issue_id": issue_id,
        "articles_expected": articles_expected,
        "articles_exported": articles_exported,
        "csv_rows": csv_rows,
        "json_records": json_records,
        "validation_status": "passed",
    }


def build_issue_processing_report(
    *,
    issue_id: str,
    pages_total: int,
    articles_detected: int,
    articles_exported: int,
    csv_rows: int,
    json_records: int,
) -> dict[str, int | str]:
    """Build a client-facing synthetic issue processing report."""

    validate_export_invariant(
        articles_expected=articles_detected,
        articles_exported=articles_exported,
        csv_rows=csv_rows,
        json_records=json_records,
    )
    return {
        "issue_id": issue_id,
        "pages_total": pages_total,
        "articles_detected": articles_detected,
        "articles_exported": articles_exported,
        "csv_rows": csv_rows,
        "json_records": json_records,
        "validation_status": "passed",
    }


def sha256_file(path: Path) -> str:
    """Compute a SHA-256 digest for an output artifact."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json_artifact(payload: dict[str, Any], path: Path) -> Path:
    """Write a deterministic JSON artifact."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def write_checksums(output_dir: Path, filenames: list[str]) -> Path:
    """Write checksums for selected output artifacts."""

    lines = [f"{sha256_file(output_dir / filename)}  {filename}" for filename in filenames]
    checksums_path = output_dir / "checksums.sha256"
    checksums_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return checksums_path


def write_workflow_artifacts(
    articles: list[ArticleMetadata],
    output_dir: Path,
    *,
    issue_id: str = DEFAULT_ISSUE_ID,
) -> tuple[Path, Path, Path]:
    """Generate manifest, report, and checksum artifacts for the demo workflow."""

    csv_path = output_dir / "articles.csv"
    json_path = output_dir / "articles.json"
    articles_expected = len(articles)
    articles_exported = len(articles)
    csv_rows = count_csv_rows(csv_path)
    json_records = count_json_records(json_path)
    pages_total = max(article.page_end for article in articles)

    export_manifest = build_export_manifest(
        issue_id=issue_id,
        articles_expected=articles_expected,
        articles_exported=articles_exported,
        csv_rows=csv_rows,
        json_records=json_records,
    )
    report = build_issue_processing_report(
        issue_id=issue_id,
        pages_total=pages_total,
        articles_detected=articles_expected,
        articles_exported=articles_exported,
        csv_rows=csv_rows,
        json_records=json_records,
    )

    manifest_path = write_json_artifact(export_manifest, output_dir / "export_manifest.json")
    report_path = write_json_artifact(report, output_dir / "issue_processing_report.json")
    checksums_path = write_checksums(
        output_dir,
        ["articles.csv", "articles.json", "export_manifest.json"],
    )
    return manifest_path, report_path, checksums_path
