"""Configuration for Phase 4 LLM recommendation intelligence."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_INPUT_JSON = ROOT / "phase3_candidate_retrieval" / "data" / "candidates.json"
DEFAULT_OUTPUT_JSON = ROOT / "phase4_llm_recommendation" / "data" / "recommendations.json"

# Groq model can be overridden with --model
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"

# Guardrails
MAX_CANDIDATES_IN_PROMPT = 12
MAX_PROMPT_CHARS = 12000
DEFAULT_OUTPUT_TOP_N = 5

