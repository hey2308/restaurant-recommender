"""Orchestrate load → extract → store for Phase 1."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Iterator

from . import config
from . import feature_extractor
from . import loader
from . import store


def run_pipeline(
    *,
    split: str | None = None,
    streaming: bool = True,
    limit: int | None = None,
    sqlite_path: Path | None = None,
    csv_path: Path | None = None,
    reset_db: bool = True,
) -> dict[str, Any]:
    """
    Load dataset, map columns from first row, clean rows, write SQLite (+ CSV).

    Returns a small summary dict (rows_processed, db_path, csv_path).
    """
    split = split or config.DEFAULT_SPLIT
    sqlite_path = sqlite_path or config.DEFAULT_SQLITE_PATH
    csv_path = csv_path or config.DEFAULT_CSV_PATH

    dataset = loader.load_zomato(split=split, streaming=streaming)

    if reset_db:
        conn = store.reset_database(sqlite_path)
    else:
        conn = store.connect(sqlite_path)
        store.init_schema(conn)

    column_map: dict[str, str] | None = None

    def cleaned_rows() -> Iterator[dict[str, Any]]:
        nonlocal column_map
        idx = 0
        for row in loader.iter_rows(dataset):
            if column_map is None:
                column_map = feature_extractor.build_column_map_from_sample(row)
            rec = feature_extractor.extract_features(row, column_map)
            rec["source_row_index"] = idx
            idx += 1
            yield rec
            if limit is not None and idx >= limit:
                break

    # Batch insert in chunks to balance memory and commit frequency
    chunk: list[dict[str, Any]] = []
    total = 0
    chunk_size = 500
    for rec in cleaned_rows():
        chunk.append(rec)
        if len(chunk) >= chunk_size:
            total += store.insert_batch(conn, chunk)
            chunk.clear()
    if chunk:
        total += store.insert_batch(conn, chunk)

    store.export_csv(conn, csv_path)
    conn.close()

    return {
        "rows_processed": total,
        "sqlite_path": str(sqlite_path.resolve()),
        "csv_path": str(csv_path.resolve()),
        "column_map": column_map or {},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 1: ingest Zomato dataset into SQLite/CSV.")
    parser.add_argument("--split", default=config.DEFAULT_SPLIT, help="Dataset split name")
    parser.add_argument("--no-streaming", action="store_true", help="Load full split (high memory)")
    parser.add_argument("--limit", type=int, default=None, help="Max rows to process (debug)")
    parser.add_argument("--db", type=Path, default=None, help="SQLite output path")
    parser.add_argument("--csv", type=Path, default=None, help="CSV export path")
    parser.add_argument("--append", action="store_true", help="Do not delete existing DB")
    args = parser.parse_args()

    summary = run_pipeline(
        split=args.split,
        streaming=not args.no_streaming,
        limit=args.limit,
        sqlite_path=args.db,
        csv_path=args.csv,
        reset_db=not args.append,
    )
    print("Phase 1 pipeline complete.")
    for k, v in summary.items():
        if k == "column_map":
            print(f"  {k}: {v}")
        else:
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
