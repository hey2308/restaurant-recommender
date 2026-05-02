"""Groq client wrapper for Phase 4."""

from __future__ import annotations

import os
from pathlib import Path

# Try to load .env file if it exists
try:
    from dotenv import load_dotenv
    # Look for .env in current directory, phase4 folder, or project root
    possible_paths = [
        Path(".env"),
        Path(__file__).parent / ".env",
        Path(__file__).parent.parent / ".env",
    ]
    for env_path in possible_paths:
        if env_path.exists():
            load_dotenv(env_path)
            break
except ImportError:
    pass  # dotenv not installed, rely on system env vars


def generate_with_groq(
    *,
    system_prompt: str,
    user_prompt: str,
    model: str,
    temperature: float = 0.2,
) -> str:
    """Send chat completion request to Groq and return text content."""
    try:
        from groq import Groq
    except Exception as exc:
        raise RuntimeError(
            "Groq SDK is not installed. Install dependencies from "
            "phase4_llm_recommendation/requirements.txt."
        ) from exc

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GROQ_API_KEY environment variable.")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Groq returned an empty response.")
    return content

