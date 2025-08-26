"""Seat utilities for conversions, parsing, and validation."""

import string

from src.models.entities import Seat, Theater


def row_index_to_letter(index: int) -> str:
    """Convert a zero-based row index to a row letter.

    :param index: Row index in the range ``0..25`` (where 0 == ``A``).
    :type index: int
    :return: Row letter (``A``–``Z``).
    :rtype: str
    :raises ValueError: If index is outside ``0..25``.
    """
    if not (0 <= index < 26):
        raise ValueError("Row index must be between 0 and 25.")
    return string.ascii_uppercase[index]


def row_letter_to_index(letter: str) -> int:
    """Convert a row letter to a zero-based row index.

    :param letter: Row letter (``A``–``Z``), case-insensitive.
    :type letter: str
    :return: Zero-based row index.
    :rtype: int
    :raises ValueError: If *letter* is not exactly one character in ``A``–``Z``.
    """
    if letter is None:
        raise ValueError("Row letter must be a single character A–Z.")
    letter = letter.strip().upper()
    if len(letter) != 1 or not ("A" <= letter <= "Z"):
        raise ValueError("Row letter must be a single character A–Z.")
    return ord(letter) - ord("A")


def parse_seat_code(code: str) -> Seat:
    """Parse a seat code like ``B03`` into a :class:`Seat`.

    :param code: Seat code string with format ``<RowLetter><2-digit column>``.
    :type code: str
    :return: Parsed seat.
    :rtype: Seat
    :raises ValueError: If the code is empty or malformed.
    """
    if not code:
        raise ValueError("Seat code cannot be empty.")

    letter = code[0].upper()
    if len(letter) != 1 or not ("A" <= letter <= "Z"):
        raise ValueError(f"Invalid seat code row in '{code}'. Row must be A–Z.")

    digits = code[1:]
    if not digits.isdigit():
        raise ValueError(f"Invalid seat code digits in '{code}'.")

    col = int(digits)
    if col < 1:
        raise ValueError("Seat column must be >= 1.")

    return Seat(row=letter, col=col)


def format_seat_code(row: int, col: int) -> str:
    """Format a seat code from zero-based *row* and one-based *col*.

    :param row: Zero-based row index.
    :type row: int
    :param col: One-based column index (``>= 1``).
    :type col: int
    :return: Seat code like ``A01``.
    :rtype: str
    """
    return f"{row_index_to_letter(row)}{col:02d}"


def seat_in_bounds(theater: Theater, seat: Seat) -> bool:
    """Return whether the seat is within the theater dimensions.

    :param theater: Theater descriptor.
    :type theater: Theater
    :param seat: Seat coordinate to check.
    :type seat: Seat
    :return: ``True`` if seat is within bounds.
    :rtype: bool
    """
    row_idx = row_letter_to_index(seat.row)
    return 0 <= row_idx < theater.rows and 1 <= seat.col <= theater.cols


def seat_is_free(theater: Theater, seat: Seat) -> bool:
    """Return whether the seat is currently unoccupied.

    :param theater: Theater descriptor.
    :type theater: Theater
    :param seat: Seat coordinate to check.
    :type seat: Seat
    :return: ``True`` if the seat is empty.
    :rtype: bool
    """
    row_idx = row_letter_to_index(seat.row)
    if not (0 <= row_idx < theater.rows) or not (1 <= seat.col <= theater.cols):
        return False
    return theater.grid[row_idx][seat.col - 1] is None
