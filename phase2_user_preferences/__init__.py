"""Phase 2: User Preference Capture — validation, normalization, web UI entrypoint."""

from .models import PreferenceProfile
from .normalizer import normalize_preferences
from .validation import validate_preferences

__all__ = [
    "PreferenceProfile",
    "normalize_preferences",
    "validate_preferences",
]
