"""Unit tests for services.feedback.domain (no database)."""

from datetime import UTC, datetime, timedelta

import pytest
from services.feedback.domain import (
    compute_distribution,
    is_duplicate,
    weighted_average,
)


def test_compute_distribution_all_zero_for_empty() -> None:
    d = compute_distribution([])
    assert d == {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}


def test_compute_distribution_counts_by_rating() -> None:
    d = compute_distribution([5, 5, 4, 1])
    assert d[5] == 2
    assert d[4] == 1
    assert d[1] == 1
    assert d[2] == 0


def test_compute_distribution_invalid_rating_raises() -> None:
    with pytest.raises(ValueError, match="rating must be between"):
        compute_distribution([6])


def test_weighted_average_empty_returns_zero() -> None:
    assert weighted_average({1: 0, 2: 0, 3: 0, 4: 0, 5: 0}) == 0.0


def test_weighted_average_known_distribution_value() -> None:
    d = compute_distribution([3, 5, 5])
    assert weighted_average(d) == 4.33


def test_is_duplicate_within_window_same_source() -> None:
    now = datetime.now(UTC)
    prev = now - timedelta(seconds=60)
    assert is_duplicate(now, prev, "web", "web", window_seconds=300) is True


def test_is_duplicate_outside_window() -> None:
    now = datetime.now(UTC)
    prev = now - timedelta(seconds=400)
    assert is_duplicate(now, prev, "web", "web", window_seconds=300) is False


def test_is_duplicate_different_source() -> None:
    now = datetime.now(UTC)
    prev = now - timedelta(seconds=10)
    assert is_duplicate(now, prev, "web", "mobile", window_seconds=300) is False


def test_is_duplicate_no_previous() -> None:
    now = datetime.now(UTC)
    assert is_duplicate(now, None, "web", "web", window_seconds=300) is False
