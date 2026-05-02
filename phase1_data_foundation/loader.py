"""Hugging Face dataset loader with optional schema introspection."""

from __future__ import annotations

from typing import Any, Iterator

from datasets import Dataset, IterableDataset, load_dataset

from . import config


def load_zomato(
    *,
    split: str | None = None,
    streaming: bool = False,
) -> Dataset | IterableDataset:
    """
    Load the Zomato restaurant recommendation dataset.

    ``streaming=True`` is recommended for large downloads to avoid loading
    the full split into memory.
    """
    split = split or config.DEFAULT_SPLIT
    return load_dataset(config.DATASET_ID, split=split, streaming=streaming)


def peek_first_row(dataset: Dataset | IterableDataset) -> dict[str, Any]:
    """Return the first row as a dict (materializes one sample)."""
    if hasattr(dataset, "__iter__"):
        return dict(next(iter(dataset)))
    # Non-streaming Dataset
    return dict(dataset[0])


def iter_rows(
    dataset: Dataset | IterableDataset,
) -> Iterator[dict[str, Any]]:
    """Yield rows as plain dicts."""
    for row in dataset:
        yield dict(row)
