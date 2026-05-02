"""Prompt construction for ranked explainable recommendations."""

from __future__ import annotations

import json
from typing import Any


def build_system_prompt() -> str:
    return (
        "You are a restaurant recommendation assistant. "
        "Given user preferences and shortlisted candidates, return ranked recommendations. "
        "Be faithful to candidate facts only. Do not invent restaurants or attributes. "
        "Respond strictly in JSON with keys: summary, recommendations. "
        "Each recommendation item must include: rank, name, why_recommended, rating, "
        "estimated_cost, cuisine, location, source_row_index."
    )


def build_user_prompt(
    profile: dict[str, Any],
    candidates: list[dict[str, Any]],
    *,
    top_n: int,
) -> str:
    payload = {
        "task": (
            f"Rank top {top_n} restaurants for this user and explain each pick in 1-2 concise lines. "
            "Use only the supplied candidates."
        ),
        "user_profile": profile,
        "candidates": candidates,
        "output_schema": {
            "summary": "string",
            "recommendations": [
                {
                    "rank": "integer starting at 1",
                    "name": "string",
                    "why_recommended": "string",
                    "rating": "number or null",
                    "estimated_cost": "number or null",
                    "cuisine": "string or null",
                    "location": "string or null",
                    "source_row_index": "integer or null",
                }
            ],
        },
    }
    return json.dumps(payload, ensure_ascii=True, indent=2)

