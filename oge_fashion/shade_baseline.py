"""Run a reproducible foundation swatch colour-distance baseline."""

from __future__ import annotations

import argparse
import sys

from .shades import (
    SOURCE_COMMIT_URL,
    SOURCE_URL,
    ShadeSourceError,
    fetch_shades,
    rank_shades,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Rank product foundation swatches by CIEDE2000 colour difference. "
            "This does not predict skin-tone or foundation suitability."
        )
    )
    parser.add_argument(
        "--target-hex",
        required=True,
        help="Reference sRGB HEX swatch, e.g. F3CFB3 or #F3CFB3.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=10,
        help="Number of ranked source swatches to display (default: 10).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Source fetch timeout in seconds (default: 30).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.top_k < 1:
        print("Error: --top-k must be at least 1.", file=sys.stderr)
        return 2
    if args.timeout <= 0:
        print("Error: --timeout must be greater than zero.", file=sys.stderr)
        return 2

    try:
        dataset = fetch_shades(timeout=args.timeout)
        matches = rank_shades(dataset, args.target_hex, top_k=args.top_k)
    except (ValueError, ShadeSourceError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print("OGE-Fashion — Foundation shade attribute baseline")
    print(f"Reference swatch: #{args.target_hex.strip().lstrip('#').upper()}")
    print("Metric: CIEDE2000 (lower distance means closer displayed swatch colour)")
    print(f"Unique shade records ranked: {len(dataset.records)}")
    print(f"Source rows inspected: {dataset.source_rows}")
    print(f"Exact duplicate rows removed: {dataset.duplicate_rows_removed}")
    print(f"Rows with missing H/S/V values (not used for ranking): {dataset.hsv_missing_rows}")
    print(f"Source revision: {SOURCE_COMMIT_URL}")
    print()
    print("Rank  Brand / product                                      HEX       Delta E00")
    print("-" * 82)

    for match in matches:
        label = f"{match.shade.brand} / {match.shade.product}"
        print(
            f"{match.rank:>4}  {label[:52]:<52}  "
            f"#{match.shade.hex_value:<6}  {match.delta_e_2000:>9.4f}"
        )

    print()
    print("Interpretation limit:")
    print(
        "This ranks historical product swatches by displayed colour only. "
        "It does not estimate skin colour, foundation suitability, or personal preference."
    )
    print(f"Data source: {SOURCE_URL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
