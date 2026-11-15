"""Pinned source loader and duplicate-aware foundation shade ranking."""

from __future__ import annotations

import csv
import io
import urllib.error
import urllib.request
from dataclasses import dataclass

from .color import delta_e_2000, hex_to_lab

UPSTREAM_REVISION = "3458c304647bef28ff2dd53f808bee3507f2a4f1"
SOURCE_URL = (
    "https://raw.githubusercontent.com/the-pudding/data/"
    f"{UPSTREAM_REVISION}/makeup-shades/shades.csv"
)
SOURCE_COMMIT_URL = (
    "https://github.com/the-pudding/data/commit/"
    f"{UPSTREAM_REVISION}"
)
MAX_SOURCE_BYTES = 2_000_000
USER_AGENT = "OGE-Fashion-Research/0.1 (+https://github.com/faisalkhan8/OGE-Fashion)"


@dataclass(frozen=True)
class ShadeRecord:
    """One unique brand/product/HEX record from the source CSV."""

    source_row: int
    brand: str
    product: str
    hex_value: str
    group: str


@dataclass(frozen=True)
class ShadeDataset:
    """Validated shade records plus source-quality diagnostics."""

    records: tuple[ShadeRecord, ...]
    source_rows: int
    duplicate_rows_removed: int
    hsv_missing_rows: int


@dataclass(frozen=True)
class ShadeMatch:
    """One shade ranked against a target colour."""

    rank: int
    shade: ShadeRecord
    delta_e_2000: float


class ShadeSourceError(RuntimeError):
    """Raised when the upstream shade source cannot be fetched or parsed."""


def parse_shade_csv(csv_text: str) -> ShadeDataset:
    """Parse the source CSV, ignoring its disputed L field.

    Exact duplicate keys are defined as brand + product + HEX (case
    insensitive for HEX). The first source occurrence is retained and its
    row number is preserved. H/S/V values are quality diagnostics only.
    """
    if not isinstance(csv_text, str):
        raise TypeError("CSV content must be text.")

    reader = csv.DictReader(io.StringIO(csv_text))
    required = {"brand", "product", "hex", "group", "H", "S", "V"}
    headers = set(reader.fieldnames or ())
    missing = required - headers
    if missing:
        raise ShadeSourceError(
            "Source CSV is missing required columns: "
            + ", ".join(sorted(missing))
        )

    records: list[ShadeRecord] = []
    seen: set[tuple[str, str, str]] = set()
    source_rows = 0
    duplicates = 0
    hsv_missing = 0

    for source_row, row in enumerate(reader, start=2):
        if not row or all(value is None or value.strip() == "" for value in row.values()):
            continue

        source_rows += 1
        brand = (row.get("brand") or "").strip()
        product = (row.get("product") or "").strip()
        hex_value = (row.get("hex") or "").strip().lstrip("#")
        group = (row.get("group") or "").strip()

        if not brand or not product:
            raise ShadeSourceError(
                f"Source row {source_row} has a blank brand or product."
            )
        if len(hex_value) != 6 or any(
            character not in "0123456789abcdefABCDEF"
            for character in hex_value
        ):
            raise ShadeSourceError(
                f"Source row {source_row} contains invalid HEX value {hex_value!r}."
            )

        if any(
            (row.get(field) or "").strip().upper() in {"", "NA", "N/A", "NULL"}
            for field in ("H", "S", "V")
        ):
            hsv_missing += 1

        duplicate_key = (brand.casefold(), product.casefold(), hex_value.casefold())
        if duplicate_key in seen:
            duplicates += 1
            continue

        seen.add(duplicate_key)
        records.append(
            ShadeRecord(
                source_row=source_row,
                brand=brand,
                product=product,
                hex_value=hex_value.upper(),
                group=group,
            )
        )

    if not records:
        raise ShadeSourceError("Source CSV contains no valid shade records.")

    return ShadeDataset(
        records=tuple(records),
        source_rows=source_rows,
        duplicate_rows_removed=duplicates,
        hsv_missing_rows=hsv_missing,
    )


def fetch_shades(timeout: float = 30.0) -> ShadeDataset:
    """Fetch the pinned source CSV at runtime; do not persist it locally."""
    request = urllib.request.Request(
        SOURCE_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/csv",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw_content = response.read(MAX_SOURCE_BYTES + 1)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise ShadeSourceError(f"Could not fetch the shade source: {exc}") from exc

    if len(raw_content) > MAX_SOURCE_BYTES:
        raise ShadeSourceError(
            f"Shade source exceeded the {MAX_SOURCE_BYTES} byte safety limit."
        )

    try:
        csv_text = raw_content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ShadeSourceError("Shade source is not valid UTF-8.") from exc

    return parse_shade_csv(csv_text)


def rank_shades(
    dataset: ShadeDataset,
    target_hex: str,
    top_k: int = 10,
) -> list[ShadeMatch]:
    """Rank unique source swatches by CIEDE2000 distance to a target HEX.

    The metric compares displayed source swatch colours only. It is not a
    skin-tone estimator, product-quality score, or user-preference model.
    """
    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    target_lab = hex_to_lab(target_hex)
    scored: list[tuple[ShadeRecord, float]] = []

    for shade in dataset.records:
        shade_lab = hex_to_lab(shade.hex_value)
        distance = delta_e_2000(target_lab, shade_lab)
        scored.append((shade, distance))

    scored.sort(
        key=lambda item: (
            item[1],
            item[0].brand.casefold(),
            item[0].product.casefold(),
            item[0].hex_value.casefold(),
            item[0].source_row,
        )
    )

    return [
        ShadeMatch(rank=index, shade=shade, delta_e_2000=distance)
        for index, (shade, distance) in enumerate(scored[:top_k], start=1)
    ]
