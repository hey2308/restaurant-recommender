"""Configuration for Phase 3 retrieval, filtering, and top-N selection."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_PHASE1_DB = ROOT / "phase1_data_foundation" / "data" / "restaurants.db"
DEFAULT_OUTPUT_JSON = ROOT / "phase3_candidate_retrieval" / "data" / "candidates.json"

# Budget bands used by phase 2 and mapped to estimated cost ranges.
# These can be tuned later from analytics/feedback.
BUDGET_RANGES: dict[str, tuple[float, float | None]] = {
    "low": (0.0, 500.0),
    "medium": (500.0, 1500.0),
    "high": (1500.0, None),
}

# Optional weighted score before LLM handoff.
DEFAULT_WEIGHTS = {
    "rating": 0.50,
    "cost_fit": 0.25,
    "tag_match": 0.15,
    "location_bonus": 0.10,
}
