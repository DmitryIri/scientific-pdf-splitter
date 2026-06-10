"""Data models for article-level extraction output."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ArticleMetadata:
    """Normalized metadata for one article extracted from a journal issue."""

    article_id: str
    title: str
    authors: list[str]
    page_start: int
    page_end: int
    abstract: str
    sha256: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ArticleMetadata:
        return cls(
            article_id=str(payload["article_id"]),
            title=str(payload["title"]),
            authors=[str(author) for author in payload["authors"]],
            page_start=int(payload["page_start"]),
            page_end=int(payload["page_end"]),
            abstract=str(payload["abstract"]),
            sha256=str(payload["sha256"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_csv_row(self) -> dict[str, str | int]:
        return {
            "article_id": self.article_id,
            "title": self.title,
            "authors": "; ".join(self.authors),
            "page_start": self.page_start,
            "page_end": self.page_end,
            "sha256": self.sha256,
        }


def stable_article_hash(
    article_id: str,
    title: str,
    authors: list[str],
    page_start: int,
    page_end: int,
    abstract: str,
) -> str:
    """Create a deterministic content hash for sample metadata."""

    raw = "|".join(
        [article_id, title, ";".join(authors), str(page_start), str(page_end), abstract]
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def sample_articles() -> list[ArticleMetadata]:
    """Return synthetic article metadata used by the demo and tests."""

    payloads = [
        {
            "article_id": "SPLIT-001",
            "title": "Synthetic Cohort Study of Editorial Workflow Timing",
            "authors": ["Alex Morgan", "Priya Shah"],
            "page_start": 1,
            "page_end": 4,
            "abstract": "A synthetic study block used to demonstrate article boundary metadata.",
        },
        {
            "article_id": "SPLIT-002",
            "title": "Rule-Based Detection of Article Headers in Journal Issues",
            "authors": ["Maya Chen"],
            "page_start": 5,
            "page_end": 8,
            "abstract": (
                "A synthetic methods block for illustrating deterministic "
                "extraction output."
            ),
        },
        {
            "article_id": "SPLIT-003",
            "title": "Integrity Checks for Article-Level CSV and JSON Exports",
            "authors": ["Jon Bell", "Nora Kim"],
            "page_start": 9,
            "page_end": 12,
            "abstract": "A synthetic validation block showing SHA-256 metadata integrity checks.",
        },
    ]

    articles: list[ArticleMetadata] = []
    for item in payloads:
        sha256 = stable_article_hash(
            article_id=item["article_id"],
            title=item["title"],
            authors=item["authors"],
            page_start=item["page_start"],
            page_end=item["page_end"],
            abstract=item["abstract"],
        )
        articles.append(ArticleMetadata(sha256=sha256, **item))
    return articles


def load_articles(path: Path) -> list[ArticleMetadata]:
    """Load article metadata from a JSON file."""

    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return [ArticleMetadata.from_dict(item) for item in payload["articles"]]
