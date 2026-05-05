"""Pure business rules for feedback (no I/O)."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime

type Distribution = dict[int, int]


def compute_distribution(ratings: Iterable[int]) -> Distribution:
    dist: Distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in ratings:
        if r < 1 or r > 5:
            msg = f"rating must be between 1 and 5, got {r}"
            raise ValueError(msg)
        dist[r] += 1
    return dist


def weighted_average(dist: Distribution) -> float:
    total_n = sum(dist.values())
    if total_n == 0:
        return 0.0
    weighted = sum(k * v for k, v in dist.items())
    return round(weighted / total_n, 2)


def is_duplicate(
    now: datetime,
    prev: datetime | None,
    source: str,
    prev_source: str | None,
    window_seconds: int = 300,
) -> bool:
    if prev is None:
        return False
    if prev_source != source:
        return False
    delta = now - prev
    return delta.total_seconds() <= float(window_seconds)
