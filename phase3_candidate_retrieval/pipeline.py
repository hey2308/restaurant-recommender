"""Phase 3 pipeline: retrieve candidates, hard filter, score, and select top-N."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from phase2_user_preferences.models import PreferenceProfile
from phase2_user_preferences.validation import validate_preferences

from . import config
from .filter_engine import apply_hard_filters
from .repository import connect, fetch_all_candidates
from .scoring import score_candidates
from .selector import select_top_n


def run_phase3(
    profile: PreferenceProfile,
    *,
    db_path: Path | None = None,
    top_n: int = 25,
) -> dict[str, Any]:
    db = db_path or config.DEFAULT_PHASE1_DB
    conn = connect(db)
    try:
        raw_candidates = fetch_all_candidates(conn)
    finally:
        conn.close()

    filtered = apply_hard_filters(raw_candidates, profile)
    scored = score_candidates(filtered, profile)
    selected = select_top_n(scored, n=top_n)

    return {
        "profile": profile.to_dict(),
        "total_candidates": len(raw_candidates),
        "filtered_candidates": len(filtered),
        "selected_candidates": len(selected),
        "candidates": [c.to_dict() for c in selected],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 3 candidate retrieval and filtering.")
    parser.add_argument("--location", required=True, help="e.g. Delhi")
    parser.add_argument("--budget", required=True, help="low | medium | high")
    parser.add_argument("--cuisine", required=True, help="e.g. Chinese")
    parser.add_argument("--min-rating", default="3.0", help="minimum rating [0,5]")
    parser.add_argument(
        "--optional-tags",
        default="",
        help="comma-separated optional tags (e.g. family-friendly,quick service)",
    )
    parser.add_argument("--top-n", type=int, default=25, help="number of candidates to shortlist")
    parser.add_argument("--db", type=Path, default=config.DEFAULT_PHASE1_DB, help="phase1 SQLite path")
    parser.add_argument(
        "--out",
        type=Path,
        default=config.DEFAULT_OUTPUT_JSON,
        help="where to write shortlisted candidates json",
    )
    args = parser.parse_args()

    payload = {
        "location": args.location,
        "budget": args.budget,
        "cuisine": args.cuisine,
        "min_rating": args.min_rating,
        "optional_tags": args.optional_tags,
    }
    profile, errors = validate_preferences(payload)
    if errors:
        raise SystemExit("Invalid preferences: " + "; ".join(errors))
    assert profile is not None

    result = run_phase3(profile, db_path=args.db, top_n=args.top_n)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("Phase 3 pipeline complete.")
    print(f"  total_candidates: {result['total_candidates']}")
    print(f"  filtered_candidates: {result['filtered_candidates']}")
    print(f"  selected_candidates: {result['selected_candidates']}")
    print(f"  output_json: {args.out.resolve()}")


if __name__ == "__main__":
    main()
