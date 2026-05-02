"""Cleaning, null handling, and numeric normalization for raw field values."""

from __future__ import annotations

import re
from typing import Any


def clean_str(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, float) and value != value:  # NaN
        return None
    s = str(value).strip()
    return s if s else None


def parse_rating(value: Any) -> float | None:
    """
    Parse rating from number or strings like '4.2', '4.2/5', '4.2 out of 5'.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        if isinstance(value, float) and value != value:
            return None
        return float(value)
    s = clean_str(value)
    if not s:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)", s)
    if not m:
        return None
    return float(m.group(1))


def parse_cost(value: Any) -> float | None:
    """
    Parse estimated cost from number or messy strings (currency symbols, ranges).
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        if isinstance(value, float) and value != value:
            return None
        return float(value)
    s = clean_str(value)
    if not s:
        return None
    digits = re.findall(r"\d+(?:\.\d+)?", s.replace(",", ""))
    if not digits:
        return None
    nums = [float(x) for x in digits]
    return sum(nums) / len(nums)


def normalize_cuisine(value: Any) -> str | None:
    """Single string of cuisines; comma-separated in output."""
    if value is None:
        return None
    if isinstance(value, list):
        parts = [clean_str(x) for x in value]
        parts = [p for p in parts if p]
        return ", ".join(parts) if parts else None
    s = clean_str(value)
    return s
