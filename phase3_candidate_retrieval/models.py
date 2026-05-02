"""Domain models for Phase 3 candidates."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Candidate:
    source_row_index: int | None
    name: str
    city: str | None
    locality: str | None
    location: str | None
    cuisine: str | None
    estimated_cost: float | None
    rating: float | None
    tags: list[str] = field(default_factory=list)
    score: float = 0.0
    score_breakdown: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_row_index": self.source_row_index,
            "name": self.name,
            "city": self.city,
            "locality": self.locality,
            "location": self.location,
            "cuisine": self.cuisine,
            "estimated_cost": self.estimated_cost,
            "rating": self.rating,
            "tags": list(self.tags),
            "score": self.score,
            "score_breakdown": dict(self.score_breakdown),
        }
