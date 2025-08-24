"""Domain entities for the GIC Cinemas booking system."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True, slots=True)
class Seat:
    """Represents a single seat coordinate in the theater.

    :param row: Row letter (``A``..``Z``).
    :type row: str
    :param col: Seat number within the row (1-based).
    :type col: int
    """

    row: str
    col: int

    def code(self) -> str:
        """Return the seat code in standard form (e.g., ``B03``).

        :return: Seat code with zero-padded column.
        :rtype: str
        """
        return f"{self.row}{self.col:02d}"


@dataclass(slots=True)
class Booking:
    """Represents a booking record.

    :param booking_id: Unique booking identifier (e.g., ``GIC0001``).
    :type booking_id: str
    :param seats: List of seats reserved in this booking.
    :type seats: list[Seat]
    """

    booking_id: str
    seats: list[Seat] = field(default_factory=list)


@dataclass(slots=True)
class Theater:
    """Represents the theater configuration and current occupancy.

    :param title: Movie title for the current show.
    :type title: str
    :param rows: Number of seating rows.
    :type rows: int
    :param cols: Number of seats per row.
    :type cols: int
    :param grid: 2D structure where ``None`` means empty, otherwise stores the
                 booking ID of the occupant.
    :type grid: list[list[Optional[str]]]
    """

    title: str
    rows: int
    cols: int
    grid: list[list[Optional[str]]] = field(init=False)

    def __post_init__(self) -> None:
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    @property
    def capacity(self) -> int:
        """Return the total number of seats in the theater.

        :return: Theater capacity.
        :rtype: int
        """
        return self.rows * self.cols

    def available(self) -> int:
        """Return the number of currently available (empty) seats.

        :return: Number of available seats.
        :rtype: int
        """
        return sum(cell is None for row in self.grid for cell in row)
