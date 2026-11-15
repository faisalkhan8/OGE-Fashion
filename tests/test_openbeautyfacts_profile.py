"""Unit tests for aggregate-only Open Beauty Facts profiling."""

import unittest

from scripts.profile_open_beauty_facts import profile_products


class OpenBeautyFactsProfileTests(unittest.TestCase):
    def test_profile_counts_duplicates_without_exposing_product_rows(self):
        products = [
            {
                "code": "0001",
                "product_name": "Product A",
                "brands": "Brand A",
                "categories_tags": ["en:makeup"],
                "ingredients_text": "ingredient list",
                "allergens_tags": [],
                "countries_tags": ["en:france"],
                "last_modified_t": 100,
            },
            {
                "code": "0001",
                "product_name": "Product A duplicate record",
                "brands": "Brand A",
                "categories_tags": ["en:makeup"],
                "ingredients_text": "",
                "allergens_tags": [],
                "countries_tags": ["en:france"],
                "last_modified_t": 100,
            },
            {
                "code": "0002",
                "product_name": "Product B",
                "brands": "",
                "categories_tags": ["en:makeup"],
                "ingredients_text": "another list",
                "allergens_tags": ["en:some-tag"],
                "countries_tags": [],
                "last_modified_t": 200,
            },
            {
                "code": "",
                "product_name": "",
                "brands": "Brand C",
                "categories_tags": [],
                "ingredients_text": "",
                "allergens_tags": [],
                "countries_tags": [],
                "last_modified_t": None,
            },
        ]

        result = profile_products(products)
        self.assertEqual(result["sample_records_returned"], 4)
        self.assertEqual(result["records_without_barcode"], 1)
        self.assertEqual(result["unique_barcodes_in_sample"], 2)
        self.assertEqual(result["duplicate_barcode_rows_in_sample"], 1)
        self.assertEqual(result["field_present_counts"]["product_name"], 3)
        self.assertEqual(result["field_present_counts"]["ingredients_text"], 2)
        self.assertEqual(result["field_coverage_pct"]["categories_tags"], 75.0)
        self.assertNotIn("products", result)
        self.assertNotIn("product_name", result)


if __name__ == "__main__":
    unittest.main()
