"""Guardrails for prompt size and safe recommendation fallback."""

from __future__ import annotations

from typing import Any

from . import config


def clamp_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Limit candidate count for predictable token usage."""
    return candidates[: config.MAX_CANDIDATES_IN_PROMPT]


def enforce_prompt_size(prompt: str) -> str:
    """Trim oversized prompts to avoid model request failure."""
    if len(prompt) <= config.MAX_PROMPT_CHARS:
        return prompt
    return prompt[: config.MAX_PROMPT_CHARS] + "\n\n[Prompt truncated by guardrail]"


def build_fallback_recommendations(
    profile: dict[str, Any],
    candidates: list[dict[str, Any]],
    *,
    top_n: int,
    reason: str,
) -> dict[str, Any]:
    """Deterministic ranking fallback if LLM call/parsing fails."""
    ranked = sorted(
        candidates,
        key=lambda c: (
            float(c.get("score", 0.0)),
            float(c.get("rating", 0.0) or 0.0),
        ),
        reverse=True,
    )[:top_n]

    recommendations: list[dict[str, Any]] = []
    for idx, item in enumerate(ranked, start=1):
        recommendations.append(
            {
                "rank": idx,
                "name": item.get("name", "Unknown"),
                "why_recommended": (
                    "Selected by fallback ranking due to LLM unavailability. "
                    "Candidate has comparatively strong score/rating for your filters."
                ),
                "rating": item.get("rating"),
                "estimated_cost": item.get("estimated_cost"),
                "cuisine": item.get("cuisine"),
                "location": item.get("location"),
                "source_row_index": item.get("source_row_index"),
            }
        )

    return {
        "profile": profile,
        "summary": "Fallback recommendations generated without LLM narrative refinement.",
        "recommendations": recommendations,
        "meta": {"mode": "fallback", "reason": reason},
    }

