"""Validate normalized preference fields and build PreferenceProfile."""

from __future__ import annotations

from typing import Any

from .models import PreferenceProfile
from .normalizer import BUDGET_CANONICAL, normalize_preferences


DEFAULT_MIN_RATING = 3.0


def validate_preferences(
    data: dict[str, Any],
    *,
    apply_defaults: bool = True,
) -> tuple[PreferenceProfile | None, list[str]]:
    """
    Validate normalized or raw preference dict.

    If ``apply_defaults`` is True, empty ``min_rating`` defaults to DEFAULT_MIN_RATING.
    Returns (profile, errors). When errors is non-empty, profile is None.
    """
    normalized = normalize_preferences(data)
    errors: list[str] = []

    location = normalized.get("location") or ""
    if not location:
        errors.append("Location is required.")

    budget = (normalized.get("budget") or "").strip().lower()
    if not budget:
        errors.append("Budget is required (low, medium, or high).")
    elif budget not in BUDGET_CANONICAL:
        errors.append(
            f"Budget must be one of: {', '.join(sorted(BUDGET_CANONICAL))}."
        )

    cuisine = normalized.get("cuisine") or ""
    if not cuisine:
        errors.append("Cuisine is required.")

    min_rating_val: float | None = None
    mr = normalized.get("min_rating")
    if mr is None or (isinstance(mr, str) and not str(mr).strip()):
        if apply_defaults:
            min_rating_val = DEFAULT_MIN_RATING
        else:
            errors.append("Minimum rating is required.")
    else:
        try:
            min_rating_val = float(mr)
        except (TypeError, ValueError):
            errors.append("Minimum rating must be a number.")
            min_rating_val = None

    if min_rating_val is not None:
        if min_rating_val < 0.0 or min_rating_val > 5.0:
            errors.append("Minimum rating must be between 0 and 5.")

    tags = normalized.get("optional_tags") or []
    if not isinstance(tags, list):
        tags = []

    if errors:
        return None, errors

    profile = PreferenceProfile(
        location=location.strip(),
        budget=budget,
        cuisine=str(cuisine).strip(),
        min_rating=min_rating_val if min_rating_val is not None else DEFAULT_MIN_RATING,
        optional_tags=[str(t).strip().lower() for t in tags if str(t).strip()],
    )
    return profile, []
