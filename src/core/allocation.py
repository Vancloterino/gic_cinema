"""Seat allocation algorithms (auto and manual)."""

from typing import List, Optional

from src.models.entities import Theater, Seat
from src.core.seat_utils import row_letter_to_index


def center_col_order(cols: int) -> List[int]:
    """Return the preferred column order from center outwards.

    Examples
    --------
    - ``cols = 6`` → ``[3, 4, 2, 5, 1, 6]``
    - ``cols = 5`` → ``[3, 2, 4, 1, 5]``

    :param cols: Number of seats per row.
    :type cols: int
    :return: Column indices in preferred order (1-based).
    :rtype: list[int]
    """
    if cols <= 0:
        return []

    order: List[int] = []
    if cols % 2 == 0:
        left = cols // 2
        right = left + 1
        order.extend([left, right])
        left -= 1
        right += 1
        while left >= 1 or right <= cols:
            if left >= 1:
                order.append(left)
                left -= 1
            if right <= cols:
                order.append(right)
                right += 1
    else:
        center = (cols + 1) // 2
        order.append(center)
        offset = 1
        while len(order) < cols:
            if center - offset >= 1:
                order.append(center - offset)
            if center + offset <= cols:
                order.append(center + offset)
            offset += 1
    return order


def auto_allocate(theater: Theater, k: int) -> Optional[List[Seat]]:
    """Allocate ``k`` seats using center-outwards preference per row.

    :param theater: Theater context (grid is inspected, not mutated).
    :type theater: Theater
    :param k: Number of seats requested.
    :type k: int
    :return: Proposed seats or ``None`` if insufficient capacity.
    :rtype: Optional[list[Seat]]
    """
    if k <= 0:
        return []
    if k > theater.available():
        return None

    proposed: List[Seat] = []
    needed = k

    for row_idx in range(theater.rows):
        if needed == 0:
            break
        row_letter = chr(ord("A") + row_idx)
        order = center_col_order(theater.cols)
        for col in order:
            if theater.grid[row_idx][col - 1] is None:
                proposed.append(Seat(row=row_letter, col=col))
                needed -= 1
                if needed == 0:
                    break

    return proposed if needed == 0 else None


def manual_allocate(theater: Theater, k: int, start: Seat) -> Optional[List[Seat]]:
    """Allocate seats starting from *start* seat, then overflow to next rows.

    Strategy
    --------
    1. In the start row, take a contiguous **rightward** block beginning at
       ``start.col`` until either the row ends, a seat is occupied, or ``k``
       seats are gathered.
    2. If seats remain, overflow to subsequent rows using
       :func:`center_col_order`.

    :param theater: Theater context (grid is inspected, not mutated).
    :type theater: Theater
    :param k: Number of seats requested.
    :type k: int
    :param start: Starting seat (assumed valid and free by caller).
    :type start: Seat
    :return: Proposed seats or ``None`` if insufficient capacity.
    :rtype: Optional[list[Seat]]
    """
    if k <= 0:
        return []
    if k > theater.available():
        return None

    proposed: List[Seat] = []
    needed = k
    start_row = row_letter_to_index(start.row)

    # Phase 1: same row, rightward contiguous seats
    col = start.col
    while col <= theater.cols and needed > 0:
        if theater.grid[start_row][col - 1] is None:
            proposed.append(Seat(row=start.row.upper(), col=col))
            needed -= 1
        else:
            break
        col += 1

    if needed == 0:
        return proposed

    # Phase 2: overflow rows with center-outwards preference
    for row_idx in range(start_row + 1, theater.rows):
        if needed == 0:
            break
        row_letter = chr(ord("A") + row_idx)
        order = center_col_order(theater.cols)
        for c in order:
            if theater.grid[row_idx][c - 1] is None:
                proposed.append(Seat(row=row_letter, col=c))
                needed -= 1
                if needed == 0:
                    break

    return proposed if needed == 0 else None
