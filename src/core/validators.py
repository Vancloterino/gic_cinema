"""Input validators and parsers for the booking CLI."""

from __future__ import annotations

import re
from typing import Tuple

from src.models.entities import Seat, Theater
from src.utils.seat_utils import seat_in_bounds, seat_is_free

def parse_init_line(line: str) -> Tuple[str, int, int]:
    """Parse the initialization line ``[Title] [Rows] [SeatsPerRow]``.

    The last two whitespace-separated tokens must be integers; everything
    before them is treated as the title (can contain spaces).

    :param line: Raw input line.
    :type line: str
    :return: Tuple of (title, rows, cols).
    :rtype: Tuple[str, int, int]
    :raises ValueError: If parsing fails or values are out of bounds.
    """
    if not line or not line.strip():
        raise ValueError("Initialization input cannot be empty.")

    parts = line.strip().split()
    if len(parts) < 3:
        raise ValueError("Provide: [Title] [Rows] [SeatsPerRow].")

    try:
        rows = int(parts[-2])
        cols = int(parts[-1])
    except ValueError as exc:
        raise ValueError("Rows and SeatsPerRow must be integers.") from exc

    title = " ".join(parts[:-2]).strip()
    if not title:
        raise ValueError("Title cannot be empty.")

    if not (1 <= rows <= 26):
        raise ValueError("Rows must be between 1 and 26 (A–Z).")
    if not (1 <= cols <= 50):
        raise ValueError("SeatsPerRow must be between 1 and 50.")

    return title, rows, cols


def parse_menu_choice(text: str) -> int:
    """Parse the main menu choice (1, 2, or 3).

    :param text: Textual input from the user.
    :type text: str
    :return: Integer menu choice.
    :rtype: int
    :raises ValueError: If choice is invalid.
    """
    choice = text.strip()
    if choice not in {"1", "2", "3"}:
        raise ValueError("Please enter 1, 2, or 3.")
    return int(choice)


def parse_ticket_count(text: str) -> int:
    """Parse a positive integer ticket count.

    :param text: Textual input from the user (e.g., ``"4"``).
    :type text: str
    :return: Positive integer ticket count.
    :rtype: int
    :raises ValueError: If not a positive integer.
    """
    value = text.strip()
    if not value.isdigit():
        raise ValueError("Please enter a positive integer.")
    count = int(value)
    if count <= 0:
        raise ValueError("Ticket count must be greater than zero.")
    return count


_BOOKING_ID_RE = re.compile(r"^GIC\d{4}$")


def parse_booking_id(text: str) -> str:
    """Validate and normalize a booking ID of the form ``GIC0001``.

    :param text: Raw booking ID string.
    :type text: str
    :return: Normalized booking ID (uppercased).
    :rtype: str
    :raises ValueError: If format is invalid.
    """
    bid = text.strip().upper()
    if not _BOOKING_ID_RE.match(bid):
        raise ValueError("Booking ID must match pattern GIC#### (e.g., GIC0001).")
    return bid

def validate_start_seat(theater: Theater, seat: Seat) -> None:
    """Validate a user-specified starting seat for manual allocation.

    Ensures the seat is within bounds and currently unoccupied.

    :param theater: Theater configuration and grid.
    :type theater: Theater
    :param seat: Starting seat provided by the user.
    :type seat: Seat
    :raises ValueError: If the seat is out of bounds or already taken.
    """
    if not seat_in_bounds(theater, seat):
        raise ValueError("Seat is out of bounds for this theater.")
    if not seat_is_free(theater, seat):
        raise ValueError("Selected seat is already taken. Choose another seat.")
