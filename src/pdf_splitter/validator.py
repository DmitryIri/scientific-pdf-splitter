"""Validation helpers for normalized article metadata."""

from __future__ import annotations

import re

from pdf_splitter.models import ArticleMetadata

_SHA256_RE = re.compile(r"^[a-f0-9]{64}$")


def validate_articles(articles: list[ArticleMetadata]) -> None:
    """Validate article metadata before export."""

    if not articles:
        raise ValueError("At least one article is required")

    seen_ids: set[str] = set()
    for article in articles:
        if not article.article_id.strip():
            raise ValueError("article_id must not be empty")
        if article.article_id in seen_ids:
            raise ValueError(f"Duplicate article_id: {article.article_id}")
        seen_ids.add(article.article_id)

        if not article.title.strip():
            raise ValueError(f"title must not be empty for {article.article_id}")
        if not article.authors:
            raise ValueError(f"authors must not be empty for {article.article_id}")
        if article.page_start < 1:
            raise ValueError(f"page_start must be positive for {article.article_id}")
        if article.page_end < article.page_start:
            raise ValueError(f"page_end must be >= page_start for {article.article_id}")
        if not _SHA256_RE.fullmatch(article.sha256):
            raise ValueError(
                f"sha256 must be a 64-character lowercase hex digest for {article.article_id}"
            )