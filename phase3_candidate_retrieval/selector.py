"""Top-N selection utilities."""

from __future__ import annotations

from .models import Candidate


def select_top_n(candidates: list[Candidate], n: int = 25) -> list[Candidate]:
    if n <= 0:
        return []
    
    # First, dedupe by restaurant name (keep highest scoring instance)
    seen_names = {}
    deduped = []
    for c in candidates:
        name = c.name.strip().lower()
        if name not in seen_names:
            seen_names[name] = c
            deduped.append(c)
    
    # Sort by score, then rating, then cost
    ordered = sorted(
        deduped,
        key=lambda c: (
            c.score,
            (c.rating if c.rating is not None else -1.0),
            _safe_neg_cost(c.estimated_cost),
        ),
        reverse=True,
    )
    return ordered[:n]


def _safe_neg_cost(cost: float | None) -> float:
    if cost is None:
        return -10**9
    # Lower cost gets slight preference when scores tie.
    return -cost
