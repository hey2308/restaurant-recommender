"""Phase 4 pipeline: prompt build, Groq call, parse, and guarded fallback."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from . import config
from .guardrails import (
    build_fallback_recommendations,
    clamp_candidates,
    enforce_prompt_size,
)
from .llm_client import generate_with_groq
from .prompt_builder import build_system_prompt, build_user_prompt
from .response_parser import parse_llm_response


def run_phase4(
    *,
    phase3_payload: dict[str, Any],
    model: str = config.DEFAULT_GROQ_MODEL,
    top_n: int = config.DEFAULT_OUTPUT_TOP_N,
) -> dict[str, Any]:
    profile = phase3_payload.get("profile", {})
    raw_candidates = phase3_payload.get("candidates", [])
    if not isinstance(raw_candidates, list):
        raise ValueError("Phase 3 payload is invalid: 'candidates' must be a list.")
    if not raw_candidates:
        raise ValueError("Phase 3 payload has no candidates to rank.")

    candidates = clamp_candidates(raw_candidates)
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(profile, candidates, top_n=top_n)
    user_prompt = enforce_prompt_size(user_prompt)

    try:
        raw = generate_with_groq(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model,
        )
        parsed = parse_llm_response(raw, profile=profile, top_n=top_n)
        parsed["meta"]["model"] = model
        parsed["meta"]["input_candidates"] = len(raw_candidates)
        parsed["meta"]["prompt_candidates"] = len(candidates)
        return parsed
    except Exception as exc:
        fallback = build_fallback_recommendations(
            profile,
            candidates,
            top_n=top_n,
            reason=str(exc),
        )
        fallback["meta"]["model"] = model
        fallback["meta"]["input_candidates"] = len(raw_candidates)
        fallback["meta"]["prompt_candidates"] = len(candidates)
        return fallback


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 4 LLM recommendation intelligence.")
    parser.add_argument(
        "--in",
        dest="input_json",
        type=Path,
        default=config.DEFAULT_INPUT_JSON,
        help="Path to Phase 3 candidates JSON.",
    )
    parser.add_argument(
        "--out",
        dest="output_json",
        type=Path,
        default=config.DEFAULT_OUTPUT_JSON,
        help="Path to write Phase 4 recommendations JSON.",
    )
    parser.add_argument("--model", default=config.DEFAULT_GROQ_MODEL, help="Groq model name.")
    parser.add_argument(
        "--top-n",
        type=int,
        default=config.DEFAULT_OUTPUT_TOP_N,
        help="Number of recommendations to return.",
    )
    args = parser.parse_args()

    payload = _load_json(args.input_json)
    result = run_phase4(phase3_payload=payload, model=args.model, top_n=args.top_n)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("Phase 4 pipeline complete.")
    print(f"  mode: {result.get('meta', {}).get('mode')}")
    print(f"  model: {result.get('meta', {}).get('model')}")
    print(f"  recommendations: {len(result.get('recommendations', []))}")
    print(f"  output_json: {args.output_json.resolve()}")


if __name__ == "__main__":
    main()

