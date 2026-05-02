"""Read candidate rows from Phase 1 SQLite store."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .models import Candidate


def connect(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(f"Phase 1 DB not found: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all_candidates(conn: sqlite3.Connection) -> list[Candidate]:
    sql = """
    SELECT source_row_index, name, city, locality, location, cuisine,
           estimated_cost, rating, tags
    FROM restaurants
    WHERE name IS NOT NULL AND TRIM(name) <> ''
    """
    rows = conn.execute(sql).fetchall()
    candidates: list[Candidate] = []
    for row in rows:
        tags = _parse_tags(row["tags"])
        candidates.append(
            Candidate(
                source_row_index=row["source_row_index"],
                name=row["name"],
                city=row["city"],
                locality=row["locality"],
                location=row["location"],
                cuisine=row["cuisine"],
                estimated_cost=_to_float(row["estimated_cost"]),
                rating=_to_float(row["rating"]),
                tags=tags,
            )
        )
    return candidates


def _parse_tags(raw: Any) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, list):
        return [str(x).strip().lower() for x in raw if str(x).strip()]
    if isinstance(raw, str):
        s = raw.strip()
        if not s:
            return []
        try:
            loaded = json.loads(s)
            if isinstance(loaded, list):
                return [str(x).strip().lower() for x in loaded if str(x).strip()]
        except json.JSONDecodeError:
            # fallback if tags were stored as plain comma-separated text
            return [p.strip().lower() for p in s.split(",") if p.strip()]
    return []


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
