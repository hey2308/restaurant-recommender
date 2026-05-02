"""Optional weighted scoring helper before LLM handoff."""

from __future__ import annotations

from phase2_user_preferences.models import PreferenceProfile

from .config import BUDGET_RANGES, DEFAULT_WEIGHTS
from .models import Candidate


def score_candidates(
    candidates: list[Candidate],
    profile: PreferenceProfile,
    *,
    weights: dict[str, float] | None = None,
) -> list[Candidate]:
    use_weights = dict(DEFAULT_WEIGHTS)
    if weights:
        use_weights.update(weights)

    for c in candidates:
        rating_component = _rating_score(c.rating)
        cost_component = _cost_fit_score(c.estimated_cost, profile.budget)
        tag_component = _tag_match_score(c.tags, profile.optional_tags)
        location_component = _location_bonus(c, profile.location)

        breakdown = {
            "rating": rating_component * use_weights["rating"],
            "cost_fit": cost_component * use_weights["cost_fit"],
            "tag_match": tag_component * use_weights["tag_match"],
            "location_bonus": location_component * use_weights["location_bonus"],
        }
        c.score_breakdown = breakdown
        c.score = round(sum(breakdown.values()), 6)
    return candidates


def _rating_score(rating: float | None) -> float:
    if rating is None:
        return 0.0
    clamped = min(max(rating, 0.0), 5.0)
    return clamped / 5.0


def _cost_fit_score(cost: float | None, budget: str) -> float:
    if cost is None:
        return 0.0
    if budget not in BUDGET_RANGES:
        return 0.5
    lower, upper = BUDGET_RANGES[budget]
    if upper is None:
        if cost >= lower:
            return 1.0
        # Slight penalty if near threshold.
        return max(0.0, 1.0 - ((lower - cost) / max(lower, 1.0)))
    if lower <= cost <= upper:
        return 1.0
    # Distance-based soft penalty for values outside the band.
    if cost < lower:
        return max(0.0, 1.0 - ((lower - cost) / max(lower, 1.0)))
    return max(0.0, 1.0 - ((cost - upper) / max(upper, 1.0)))


def _tag_match_score(candidate_tags: list[str], requested_tags: list[str]) -> float:
    if not requested_tags:
        return 1.0
    if not candidate_tags:
        return 0.0
    requested = {t.strip().lower() for t in requested_tags if t.strip()}
    if not requested:
        return 1.0
    candidate = {t.strip().lower() for t in candidate_tags if t.strip()}
    if not candidate:
        return 0.0
    matched = requested.intersection(candidate)
    return len(matched) / len(requested)


def _location_bonus(candidate: Candidate, requested_location: str) -> float:
    req = requested_location.strip().lower()
    if not req:
        return 0.0
    city = (candidate.city or "").strip().lower()
    locality = (candidate.locality or "").strip().lower()
    if req == locality:
        return 1.0
    if req == city:
        return 0.8
    if req in (candidate.location or "").lower():
        return 0.5
    return 0.0
