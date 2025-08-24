"""Global pytest fixtures for the GIC Cinemas project."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import pytest

from src.models.entities import Theater, Seat  # noqa: E402
from src.state.context import AppContext  # noqa: E402


@pytest.fixture()
def theater_4x6() -> Theater:
    """A small theater with 4 rows and 6 columns."""
    return Theater(title="Inception", rows=4, cols=6)


@pytest.fixture()
def app_context_empty(theater_4x6: Theater) -> AppContext:
    """Empty application context with a fresh theater."""
    return AppContext(theater=theater_4x6)


@pytest.fixture()
def occupy() -> Callable[[Theater, list[Seat], str], None]:
    """Utility to mark seats as booked in the grid.

    :return: Function that takes (theater, seats, booking_id) and mutates grid.
    :rtype: Callable
    """

    def _occupy(theater: Theater, seats: list[Seat], booking_id: str) -> None:
        for s in seats:
            row_idx = ord(s.row.upper()) - ord("A")
            theater.grid[row_idx][s.col - 1] = booking_id

    return _occupy
