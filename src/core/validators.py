"""Input validators and parsers for the CLI."""

import re
from typing import Tuple

from src.models.entities import Seat, Theater
from src.core.seat_utils import seat_in_bounds, seat_is_free


def parse_init_line(line: str) -> Tuple[str, int, int]:
    """Parse the initialization line ``[Title] [Rows] [SeatsPerRow]``.

    The final two whitespace-delimited tokens must be integers. All preceding
    tokens compose the title (which may contain spaces).

    :param line: Raw input line.
    :type line: str
    :return: Tuple ``(title, rows, cols)``.
    :rtype: Tuple[str, int, int]
    :raises ValueError: On malformed input or out-of-bounds values.
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


def parse_ticket_count(text: str) -> int:
    """Parse a positive integer ticket count.

    :param text: Input string for ticket count.
    :type text: str
    :return: Positive integer count.
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

    :param text: Raw booking ID.
    :type text: str
    :return: Normalized booking ID (uppercased).
    :rtype: str
    :raises ValueError: If the pattern does not match ``GIC####``.
    """
    bid = text.strip().upper()
    if not _BOOKING_ID_RE.match(bid):
        raise ValueError("Booking ID must match pattern GIC#### (e.g., GIC0001).")
    return bid


def validate_start_seat(theater: Theater, seat: Seat) -> None:
    """Validate a proposed starting seat for manual allocation.

    The seat must be in bounds and currently free.

    :param theater: Theater descriptor.
    :type theater: Theater
    :param seat: Proposed starting seat.
    :type seat: Seat
    :raises ValueError: If the seat is out of bounds or already taken.
    """
    if not seat_in_bounds(theater, seat):
        raise ValueError("Seat is out of bounds for this theater.")
    if not seat_is_free(theater, seat):
        raise ValueError("Selected seat is already taken. Choose another seat.")
