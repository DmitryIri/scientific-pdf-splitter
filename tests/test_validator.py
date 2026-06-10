import pytest

from pdf_splitter.models import ArticleMetadata, sample_articles
from pdf_splitter.validator import validate_articles


def test_validator_accepts_sample_articles() -> None:
    validate_articles(sample_articles())


def test_validator_rejects_invalid_page_range() -> None:
    article = sample_articles()[0]
    invalid = ArticleMetadata(
        article_id=article.article_id,
        title=article.title,
        authors=article.authors,
        page_start=5,
        page_end=2,
        abstract=article.abstract,
        sha256=article.sha256,
    )

    with pytest.raises(ValueError, match="page_end"):
        validate_articles([invalid])