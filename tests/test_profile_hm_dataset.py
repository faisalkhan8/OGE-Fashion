import csv
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from profile_hm_dataset import DatasetProfileError, profile_dataset


class HmDatasetProfilerTests(unittest.TestCase):
    def write_csv(self, path: Path, headers, rows):
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.write_csv(
            self.root / "articles.csv",
            ["article_id", "product_type_name", "product_group_name", "colour_group_name", "graphical_appearance_name", "detail_desc"],
            [
                {"article_id":"001", "product_type_name":"dress", "product_group_name":"garment", "colour_group_name":"blue", "graphical_appearance_name":"solid", "detail_desc":"text"},
                {"article_id":"002", "product_type_name":"shirt", "product_group_name":"garment", "colour_group_name":"", "graphical_appearance_name":"stripe", "detail_desc":""},
            ],
        )
        self.write_csv(
            self.root / "transactions_train.csv",
            ["t_dat", "customer_id", "article_id", "price", "sales_channel_id"],
            [
                {"t_dat":"2020-01-01", "customer_id":"secret-user-a", "article_id":"001", "price":"0.05", "sales_channel_id":"1"},
                {"t_dat":"2020-01-03", "customer_id":"secret-user-b", "article_id":"999", "price":"bad", "sales_channel_id":"2"},
                {"t_dat":"bad-date", "customer_id":"secret-user-c", "article_id":"002", "price":"0.12", "sales_channel_id":"1"},
            ],
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_aggregate_profile_and_privacy(self):
        report = profile_dataset(self.root)
        articles = report["files"]["articles"]
        transactions = report["files"]["transactions"]
        self.assertEqual(articles["rows"], 2)
        self.assertEqual(articles["unique_nonempty_article_ids"], 2)
        self.assertEqual(articles["missing_values"]["colour_group_name"], 1)
        self.assertEqual(transactions["rows"], 3)
        self.assertEqual(transactions["date_min"], "2020-01-01")
        self.assertEqual(transactions["date_max"], "2020-01-03")
        self.assertEqual(transactions["invalid_date_rows"], 1)
        self.assertEqual(transactions["invalid_price_rows"], 1)
        self.assertEqual(transactions["rows_with_article_id_not_in_articles_csv"], 1)
        rendered = str(report)
        self.assertNotIn("secret-user-a", rendered)
        self.assertNotIn("secret-user-b", rendered)

    def test_missing_file_fails_closed(self):
        (self.root / "transactions_train.csv").unlink()
        with self.assertRaises(DatasetProfileError):
            profile_dataset(self.root)

    def test_missing_required_column_fails_closed(self):
        self.write_csv(
            self.root / "transactions_train.csv",
            ["t_dat", "customer_id", "article_id", "price"],
            [],
        )
        with self.assertRaises(DatasetProfileError):
            profile_dataset(self.root)

    def test_duplicate_article_ids_are_counted(self):
        self.write_csv(
            self.root / "articles.csv",
            ["article_id", "product_type_name", "product_group_name", "colour_group_name", "graphical_appearance_name", "detail_desc"],
            [
                {"article_id":"001", "product_type_name":"dress", "product_group_name":"garment", "colour_group_name":"blue", "graphical_appearance_name":"solid", "detail_desc":"a"},
                {"article_id":"001", "product_type_name":"dress", "product_group_name":"garment", "colour_group_name":"blue", "graphical_appearance_name":"solid", "detail_desc":"b"},
            ],
        )
        report = profile_dataset(self.root)
        self.assertEqual(report["files"]["articles"]["duplicate_article_id_rows_after_first"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
