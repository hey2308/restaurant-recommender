"""Persist cleaned restaurant records to SQLite and optional CSV."""

from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path
from typing import Any, Iterable

from . import config


CREATE_SQL = """
CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_row_index INTEGER,
    name TEXT,
    city TEXT,
    locality TEXT,
    location TEXT,
    cuisine TEXT,
    estimated_cost REAL,
    rating REAL,
    tags TEXT,
    data_quality TEXT
);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(CREATE_SQL)
    conn.commit()


def insert_batch(
    conn: sqlite3.Connection,
    records: Iterable[dict[str, Any]],
) -> int:
    """Insert records; returns count inserted."""
    sql = """
    INSERT INTO restaurants (
        source_row_index, name, city, locality, location, cuisine,
        estimated_cost, rating, tags, data_quality
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    n = 0
    cur = conn.cursor()
    for rec in records:
        dq = rec.get("data_quality") or {}
        cur.execute(
            sql,
            (
                rec.get("source_row_index"),
                rec.get("name"),
                rec.get("city"),
                rec.get("locality"),
                rec.get("location"),
                rec.get("cuisine"),
                rec.get("estimated_cost"),
                rec.get("rating"),
                json.dumps(rec.get("tags") or []),
                json.dumps(dq),
            ),
        )
        n += 1
    conn.commit()
    return n


def export_csv(conn: sqlite3.Connection, csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    cur = conn.execute(
        """
        SELECT source_row_index, name, city, locality, location, cuisine,
               estimated_cost, rating, tags, data_quality
        FROM restaurants
        ORDER BY id
        """
    )
    rows = cur.fetchall()
    colnames = [d[0] for d in cur.description]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(colnames)
        w.writerows(rows)


def reset_database(db_path: Path) -> sqlite3.Connection:
    """Remove previous DB file and return a fresh connection with schema."""
    if db_path.exists():
        db_path.unlink()
    conn = connect(db_path)
    init_schema(conn)
    return conn
