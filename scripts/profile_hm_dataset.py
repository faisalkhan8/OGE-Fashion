"""Privacy-conscious aggregate profiler for the H&M fashion recommendation CSVs.

Only aggregate counts, date bounds, file sizes and hashes are emitted. No
customer/article identifiers or row-level records are written to the report.
The user must download the data and accept the current Kaggle competition rules.
"""
from __future__ import annotations

import argparse
import csv
from datetime import date
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable


class DatasetProfileError(ValueError):
    """Raised when required input files or expected columns are missing."""


ARTICLE_REQUIRED = {
    "article_id", "product_type_name", "product_group_name",
    "colour_group_name", "graphical_appearance_name", "detail_desc",
}
TRANSACTION_REQUIRED = {
    "t_dat", "customer_id", "article_id", "price", "sales_channel_id",
}
ARTICLE_PROFILE_FIELDS = (
    "article_id", "product_type_name", "product_group_name",
    "colour_group_name", "graphical_appearance_name", "detail_desc",
)
TRANSACTION_PROFILE_FIELDS = (
    "t_dat", "customer_id", "article_id", "price", "sales_channel_id",
)


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _header_and_reader(path: Path, required: set[str]):
    if not path.is_file():
        raise DatasetProfileError(f"Required file not found: {path.name}")
    stream = path.open("r", encoding="utf-8-sig", newline="")
    reader = csv.DictReader(stream)
    header = set(reader.fieldnames or [])
    missing = sorted(required - header)
    if missing:
        stream.close()
        raise DatasetProfileError(
            f"{path.name} is missing required columns: {', '.join(missing)}"
        )
    return stream, reader, list(reader.fieldnames or [])


def profile_articles(path: Path) -> tuple[dict[str, object], set[str]]:
    stream, reader, header = _header_and_reader(path, ARTICLE_REQUIRED)
    missing_counts = {name: 0 for name in ARTICLE_PROFILE_FIELDS}
    article_ids: set[str] = set()
    duplicate_ids = 0
    rows = 0
    try:
        for row in reader:
            rows += 1
            for name in ARTICLE_PROFILE_FIELDS:
                if not (row.get(name) or "").strip():
                    missing_counts[name] += 1
            article_id = (row.get("article_id") or "").strip()
            if article_id:
                if article_id in article_ids:
                    duplicate_ids += 1
                else:
                    article_ids.add(article_id)
    finally:
        stream.close()
    report = {
        "file": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "columns": header,
        "rows": rows,
        "unique_nonempty_article_ids": len(article_ids),
        "duplicate_article_id_rows_after_first": duplicate_ids,
        "missing_values": missing_counts,
    }
    return report, article_ids


def profile_transactions(path: Path, article_ids: set[str]) -> dict[str, object]:
    stream, reader, header = _header_and_reader(path, TRANSACTION_REQUIRED)
    missing_counts = {name: 0 for name in TRANSACTION_PROFILE_FIELDS}
    rows = 0
    invalid_date_rows = 0
    invalid_price_rows = 0
    unknown_article_rows = 0
    min_date: date | None = None
    max_date: date | None = None
    try:
        for row in reader:
            rows += 1
            for name in TRANSACTION_PROFILE_FIELDS:
                if not (row.get(name) or "").strip():
                    missing_counts[name] += 1

            raw_date = (row.get("t_dat") or "").strip()
            if raw_date:
                try:
                    parsed_date = date.fromisoformat(raw_date)
                    min_date = parsed_date if min_date is None else min(min_date, parsed_date)
                    max_date = parsed_date if max_date is None else max(max_date, parsed_date)
                except ValueError:
                    invalid_date_rows += 1

            raw_price = (row.get("price") or "").strip()
            if raw_price:
                try:
                    price = float(raw_price)
                    if not math.isfinite(price) or price < 0:
                        invalid_price_rows += 1
                except ValueError:
                    invalid_price_rows += 1

            article_id = (row.get("article_id") or "").strip()
            if article_id and article_id not in article_ids:
                unknown_article_rows += 1
    finally:
        stream.close()

    return {
        "file": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "columns": header,
        "rows": rows,
        "date_min": min_date.isoformat() if min_date else None,
        "date_max": max_date.isoformat() if max_date else None,
        "invalid_date_rows": invalid_date_rows,
        "invalid_price_rows": invalid_price_rows,
        "rows_with_article_id_not_in_articles_csv": unknown_article_rows,
        "missing_values": missing_counts,
    }


def profile_dataset(data_dir: Path) -> dict[str, object]:
    """Profile articles.csv and transactions_train.csv without exposing rows."""
    article_report, article_ids = profile_articles(data_dir / "articles.csv")
    transaction_report = profile_transactions(
        data_dir / "transactions_train.csv", article_ids
    )
    return {
        "profile_version": "1.0",
        "data_use_note": (
            "The operator must personally accept the current Kaggle competition "
            "rules. Raw data and row-level records are not copied into this report."
        ),
        "customer_metadata_processed": False,
        "article_images_processed": False,
        "files": {
            "articles": article_report,
            "transactions": transaction_report,
        },
        "privacy_note": (
            "No customer IDs, article IDs, customer ages, postal codes, descriptions, "
            "or individual transaction records are emitted."
        ),
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir", required=True, type=Path,
        help="Directory containing locally accepted articles.csv and transactions_train.csv",
    )
    parser.add_argument(
        "--output", type=Path,
        help="Optional local JSON output path; keep this report out of public GitHub if it contains local hashes.",
    )
    args = parser.parse_args(argv)
    try:
        report = profile_dataset(args.data_dir)
    except (DatasetProfileError, UnicodeError, csv.Error, OSError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Aggregate profile written locally to {args.output}")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
