"""Seat utility functions for conversions and validation."""

from __future__ import annotations

import string
from typing import Optional

from src.models.entities import Seat, Theater


def row_index_to_letter(index: int) -> str:
    """Convert a zero-based row index to a row letter.

    :param index: Row index (0-based, where 0 == A).
    :type index: int
    :return: Row letter.
    :rtype: str
    :raises ValueError: If index is not in the range 0..25.
    """
    if not (0 <= index < 26):
        raise ValueError("Row index must be between 0 and 25.")
    return string.ascii_uppercase[index]


def row_letter_to_index(letter: str) -> int:
    """Convert a row letter to a zero-based row index.

    :param letter: Row letter (A–Z).
    :type letter: str
    :return: Zero-based index.
    :rtype: int
    :raises ValueError: If *letter* is not a single character in A–Z.
    """
    if letter is None:
        raise ValueError("Row letter must be a single character A–Z.")
    letter = letter.strip().upper()
    if len(letter) != 1 or not ("A" <= letter <= "Z"):
        raise ValueError("Row letter must be a single character A–Z.")
    return ord(letter) - ord("A")


def parse_seat_code(code: str) -> Seat:
    """Parse a seat code like ``B03`` into a :class:`Seat`.

    :param code: Seat code string.
    :type code: str
    :return: Seat object.
    :rtype: Seat
    :raises ValueError: If format is invalid.
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
    """Format a seat code from row index and col.

    :param row: Row index (0-based).
    :type row: int
    :param col: Column index (1-based).
    :type col: int
    :return: Seat code string.
    :rtype: str
    """
    return f"{row_index_to_letter(row)}{col:02d}"


def seat_in_bounds(theater: Theater, seat: Seat) -> bool:
    """Return whether *seat* lies within the dimensions of *theater*.

    :param theater: Theater to check against.
    :type theater: Theater
    :param seat: Seat coordinate.
    :type seat: Seat
    :return: ``True`` if in bounds, else ``False``.
    :rtype: bool
    """
    row_idx = row_letter_to_index(seat.row)
    return 0 <= row_idx < theater.rows and 1 <= seat.col <= theater.cols


def seat_is_free(theater: Theater, seat: Seat) -> bool:
    """Return whether *seat* is currently unoccupied.

    :param theater: Theater to check against.
    :type theater: Theater
    :param seat: Seat coordinate.
    :type seat: Seat
    :return: ``True`` if empty, else ``False``.
    :rtype: bool
    """
    row_idx = row_letter_to_index(seat.row)
    if not (0 <= row_idx < theater.rows) or not (1 <= seat.col <= theater.cols):
        return False
    return theater.grid[row_idx][seat.col - 1] is None
