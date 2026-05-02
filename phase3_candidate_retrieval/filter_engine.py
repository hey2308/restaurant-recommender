"""Hard filtering for location, budget, cuisine, and minimum rating."""

from __future__ import annotations

from phase2_user_preferences.models import PreferenceProfile

from .config import BUDGET_RANGES
from .models import Candidate


def apply_hard_filters(
    candidates: list[Candidate],
    profile: PreferenceProfile,
) -> list[Candidate]:
    out: list[Candidate] = []
    for c in candidates:
        if not _matches_location(c, profile.location):
            continue
        if not _matches_cuisine(c, profile.cuisine):
            continue
        if not _matches_rating(c, profile.min_rating):
            continue
        if not _matches_budget(c, profile.budget):
            continue
        out.append(c)
    return out


def _matches_location(candidate: Candidate, requested_location: str) -> bool:
    req = requested_location.strip().lower()
    if not req:
        return True
    values = [
        (candidate.city or "").lower(),
        (candidate.locality or "").lower(),
        (candidate.location or "").lower(),
    ]
    return any(req in value for value in values if value)


def _matches_cuisine(candidate: Candidate, requested_cuisine: str) -> bool:
    req = requested_cuisine.strip().lower()
    if not req:
        return True
    cuisine = (candidate.cuisine or "").lower()
    return req in cuisine


def _matches_rating(candidate: Candidate, min_rating: float) -> bool:
    if candidate.rating is None:
        return False
    return candidate.rating >= min_rating


def _matches_budget(candidate: Candidate, budget: str) -> bool:
    band = budget.strip().lower()
    if band not in BUDGET_RANGES:
        return True
    cost = candidate.estimated_cost
    if cost is None:
        return False
    lower, upper = BUDGET_RANGES[band]
    if upper is None:
        return cost >= lower
    return lower <= cost <= upper
