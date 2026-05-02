"""Response formatter for card/table/json presentation structures."""

from __future__ import annotations

from typing import Any


def to_card_view(recommendations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for rec in recommendations:
        cards.append(
            {
                "title": rec.get("name", "Unknown"),
                "subtitle": f"Rank #{rec.get('rank', '-')}",
                "rating": rec.get("rating"),
                "estimated_cost": rec.get("estimated_cost"),
                "cuisine": rec.get("cuisine"),
                "location": rec.get("location"),
                "explanation": rec.get("why_recommended", ""),
            }
        )
    return cards


def to_table_view(recommendations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rec in recommendations:
        rows.append(
            {
                "rank": rec.get("rank"),
                "name": rec.get("name"),
                "rating": rec.get("rating"),
                "estimated_cost": rec.get("estimated_cost"),
                "cuisine": rec.get("cuisine"),
                "location": rec.get("location"),
            }
        )
    return rows


def build_presentation_payload(phase4_payload: dict[str, Any]) -> dict[str, Any]:
    profile = phase4_payload.get("profile", {})
    summary = phase4_payload.get("summary", "")
    recommendations = phase4_payload.get("recommendations", [])
    meta = phase4_payload.get("meta", {})

    return {
        "profile": profile,
        "summary": summary,
        "cards": to_card_view(recommendations),
        "table_rows": to_table_view(recommendations),
        "raw_recommendations": recommendations,
        "meta": meta,
    }

