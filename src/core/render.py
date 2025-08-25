"""ASCII rendering utilities for the seating map."""

from __future__ import annotations

from typing import Iterable, Optional

from src.models.entities import Theater, Seat


def render_seat_map(
    theater: Theater,
    current_booking_id: Optional[str] = None,
    preview_seats: Optional[Iterable[Seat]] = None,
) -> str:
    """Render the theater seat map as a monospaced ASCII string.

    The output shows a header with the word ``SCREEN``, a horizontal divider,
    then rows rendered **from back to front** (e.g., for 8 rows: ``H`` to ``A``).
    A footer lists the seat numbers.

    Symbol legend
    -------------
    ``.`` :
        Empty seat (available).
    ``o`` :
        Seats highlighted for the **current view**. This is either:
        - seats belonging to the ``current_booking_id`` when checking a booking, or
        - seats provided in ``preview_seats`` during an in-progress booking preview.
        If both are provided, ``preview_seats`` take precedence.
    ``#`` :
        Seats booked by **other bookings**.

    :param theater: Theater configuration and current occupancy grid.
    :type theater: Theater
    :param current_booking_id: Booking ID to highlight as the current view, if any.
    :type current_booking_id: Optional[str]
    :param preview_seats: Provisional seats to highlight for a draft booking.
    :type preview_seats: Optional[Iterable[Seat]]
    :return: Multi-line string suitable for printing to console.
    :rtype: str
    """
    # Precompute a set for quick membership when previewing seats. {'A04', 'A06', 'A05', 'A07'}
    preview_codes = {s.row.upper() + f"{s.col:02d}" for s in preview_seats or []}

    lines: list[str] = []
    # Header
    lines.append("    S C R E E N")
    # Divider length: row label (1 char) + 1 space + 2*cols-1 characters for seats + some padding
    divider_len = 2 * theater.cols + 2
    lines.append("-" * max(divider_len, 18))

    # Rows: render from back (last index) to front (index 0).
    for row_idx in range(theater.rows - 1, -1, -1):
        row_letter = chr(ord("A") + row_idx)
        cells: list[str] = []
        for col in range(1, theater.cols + 1):
            seat_code = f"{row_letter}{col:02d}"
            occupant = theater.grid[row_idx][col - 1]
            char: str

            if seat_code in preview_codes:
                char = "o"
            elif occupant is None:
                char = "."
            else:
                # Occupied by some booking
                if current_booking_id is not None and occupant == current_booking_id:
                    char = "o"
                else:
                    char = "#"

            cells.append(char)

        # Example: "A  . . o o . ."
        lines.append(f"{row_letter}  " + " ".join(cells))

    # Footer: seat numbers
    footer_nums = " ".join(str(i) for i in range(1, theater.cols + 1))
    lines.append(f"   {footer_nums}")

    return "\n".join(lines)
