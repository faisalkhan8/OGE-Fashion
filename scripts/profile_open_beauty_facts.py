"""Aggregate-only Open Beauty Facts makeup catalogue profiler.

Queries the structured-search API for a small number of category tags.
Product records are processed in memory only; only aggregate statistics are
printed. Product images, names, barcodes, and raw records are never persisted.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone

API_BASE = "https://world.openbeautyfacts.org/api/v2/search"
DEFAULT_CATEGORIES = (
    "makeup",
    "make-up",
    "cosmetics",
    "foundation",
    "lipstick",
    "mascara",
    "eyeshadow",
    "face-makeup",
    "lip-makeup",
)
FIELDS = (
    "code",
    "product_name",
    "brands",
    "categories_tags",
    "ingredients_text",
    "allergens_tags",
    "countries_tags",
    "last_modified_t",
)
USER_AGENT = (
    "OGE-Fashion-research/0.1 "
    "(https://github.com/faisalkhan8/OGE-Fashion)"
)


def request_category(category: str, page_size: int, timeout: float) -> dict:
    params = {
        "categories_tags_en": category,
        "page": 1,
        "page_size": page_size,
        "fields": ",".join(FIELDS),
    }
    url = API_BASE + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read(5_000_001)
    if len(raw) > 5_000_000:
        raise RuntimeError("API response exceeded the 5 MB safety limit.")
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("products"), list):
        raise RuntimeError("API response did not contain a products array.")
    return data


def profile_products(products: list[dict]) -> dict:
    checks = {
        "product_name": lambda p: bool(str(p.get("product_name") or "").strip()),
        "brand": lambda p: bool(str(p.get("brands") or "").strip()),
        "category_tags": lambda p: bool(p.get("categories_tags")),
        "ingredients_text": lambda p: bool(str(p.get("ingredients_text") or "").strip()),
        "allergens_tags": lambda p: bool(p.get("allergens_tags")),
        "countries_tags": lambda p: bool(p.get("countries_tags")),
        "last_modified_t": lambda p: bool(p.get("last_modified_t")),
    }
    counts = {
        field: sum(1 for product in products if predicate(product))
        for field, predicate in checks.items()
    }
    barcodes = [
        str(product.get("code") or "").strip()
        for product in products
        if str(product.get("code") or "").strip()
    ]
    missing_codes = len(products) - len(barcodes)
    duplicate_barcode_rows = len(barcodes) - len(set(barcodes))
    return {
        "sample_records_returned": len(products),
        "records_without_barcode": missing_codes,
        "unique_barcodes_in_sample": len(set(barcodes)),
        "duplicate_barcode_rows_in_sample": duplicate_barcode_rows,
        "field_present_counts": counts,
        "field_coverage_pct": {
            field: round(100.0 * count / len(products), 1) if products else None
            for field, count in counts.items()
        },
    }


def run_profile(categories: tuple[str, ...], page_size: int, timeout: float, delay: float) -> dict:
    result = {
        "profiled_at_utc": datetime.now(timezone.utc).isoformat(),
        "api": API_BASE,
        "api_version_note": (
            "Structured category search is documented under API v2. "
            "Official documentation currently labels v2 deprecated and states "
            "structured search is not available in v3."
        ),
        "requested_fields": list(FIELDS),
        "page_size": page_size,
        "categories": {},
        "limitations": [
            "Counts are returned by the API for the queried taxonomy tag and may overlap across tags.",
            "Only the first page is sampled for field coverage.",
            "A missing field in this sample does not establish that all records lack it.",
            "Community-contributed product metadata is not ground-truth user preference data.",
            "No images or raw product records are saved or printed.",
        ],
    }

    for index, category in enumerate(categories):
        try:
            payload = request_category(category, page_size, timeout)
            products = payload["products"]
            result["categories"][category] = {
                "api_total_count": payload.get("count"),
                "page": payload.get("page"),
                "page_size": payload.get("page_size"),
                "page_count": payload.get("page_count"),
                **profile_products(products),
                "status": "ok",
            }
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, RuntimeError, ValueError) as exc:
            result["categories"][category] = {
                "status": "error",
                "error_type": type(exc).__name__,
                "error": str(exc)[:300],
            }

        if index < len(categories) - 1 and delay > 0:
            time.sleep(delay)

    success_count = sum(
        1 for entry in result["categories"].values() if entry.get("status") == "ok"
    )
    result["summary"] = {
        "category_queries": len(categories),
        "successful_queries": success_count,
        "failed_queries": len(categories) - success_count,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--categories",
        default=",".join(DEFAULT_CATEGORIES),
        help="Comma-separated English category tags to test.",
    )
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument(
        "--delay",
        type=float,
        default=6.0,
        help="Seconds between category requests; default 6 seconds to limit request rate.",
    )
    args = parser.parse_args()

    categories = tuple(dict.fromkeys(
        part.strip().lower() for part in args.categories.split(",") if part.strip()
    ))
    if not categories:
        parser.error("At least one category tag is required.")
    if not 1 <= args.page_size <= 100:
        parser.error("--page-size must be between 1 and 100.")
    if args.timeout <= 0 or args.delay < 0:
        parser.error("--timeout must be positive and --delay cannot be negative.")

    result = run_profile(categories, args.page_size, args.timeout, args.delay)
    print(json.dumps(result, indent=2, sort_keys=True))

    if result["summary"]["successful_queries"] == 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
