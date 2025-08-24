"""Seat allocation algorithms for bookings."""

from __future__ import annotations

from typing import Optional

from src.models.entities import Theater, Seat
from src.utils.seat_utils import row_index_to_letter


def center_col_order(cols: int) -> list[int]:
    """Return seat column indices in center-outward order.

    For example, with 10 seats: [5, 6, 4, 7, 3, 8, 2, 9, 1, 10].

    :param cols: Number of seats in the row.
    :type cols: int
    :return: List of column numbers in allocation order.
    :rtype: list[int]
    """
    mid_left = (cols // 2)
    mid_right = mid_left + 1 if cols % 2 == 0 else mid_left + 1

    order: list[int] = []
    left, right = mid_left, mid_right

    if cols % 2 == 1:
        order.append(mid_left + 1)
        left, right = mid_left, mid_left + 2
    else:
        order.extend([mid_left, mid_right])
        left, right = mid_left - 1, mid_right + 1

    while left >= 1 or right <= cols:
        if left >= 1:
            order.append(left)
            left -= 1
        if right <= cols:
            order.append(right)
            right += 1

    return order


def auto_allocate(theater: Theater, k: int) -> Optional[list[Seat]]:
    """Allocate seats automatically using default rules.

    Rules
    -----
    1. Start from the furthest row from the screen (row A).
    2. Within a row, pick seats in center-outward order.
    3. If row cannot fit all, overflow to next row.

    :param theater: Theater object.
    :type theater: Theater
    :param k: Number of seats requested.
    :type k: int
    :return: List of allocated seats, or ``None`` if insufficient capacity.
    :rtype: Optional[list[Seat]]
    """
    if k > theater.available():
        return None

    seats: list[Seat] = []
    for row_idx in range(theater.rows):
        cols_order = center_col_order(theater.cols)
        for col in cols_order:
            if theater.grid[row_idx][col - 1] is None:
                seats.append(Seat(row=chr(ord("A") + row_idx), col=col))
                if len(seats) == k:
                    return seats
    return None


def manual_allocate(theater: Theater, k: int, start: Seat) -> Optional[list[Seat]]:
    """Allocate seats starting from a user-specified seat.

    Rules
    -----
    - Fill to the right within the same row.
    - If insufficient seats, overflow to the next row closer to the screen,
      using default center-outward order.

    :param theater: Theater object.
    :type theater: Theater
    :param k: Number of seats requested.
    :type k: int
    :param start: Starting seat provided by user.
    :type start: Seat
    :return: List of allocated seats, or ``None`` if not possible.
    :rtype: Optional[list[Seat]]
    """
    if k > theater.available():
        return None

    seats: list[Seat] = []
    row_idx = ord(start.row.upper()) - ord("A")

    # Phase 1: same row to the right
    for col in range(start.col, theater.cols + 1):
        if theater.grid[row_idx][col - 1] is None:
            seats.append(Seat(row=start.row.upper(), col=col))
            if len(seats) == k:
                return seats

    # Phase 2: overflow to next rows
    for next_row in range(row_idx + 1, theater.rows):
        cols_order = center_col_order(theater.cols)
        for col in cols_order:
            if theater.grid[next_row][col - 1] is None:
                seats.append(Seat(row=chr(ord("A") + next_row), col=col))
                if len(seats) == k:
                    return seats

    return None
