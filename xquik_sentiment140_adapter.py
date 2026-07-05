"""Convert Xquik tweet exports into Sentiment140-style CSV rows."""

from __future__ import annotations

import argparse
import csv
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path


SENTIMENT140_COLUMNS = ["target", "ids", "date", "flag", "user", "text"]

COLUMN_ALIASES = {
    "ids": ("ids", "id", "tweet_id", "post_id", "status_id"),
    "date": ("date", "created_at", "timestamp", "published_at"),
    "flag": ("flag", "query", "keyword", "search_term"),
    "user": ("user", "username", "screen_name", "author", "handle"),
    "text": ("text", "full_text", "tweet_text", "content", "body"),
    "target": ("target", "sentiment", "label", "polarity"),
}

TARGET_ALIASES = {
    "0": "0",
    "negative": "0",
    "neg": "0",
    "-1": "0",
    "4": "4",
    "positive": "4",
    "pos": "4",
    "1": "4",
}


def _normalize_key(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def _index_row(row: Mapping[str, object]) -> dict[str, object]:
    return {_normalize_key(str(key)): value for key, value in row.items()}


def _first_value(row: Mapping[str, object], aliases: Sequence[str]) -> str:
    for alias in aliases:
        value = row.get(alias)
        if value is not None and str(value).strip() and str(value).lower() != "nan":
            return str(value).strip()
    return ""


def sentiment140_target(value: object) -> str | None:
    """Map common binary sentiment labels to Sentiment140 targets."""
    normalized = str(value).strip().lower()
    if not normalized:
        return None
    return TARGET_ALIASES.get(normalized)


def normalize_xquik_row(row: Mapping[str, object], *, include_unlabeled: bool = False) -> dict[str, str] | None:
    indexed_row = _index_row(row)
    text = _first_value(indexed_row, COLUMN_ALIASES["text"])
    if not text:
        return None

    target_value = _first_value(indexed_row, COLUMN_ALIASES["target"])
    target = sentiment140_target(target_value)
    if target is None and not include_unlabeled:
        return None

    return {
        "target": target or "",
        "ids": _first_value(indexed_row, COLUMN_ALIASES["ids"]),
        "date": _first_value(indexed_row, COLUMN_ALIASES["date"]),
        "flag": _first_value(indexed_row, COLUMN_ALIASES["flag"]) or "XQUIK_EXPORT",
        "user": _first_value(indexed_row, COLUMN_ALIASES["user"]),
        "text": text,
    }


def normalize_xquik_rows(
    rows: Iterable[Mapping[str, object]],
    *,
    include_unlabeled: bool = False,
) -> list[dict[str, str]]:
    normalized_rows = []
    for row in rows:
        normalized_row = normalize_xquik_row(row, include_unlabeled=include_unlabeled)
        if normalized_row is not None:
            normalized_rows.append(normalized_row)
    return normalized_rows


def convert_csv(input_path: Path, output_path: Path, *, include_unlabeled: bool = False) -> int:
    with input_path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        rows = normalize_xquik_rows(reader, include_unlabeled=include_unlabeled)

    with output_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=SENTIMENT140_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert Xquik tweet exports to Sentiment140 CSV format.")
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument(
        "--include-unlabeled",
        action="store_true",
        help="Keep rows without positive or negative labels with an empty target column.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    count = convert_csv(args.input_csv, args.output_csv, include_unlabeled=args.include_unlabeled)
    print(f"Wrote {count} Sentiment140 rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
