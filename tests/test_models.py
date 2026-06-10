from pdf_splitter.models import ArticleMetadata, sample_articles


def test_sample_article_metadata_shape() -> None:
    articles = sample_articles()

    assert len(articles) == 3
    first = articles[0]
    assert isinstance(first, ArticleMetadata)
    assert first.article_id == "SPLIT-001"
    assert first.page_start == 1
    assert first.page_end == 4
    assert len(first.sha256) == 64
    assert first.to_csv_row()["authors"] == "Alex Morgan; Priya Shah"
