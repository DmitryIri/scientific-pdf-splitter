import csv
import json

from pdf_splitter.models import sample_articles
from pdf_splitter.output import write_outputs


def test_write_csv_and_json_outputs(tmp_path) -> None:
    csv_path, json_path = write_outputs(sample_articles(), tmp_path)

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert csv_path.name == "articles.csv"
    assert json_path.name == "articles.json"
    assert len(rows) == 3
    assert rows[0]["article_id"] == "SPLIT-001"
    assert (
        payload["articles"][1]["title"]
        == "Rule-Based Detection of Article Headers in Journal Issues"
    )