"""Structured preference profile produced by Phase 2."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PreferenceProfile:
    """Validated, normalized user preferences for downstream phases."""

    location: str
    budget: str  # "low" | "medium" | "high"
    cuisine: str
    min_rating: float
    optional_tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "location": self.location,
            "budget": self.budget,
            "cuisine": self.cuisine,
            "min_rating": self.min_rating,
            "optional_tags": list(self.optional_tags),
        }
