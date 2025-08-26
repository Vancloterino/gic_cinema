"""ASCII renderer for seat maps."""

from typing import Iterable, Optional

from src.core.renderers.base import Renderer
from src.models.entities import Seat, Theater


class AsciiRenderer(Renderer):
    """Render the theater seat map as monospaced ASCII."""

    def seat_map(
        self,
        theater: Theater,
        current_booking_id: Optional[str] = None,
        preview_seats: Optional[Iterable[Seat]] = None,
    ) -> str:
        """Render the seat map using ASCII symbols.

        Legend
        ------
        ``.`` :
            Empty seat.
        ``o`` :
            Highlight (seats for *current_booking_id* or *preview_seats*).
        ``#`` :
            Booked seat belonging to another booking.

        :param theater: Theater descriptor.
        :type theater: Theater
        :param current_booking_id: Booking ID whose seats should be highlighted.
        :type current_booking_id: Optional[str]
        :param preview_seats: Seats to highlight as a draft selection.
        :type preview_seats: Optional[Iterable[Seat]]
        :return: Multi-line string suitable for console output.
        :rtype: str
        """
        preview_codes = {s.row.upper() + f"{s.col:02d}" for s in (preview_seats or [])}

        lines: list[str] = []
        lines.append("    S C R E E N")

        # Divider width matches row width; keep at least 18 chars for aesthetics.
        divider_len = 2 * theater.cols + 2
        lines.append("-" * max(divider_len, 18))

        # Render rows from back to front (e.g., B then A for 2 rows).
        for row_idx in range(theater.rows - 1, -1, -1):
            row_letter = chr(ord("A") + row_idx)
            cells: list[str] = []
            for col in range(1, theater.cols + 1):
                seat_code = f"{row_letter}{col:02d}"
                occupant = theater.grid[row_idx][col - 1]
                if seat_code in preview_codes:
                    char = "o"
                elif occupant is None:
                    char = "."
                else:
                    char = (
                        "o"
                        if (current_booking_id and occupant == current_booking_id)
                        else "#"
                    )
                cells.append(char)
            lines.append(f"{row_letter}  " + " ".join(cells))

        # Footer numbers aligned under seats.
        footer_nums = " ".join(str(i) for i in range(1, theater.cols + 1))
        lines.append(f"   {footer_nums}")
        return "\n".join(lines)
