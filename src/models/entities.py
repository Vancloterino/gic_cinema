"""Domain entities (dataclasses)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class Seat:
    """A seat coordinate.

    :param row: Row letter (``A``–``Z``).
    :type row: str
    :param col: One-based column index.
    :type col: int
    """

    row: str
    col: int

    def code(self) -> str:
        """Return the seat code as ``<Row><2-digit Col>`` (e.g., ``A03``).

        :return: Formatted seat code.
        :rtype: str
        """
        return f"{self.row.upper()}{self.col:02d}"


@dataclass(slots=True)
class Booking:
    """A confirmed booking.

    :param booking_id: Unique booking identifier (e.g., ``GIC0001``).
    :type booking_id: str
    :param seats: Seats reserved by this booking.
    :type seats: list[Seat]
    """

    booking_id: str
    seats: List[Seat] = field(default_factory=list)


@dataclass(slots=True)
class Theater:
    """A single-screen theater layout and occupancy grid.

    :param title: Film title for the current screening.
    :type title: str
    :param rows: Number of seating rows.
    :type rows: int
    :param cols: Number of seats per row.
    :type cols: int
    """

    title: str
    rows: int
    cols: int
    grid: List[List[Optional[str]]] = field(init=False)

    def __post_init__(self) -> None:
        """Initialize the occupancy grid as an ``rows × cols`` matrix of ``None``."""
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def capacity(self) -> int:
        """Return the total number of seats.

        :return: ``rows * cols``.
        :rtype: int
        """
        return self.rows * self.cols

    def available(self) -> int:
        """Return the number of currently unoccupied seats.

        :return: Count of seats with ``None`` in the grid.
        :rtype: int
        """
        return sum(1 for r in self.grid for c in r if c is None)
