"""Map arbitrary dataset columns to a canonical restaurant schema."""

from __future__ import annotations

from typing import Any

from . import config
from . import preprocessor


# Lowercase keys -> canonical field name
_CANONICAL_ALIASES: dict[str, str] = {
    # name
    "restaurant name": "name",
    "restaurant_name": "name",
    "name": "name",
    "title": "name",
    # location
    "city": "city",
    "listed_in(city)": "city",
    "location": "locality",
    "area": "locality",
    "locality": "locality",
    "locality verbose": "locality",
    "address": "locality",
    # cuisine
    "cuisines": "cuisine",
    "cuisine": "cuisine",
    # cost
    "average cost for two": "estimated_cost",
    "average_cost_for_two": "estimated_cost",
    "cost": "estimated_cost",
    "approx_cost(for two people)": "estimated_cost",
    "approx cost(for two people)": "estimated_cost",
    "approx_cost": "estimated_cost",
    # rating
    "aggregate rating": "rating",
    "aggregate_rating": "rating",
    "rate": "rating",
    "rating": "rating",
    "ratings": "rating",
    # optional metadata for tags
    "has online delivery": "has_online_delivery",
    "has table booking": "has_table_booking",
    "is delivering now": "is_delivering_now",
    "online_order": "has_online_delivery",
    "book_table": "has_table_booking",
}


def _normalize_key(key: str) -> str:
    return key.strip().lower().replace("\n", " ")


def _resolve_column_map(sample_keys: list[str]) -> dict[str, str]:
    """Map actual dataset column name -> canonical name."""
    mapping: dict[str, str] = {}
    for raw in sample_keys:
        norm = _normalize_key(raw)
        if norm in _CANONICAL_ALIASES:
            mapping[raw] = _CANONICAL_ALIASES[norm]
    return mapping


def extract_features(
    row: dict[str, Any],
    column_map: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Produce a canonical record:

    - name, city, locality, location (combined), cuisine, estimated_cost, rating
    - tags: list of strings from known flags + optional freeform
    - data_quality: flags for bounds / missing core fields
    """
    if column_map is None:
        column_map = _resolve_column_map(list(row.keys()))

    def get_canonical(canonical: str) -> Any:
        for raw, c in column_map.items():
            if c == canonical and raw in row:
                return row[raw]
        return None

    name = preprocessor.clean_str(get_canonical("name"))
    city = preprocessor.clean_str(get_canonical("city"))
    locality = preprocessor.clean_str(get_canonical("locality"))
    cuisine = preprocessor.normalize_cuisine(get_canonical("cuisine"))

    rating_raw = get_canonical("rating")
    cost_raw = get_canonical("estimated_cost")

    rating = preprocessor.parse_rating(rating_raw)
    estimated_cost = preprocessor.parse_cost(cost_raw)

    location_parts = [p for p in (locality, city) if p]
    location_combined = ", ".join(location_parts) if location_parts else None

    tags: list[str] = []
    for raw, canon in column_map.items():
        if canon in ("has_online_delivery", "has_table_booking", "is_delivering_now"):
            v = row.get(raw)
            if v in (True, 1, "1", "yes", "Yes", "YES", "true", "True"):
                tags.append(canon)

    data_quality: dict[str, Any] = {
        "missing_name": name is None,
        "missing_location": city is None and locality is None,
        "missing_cuisine": cuisine is None,
        "missing_rating": rating is None,
        "missing_cost": estimated_cost is None,
    }

    if rating is not None:
        if rating < config.RATING_MIN or rating > config.RATING_MAX:
            data_quality["rating_out_of_bounds"] = True
            rating = None
        else:
            data_quality["rating_out_of_bounds"] = False

    if estimated_cost is not None:
        if estimated_cost < config.COST_MIN or estimated_cost > config.COST_MAX:
            data_quality["cost_out_of_bounds"] = True
            estimated_cost = None
        else:
            data_quality["cost_out_of_bounds"] = False

    return {
        "name": name,
        "city": city,
        "locality": locality,
        "location": location_combined,
        "cuisine": cuisine,
        "estimated_cost": estimated_cost,
        "rating": rating,
        "tags": tags,
        "data_quality": data_quality,
    }


def build_column_map_from_sample(row: dict[str, Any]) -> dict[str, str]:
    return _resolve_column_map(list(row.keys()))
