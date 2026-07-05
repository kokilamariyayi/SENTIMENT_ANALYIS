import csv
import tempfile
import unittest
from pathlib import Path

from xquik_sentiment140_adapter import (
    SENTIMENT140_COLUMNS,
    convert_csv,
    normalize_xquik_rows,
    sentiment140_target,
)


class XquikSentiment140AdapterTest(unittest.TestCase):
    def test_maps_common_sentiment_labels_to_sentiment140_targets(self):
        self.assertEqual(sentiment140_target("positive"), "4")
        self.assertEqual(sentiment140_target("Negative"), "0")
        self.assertEqual(sentiment140_target("neutral"), None)

    def test_normalizes_xquik_export_aliases(self):
        rows = normalize_xquik_rows(
            [
                {
                    "tweet_id": "100",
                    "created_at": "2026-07-05T12:00:00Z",
                    "full_text": "The service is fast",
                    "username": "customer",
                    "sentiment": "positive",
                    "keyword": "brand",
                },
                {
                    "tweet_id": "101",
                    "full_text": "No label yet",
                    "sentiment": "neutral",
                },
            ]
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["target"], "4")
        self.assertEqual(rows[0]["ids"], "100")
        self.assertEqual(rows[0]["flag"], "brand")
        self.assertEqual(rows[0]["user"], "customer")

    def test_converts_csv_with_sentiment140_header(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            source_path = Path(tmp_dir) / "xquik.csv"
            output_path = Path(tmp_dir) / "training.csv"
            source_path.write_text(
                "tweet_id,created_at,tweet_text,screen_name,label\n"
                "200,2026-07-05T12:00:00Z,Great launch,user_a,pos\n"
                "201,2026-07-05T13:00:00Z,Bad support,user_b,neg\n",
                encoding="utf-8",
            )

            count = convert_csv(source_path, output_path)

            self.assertEqual(count, 2)
            with output_path.open(newline="", encoding="utf-8") as output:
                reader = csv.DictReader(output)
                self.assertEqual(reader.fieldnames, SENTIMENT140_COLUMNS)
                rows = list(reader)

        self.assertEqual(rows[0]["target"], "4")
        self.assertEqual(rows[1]["target"], "0")


if __name__ == "__main__":
    unittest.main()
