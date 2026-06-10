import json

import pytest

from pdf_splitter.models import sample_articles
from pdf_splitter.output import write_outputs
from pdf_splitter.workflow import (
    build_export_manifest,
    sha256_file,
    validate_export_invariant,
    write_workflow_artifacts,
)


def test_write_workflow_artifacts(tmp_path) -> None:
    articles = sample_articles()
    write_outputs(articles, tmp_path)

    manifest_path, report_path, checksums_path = write_workflow_artifacts(articles, tmp_path)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    checksums = checksums_path.read_text(encoding="utf-8").splitlines()

    assert manifest == {
        "issue_id": "ISSUE-2026-01",
        "articles_expected": 3,
        "articles_exported": 3,
        "csv_rows": 3,
        "json_records": 3,
        "validation_status": "passed",
    }
    assert report == {
        "issue_id": "ISSUE-2026-01",
        "pages_total": 12,
        "articles_detected": 3,
        "articles_exported": 3,
        "csv_rows": 3,
        "json_records": 3,
        "validation_status": "passed",
    }
    assert checksums == [
        f"{sha256_file(tmp_path / 'articles.csv')}  articles.csv",
        f"{sha256_file(tmp_path / 'articles.json')}  articles.json",
        f"{sha256_file(tmp_path / 'export_manifest.json')}  export_manifest.json",
    ]


def test_build_export_manifest_validates_invariant() -> None:
    payload = build_export_manifest(
        issue_id="ISSUE-2026-01",
        articles_expected=3,
        articles_exported=3,
        csv_rows=3,
        json_records=3,
    )

    assert payload["validation_status"] == "passed"


def test_validate_export_invariant_rejects_mismatch() -> None:
    with pytest.raises(ValueError, match="Export invariant failed"):
        validate_export_invariant(
            articles_expected=3,
            articles_exported=3,
            csv_rows=2,
            json_records=3,
        )
