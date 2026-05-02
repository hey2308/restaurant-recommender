"""Render outputs for web (HTML) and CLI text."""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any


def render_html(
    *,
    profile: dict[str, Any],
    summary: str,
    cards: list[dict[str, Any]],
    explanation_lines: list[str],
) -> str:
    cards_html = []
    for c in cards:
        cards_html.append(
            "<div class='card'>"
            f"<h3>{escape(str(c.get('title', 'Unknown')))}</h3>"
            f"<p><strong>{escape(str(c.get('subtitle', '')))}</strong></p>"
            f"<p>Rating: {escape(str(c.get('rating')))}</p>"
            f"<p>Estimated cost: {escape(str(c.get('estimated_cost')))}</p>"
            f"<p>Cuisine: {escape(str(c.get('cuisine')))}</p>"
            f"<p>Location: {escape(str(c.get('location')))}</p>"
            f"<p>{escape(str(c.get('explanation', '')))}</p>"
            "</div>"
        )

    explanation_html = "<br/>".join(escape(line) for line in explanation_lines)
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Restaurant Recommendations</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; background: #f8fafc; }}
    .container {{ max-width: 960px; margin: auto; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }}
    .card {{ background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; }}
    .meta {{ color: #334155; }}
    .explanation {{ margin-top: 18px; padding: 12px; background: #fff; border-radius: 10px; border: 1px solid #e2e8f0; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Top Restaurant Recommendations</h1>
    <p class="meta">
      Profile: location={escape(str(profile.get("location")))} | budget={escape(str(profile.get("budget")))}
      | cuisine={escape(str(profile.get("cuisine")))} | min_rating={escape(str(profile.get("min_rating")))}
    </p>
    <p><strong>Summary:</strong> {escape(summary)}</p>
    <div class="cards">
      {''.join(cards_html)}
    </div>
    <div class="explanation">
      <h2>Explanation View</h2>
      <p>{explanation_html}</p>
    </div>
  </div>
</body>
</html>
"""


def render_cli_text(
    *,
    summary: str,
    table_rows: list[dict[str, Any]],
    explanation_lines: list[str],
) -> str:
    lines = []
    lines.append("Top Restaurant Recommendations")
    lines.append("=" * 30)
    lines.append(f"Summary: {summary}")
    lines.append("")
    lines.append("Table View")
    lines.append("-" * 30)
    for row in table_rows:
        lines.append(
            f"{row.get('rank')}. {row.get('name')} | "
            f"rating={row.get('rating')} | cost={row.get('estimated_cost')} | "
            f"cuisine={row.get('cuisine')} | location={row.get('location')}"
        )
    lines.append("")
    lines.extend(explanation_lines)
    return "\n".join(lines)


def write_output(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

