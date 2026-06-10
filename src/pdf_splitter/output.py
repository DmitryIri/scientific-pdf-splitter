"""CSV and JSON writers for article metadata outputs."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from pdf_splitter.models import ArticleMetadata
from pdf_splitter.validator import validate_articles

CSV_FIELDS = ["article_id", "title", "authors", "page_start", "page_end", "sha256"]


def write_articles_csv(articles: list[ArticleMetadata], path: Path) -> Path:
    """Write article metadata to CSV."""

    validate_articles(articles)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for article in articles:
            writer.writerow(article.to_csv_row())
    return path


def write_articles_json(articles: list[ArticleMetadata], path: Path) -> Path:
    """Write article metadata to JSON."""

    validate_articles(articles)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"articles": [article.to_dict() for article in articles]}
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def write_outputs(articles: list[ArticleMetadata], output_dir: Path) -> tuple[Path, Path]:
    """Write both CSV and JSON output artifacts."""

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = write_articles_csv(articles, output_dir / "articles.csv")
    json_path = write_articles_json(articles, output_dir / "articles.json")
    return csv_path, json_path