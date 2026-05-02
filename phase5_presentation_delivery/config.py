"""Configuration for Phase 5 presentation and delivery."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_INPUT_JSON = ROOT / "phase4_llm_recommendation" / "data" / "recommendations.json"
DEFAULT_OUTPUT_JSON = ROOT / "phase5_presentation_delivery" / "data" / "presentation.json"
DEFAULT_OUTPUT_HTML = ROOT / "phase5_presentation_delivery" / "data" / "recommendations.html"
DEFAULT_OUTPUT_TEXT = ROOT / "phase5_presentation_delivery" / "data" / "recommendations.txt"

