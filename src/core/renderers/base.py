"""Renderer protocol."""

from typing import Iterable, Optional, Protocol

from src.models.entities import Seat, Theater


class Renderer(Protocol):
    """Protocol for seat map renderers."""

    def seat_map(
        self,
        theater: Theater,
        current_booking_id: Optional[str] = None,
        preview_seats: Optional[Iterable[Seat]] = None,
    ) -> str:
        """Return a string representation of the seat map.

        :param theater: Theater descriptor.
        :type theater: Theater
        :param current_booking_id: Booking ID to highlight, if any.
        :type current_booking_id: Optional[str]
        :param preview_seats: Provisional seats to highlight, if any.
        :type preview_seats: Optional[Iterable[Seat]]
        :return: Rendered ASCII seat map (or other format in future renderers).
        :rtype: str
        """
