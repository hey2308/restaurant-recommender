"""Phase 5 pipeline: format parsed recommendations and render final views."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from . import config
from .explanation_view import build_explanation_lines
from .response_formatter import build_presentation_payload
from .ui_renderer import render_cli_text, render_html, write_output


def run_phase5(phase4_payload: dict[str, Any]) -> dict[str, Any]:
    presentation = build_presentation_payload(phase4_payload)
    profile = presentation["profile"]
    recommendations = presentation["raw_recommendations"]
    explanation_lines = build_explanation_lines(profile, recommendations)
    presentation["explanation_lines"] = explanation_lines
    return presentation


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 5 presentation and delivery.")
    parser.add_argument(
        "--in",
        dest="input_json",
        type=Path,
        default=config.DEFAULT_INPUT_JSON,
        help="Path to Phase 4 recommendations JSON.",
    )
    parser.add_argument(
        "--out-json",
        type=Path,
        default=config.DEFAULT_OUTPUT_JSON,
        help="Path to presentation payload JSON.",
    )
    parser.add_argument(
        "--out-html",
        type=Path,
        default=config.DEFAULT_OUTPUT_HTML,
        help="Path to rendered HTML view.",
    )
    parser.add_argument(
        "--out-text",
        type=Path,
        default=config.DEFAULT_OUTPUT_TEXT,
        help="Path to CLI-style text output.",
    )
    args = parser.parse_args()

    phase4_payload = _load_json(args.input_json)
    result = run_phase5(phase4_payload)

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(result, indent=2), encoding="utf-8")

    html = render_html(
        profile=result["profile"],
        summary=result["summary"],
        cards=result["cards"],
        explanation_lines=result["explanation_lines"],
    )
    text = render_cli_text(
        summary=result["summary"],
        table_rows=result["table_rows"],
        explanation_lines=result["explanation_lines"],
    )
    write_output(args.out_html, html)
    write_output(args.out_text, text)

    print("Phase 5 pipeline complete.")
    print(f"  input_json: {args.input_json.resolve()}")
    print(f"  output_json: {args.out_json.resolve()}")
    print(f"  output_html: {args.out_html.resolve()}")
    print(f"  output_text: {args.out_text.resolve()}")


if __name__ == "__main__":
    main()

