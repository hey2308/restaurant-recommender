"""Phase 1: Data Foundation Layer — loader, preprocessor, feature extraction, store."""

from typing import Any

__all__ = ["run_pipeline"]


def __getattr__(name: str) -> Any:
    if name == "run_pipeline":
        from .pipeline import run_pipeline as fn

        return fn
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
