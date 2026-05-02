"""Phase 3: Candidate retrieval and filtering."""

from typing import Any

__all__ = ["run_phase3"]


def __getattr__(name: str) -> Any:
    if name == "run_phase3":
        from .pipeline import run_phase3 as fn

        return fn
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
