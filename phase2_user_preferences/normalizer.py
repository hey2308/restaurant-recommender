"""Map raw user input to canonical labels and field shapes."""

from __future__ import annotations

import re
from typing import Any

# Canonical budget bands (aligned with problem statement)
BUDGET_CANONICAL = frozenset({"low", "medium", "high"})

_BUDGET_ALIASES: dict[str, str] = {
    "low": "low",
    "cheap": "low",
    "budget": "low",
    "economy": "low",
    "medium": "medium",
    "mid": "medium",
    "moderate": "medium",
    "average": "medium",
    "high": "high",
    "expensive": "high",
    "premium": "high",
    "luxury": "high",
}

def _split_tags(raw: str | None) -> list[str]:
    if not raw or not str(raw).strip():
        return []
    parts = re.split(r"[,;\n]+", str(raw))
    return [p.strip().lower() for p in parts if p.strip()]


def normalize_preferences(raw: dict[str, Any]) -> dict[str, Any]:
    """
    Normalize form or JSON body fields into a flat dict for validation.

    Expected keys (all optional until validation): location, budget, cuisine,
    min_rating, optional_tags (list or comma-separated string).
    """
    out: dict[str, Any] = {}

    loc = raw.get("location")
    out["location"] = str(loc).strip() if loc is not None else ""

    budget = raw.get("budget")
    if budget is not None:
        b = str(budget).strip().lower()
        out["budget"] = _BUDGET_ALIASES.get(b, b)
    else:
        out["budget"] = ""

    cuisine = raw.get("cuisine")
    out["cuisine"] = str(cuisine).strip() if cuisine is not None else ""

    mr = raw.get("min_rating")
    if mr is None or (isinstance(mr, str) and not str(mr).strip()):
        out["min_rating"] = None
    else:
        out["min_rating"] = mr

    tags: list[str] = []
    ot = raw.get("optional_tags")
    if isinstance(ot, list):
        tags = [str(t).strip().lower() for t in ot if str(t).strip()]
    elif isinstance(ot, str):
        tags = _split_tags(ot)
    elif ot is not None:
        tags = _split_tags(str(ot))

    # De-dupe preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    out["optional_tags"] = unique

    return out
