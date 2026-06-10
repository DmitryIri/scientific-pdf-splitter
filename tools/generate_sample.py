"""Generate synthetic sample input and expected outputs for the portfolio demo."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pdf_splitter.models import ArticleMetadata, sample_articles  # noqa: E402
from pdf_splitter.output import write_outputs  # noqa: E402


def _pdf_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _content_stream(article: ArticleMetadata) -> bytes:
    lines = [
        f"Article ID: {article.article_id}",
        article.title,
        f"Authors: {', '.join(article.authors)}",
        f"Pages: {article.page_start}-{article.page_end}",
        "",
        article.abstract,
    ]
    commands = ["BT", "/F1 12 Tf", "72 760 Td", "14 TL"]
    for line in lines:
        commands.append(f"({_pdf_escape(line)}) Tj")
        commands.append("T*")
    commands.append("ET")
    return "\n".join(commands).encode("ascii")


def write_synthetic_pdf(path: Path, articles: list[ArticleMetadata]) -> Path:
    """Write a minimal valid PDF with one page per synthetic article."""

    path.parent.mkdir(parents=True, exist_ok=True)
    objects: list[bytes] = []
    page_ids = [4 + index * 2 for index in range(len(articles))]
    content_ids = [5 + index * 2 for index in range(len(articles))]
    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)

    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(articles)} >>".encode("ascii"))
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    for content_id, article in zip(content_ids, articles, strict=True):
        page_obj = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 3 0 R >> >> /Contents {content_id} 0 R >>"
        )
        content = _content_stream(article)
        stream = b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n"
        stream += content + b"\nendstream"
        objects.append(page_obj.encode("ascii"))
        objects.append(stream)

    output = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{index} 0 obj\n".encode("ascii"))
        output.extend(obj)
        output.extend(b"\nendobj\n")

    xref_offset = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )

    path.write_bytes(output)
    return path


def write_metadata(path: Path, articles: list[ArticleMetadata]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"articles": [article.to_dict() for article in articles]}
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> None:
    articles = sample_articles()
    pdf_path = write_synthetic_pdf(ROOT / "data/sample/input/sample_journal_issue.pdf", articles)
    metadata_path = write_metadata(ROOT / "data/sample/input/articles_metadata.json", articles)
    csv_path, json_path = write_outputs(articles, ROOT / "data/sample/output")

    print(f"Synthetic PDF: {pdf_path.relative_to(ROOT)}")
    print(f"Metadata JSON: {metadata_path.relative_to(ROOT)}")
    print(f"CSV output: {csv_path.relative_to(ROOT)}")
    print(f"JSON output: {json_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()