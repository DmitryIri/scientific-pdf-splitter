"""Run the synthetic portfolio demo and export article metadata."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pdf_splitter.models import load_articles  # noqa: E402
from pdf_splitter.output import write_outputs  # noqa: E402
from pdf_splitter.validator import validate_articles  # noqa: E402
from pdf_splitter.workflow import write_workflow_artifacts  # noqa: E402


def main() -> None:
    metadata_path = ROOT / "data/sample/input/articles_metadata.json"
    output_dir = ROOT / "data/sample/output"

    articles = load_articles(metadata_path)
    validate_articles(articles)
    csv_path, json_path = write_outputs(articles, output_dir)
    manifest_path, report_path, checksums_path = write_workflow_artifacts(articles, output_dir)

    print("Generated synthetic article exports")
    print(f"Articles: {len(articles)}")
    print(f"CSV: {csv_path.relative_to(ROOT)}")
    print(f"JSON: {json_path.relative_to(ROOT)}")
    print(f"Export manifest: {manifest_path.relative_to(ROOT)}")
    print(f"Issue report: {report_path.relative_to(ROOT)}")
    print(f"Checksums: {checksums_path.relative_to(ROOT)}")
    print("Sample row:")
    print(
        f"- {articles[0].article_id}: {articles[0].title} "
        f"({articles[0].page_start}-{articles[0].page_end})"
    )


if __name__ == "__main__":
    main()
