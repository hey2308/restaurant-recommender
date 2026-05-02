"""Build user-facing explanation text for why recommendations were picked."""

from __future__ import annotations

from typing import Any


def build_explanation_lines(
    profile: dict[str, Any],
    recommendations: list[dict[str, Any]],
) -> list[str]:
    lines: list[str] = []
    lines.append("Why these restaurants were recommended")
    lines.append(
        "Preferences considered: "
        f"location={profile.get('location')}, "
        f"budget={profile.get('budget')}, "
        f"cuisine={profile.get('cuisine')}, "
        f"min_rating={profile.get('min_rating')}"
    )
    if profile.get("optional_tags"):
        lines.append(f"Optional tags: {', '.join(profile.get('optional_tags', []))}")
    lines.append("")

    for rec in recommendations:
        lines.append(f"{rec.get('rank', '-')}. {rec.get('name', 'Unknown')}")
        lines.append(f"   Reason: {rec.get('why_recommended', 'No reason provided.')}")
        lines.append(
            "   Details: "
            f"rating={rec.get('rating')}, "
            f"cost={rec.get('estimated_cost')}, "
            f"cuisine={rec.get('cuisine')}, "
            f"location={rec.get('location')}"
        )
        lines.append("")
    return lines

