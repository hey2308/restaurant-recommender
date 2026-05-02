"""Basic web UI and JSON API for user preference capture (Phase 2)."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from phase2_user_preferences.validation import validate_preferences

_TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"
app = Flask(__name__, template_folder=str(_TEMPLATE_DIR))
app.config["JSON_SORT_KEYS"] = False


def _form_to_payload() -> dict:
    return {
        "location": request.form.get("location", ""),
        "budget": request.form.get("budget", ""),
        "cuisine": request.form.get("cuisine", ""),
        "min_rating": request.form.get("min_rating") or None,
        "optional_tags": request.form.getlist("optional_tags"),
    }


def _json_to_payload() -> dict:
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return {}
    raw_tags = body.get("optional_tags")
    if raw_tags is None:
        tags: list[str] | str = []
    elif isinstance(raw_tags, list):
        tags = raw_tags
    elif isinstance(raw_tags, str):
        tags = raw_tags
    else:
        tags = [str(raw_tags)]
    return {
        "location": body.get("location", ""),
        "budget": body.get("budget", ""),
        "cuisine": body.get("cuisine", ""),
        "min_rating": body.get("min_rating"),
        "optional_tags": tags,
    }


@app.get("/")
def index():
    return render_template("preferences.html")


@app.post("/submit")
def submit():
    profile, errors = validate_preferences(_form_to_payload())
    if errors:
        return (
            render_template(
                "preferences.html",
                errors=errors,
                form=request.form,
            ),
            400,
        )
    assert profile is not None
    return render_template("result.html", profile=profile)


@app.post("/api/preferences")
def api_preferences():
    profile, errors = validate_preferences(_json_to_payload())
    if errors:
        return jsonify({"ok": False, "errors": errors}), 400
    assert profile is not None
    return jsonify({"ok": True, "profile": profile.to_dict()}), 200


@app.get("/health")
def health():
    return jsonify({"status": "ok", "phase": 2}), 200


def create_app() -> Flask:
    """Factory for tests or WSGI servers."""
    return app


def main() -> None:
    host = os.getenv("PHASE2_HOST", "0.0.0.0")
    port = int(os.getenv("PHASE2_PORT", "5000"))
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
