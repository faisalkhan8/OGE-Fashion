"""Tests for the pinned shade-source parser and ranking."""

import unittest

from oge_fashion.shades import parse_shade_csv, rank_shades


CSV_FIXTURE = """brand,product,hex,group,H,S,V,L
Brand A,Foundation One,F3CFB3,0,25,0.25,0.95,0.7
Brand B,Foundation Two,000000,1,0,0,0,0.0
Brand A,Foundation One,f3cfb3,0,25,0.25,0.95,0.7
Brand C,Foundation Three,FFFFFF,2,NA,NA,NA,0.9
"""


class ShadeParsingTests(unittest.TestCase):
    def test_parser_counts_rows_duplicates_and_missing_hsv(self):
        dataset = parse_shade_csv(CSV_FIXTURE)
        self.assertEqual(dataset.source_rows, 4)
        self.assertEqual(len(dataset.records), 3)
        self.assertEqual(dataset.duplicate_rows_removed, 1)
        self.assertEqual(dataset.hsv_missing_rows, 1)
        self.assertEqual(dataset.records[0].source_row, 2)
        self.assertEqual(dataset.records[2].source_row, 5)

    def test_disputed_l_column_is_not_required(self):
        rows = [line.rsplit(",", 1)[0] for line in CSV_FIXTURE.strip().splitlines()]
        fixture = "\n".join(rows) + "\n"
        dataset = parse_shade_csv(fixture)
        self.assertEqual(len(dataset.records), 3)

    def test_invalid_hex_is_rejected(self):
        fixture = CSV_FIXTURE.replace("F3CFB3", "NOTHEX", 1)
        with self.assertRaises(ValueError):
            parse_shade_csv(fixture)

    def test_missing_required_column_is_rejected(self):
        fixture = CSV_FIXTURE.replace("group,H,S,V,L", "H,S,V,L")
        with self.assertRaises(ValueError):
            parse_shade_csv(fixture)


class ShadeRankingTests(unittest.TestCase):
    def setUp(self):
        self.dataset = parse_shade_csv(CSV_FIXTURE)

    def test_exact_colour_is_ranked_first(self):
        matches = rank_shades(self.dataset, "F3CFB3", top_k=3)
        self.assertEqual(matches[0].shade.brand, "Brand A")
        self.assertAlmostEqual(matches[0].delta_e_2000, 0.0, places=10)

    def test_ties_are_deterministic(self):
        first = rank_shades(self.dataset, "FFFFFF", top_k=3)
        second = rank_shades(self.dataset, "FFFFFF", top_k=3)
        self.assertEqual(
            [(item.shade.brand, item.shade.product, item.shade.hex_value) for item in first],
            [(item.shade.brand, item.shade.product, item.shade.hex_value) for item in second],
        )

    def test_top_k_must_be_positive(self):
        with self.assertRaises(ValueError):
            rank_shades(self.dataset, "FFFFFF", top_k=0)


if __name__ == "__main__":
    unittest.main()
