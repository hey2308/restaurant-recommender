"""Parse and normalize LLM JSON into Phase 4 output contract."""

from __future__ import annotations

import json
from typing import Any


def parse_llm_response(
    raw_response: str,
    *,
    profile: dict[str, Any],
    top_n: int,
) -> dict[str, Any]:
    data = json.loads(raw_response)
    summary = str(data.get("summary", "")).strip() or "Top recommendations generated."
    items = data.get("recommendations", [])

    if not isinstance(items, list):
        raise ValueError("LLM response field 'recommendations' must be a list.")

    normalized: list[dict[str, Any]] = []
    for idx, item in enumerate(items[:top_n], start=1):
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "rank": int(item.get("rank", idx)),
                "name": str(item.get("name", "Unknown")),
                "why_recommended": str(item.get("why_recommended", "")).strip(),
                "rating": item.get("rating"),
                "estimated_cost": item.get("estimated_cost"),
                "cuisine": item.get("cuisine"),
                "location": item.get("location"),
                "source_row_index": item.get("source_row_index"),
            }
        )

    if not normalized:
        raise ValueError("No recommendations found in LLM response.")

    return {
        "profile": profile,
        "summary": summary,
        "recommendations": normalized,
        "meta": {"mode": "llm"},
    }

