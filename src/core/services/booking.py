"""Booking service: preview and commit operations.

This module centralizes seat allocation previews and grid mutations so
commands remain thin and easy to test.
"""

from __future__ import annotations

from typing import Iterable, Optional

from src.core.allocation import auto_allocate, manual_allocate
from src.core.errors import CapacityExceeded, NotFound
from src.core.seat_utils import row_letter_to_index
from src.models.context import AppContext
from src.models.entities import Booking, Seat


class BookingService:
    """High-level booking operations."""

    def preview_auto(self, ctx: AppContext, k: int) -> Optional[list[Seat]]:
        """Return an auto-allocation preview for ``k`` seats.

        :param ctx: Application context.
        :type ctx: AppContext
        :param k: Number of seats requested.
        :type k: int
        :return: Proposed seats or ``None`` if not possible.
        :rtype: Optional[list[Seat]]
        :raises CapacityExceeded: If requested seats exceed availability.
        """
        if k > ctx.theater.available():
            raise CapacityExceeded(
                f"Sorry, there are only {ctx.theater.available()} seats available.\n"
            )
        return auto_allocate(ctx.theater, k)

    def preview_manual(
        self, ctx: AppContext, k: int, start: Seat
    ) -> Optional[list[Seat]]:
        """Return a manual allocation preview from *start*.

        :param ctx: Application context.
        :type ctx: AppContext
        :param k: Number of seats requested.
        :type k: int
        :param start: Starting seat.
        :type start: Seat
        :return: Proposed seats or ``None`` if not possible.
        :rtype: Optional[list[Seat]]
        :raises CapacityExceeded: If requested seats exceed availability.
        """
        if k > ctx.theater.available():
            raise CapacityExceeded(
                f"Sorry, there are only {ctx.theater.available()} seats available./n"
            )
        return manual_allocate(ctx.theater, k, start)

    # ----- commit & ids -----

    def new_provisional_id(self, ctx: AppContext) -> str:
        """Generate a new booking identifier without committing.

        :param ctx: Application context.
        :type ctx: AppContext
        :return: New booking ID like ``GIC0001``.
        :rtype: str
        """
        return ctx.generate_booking_id()

    def commit_booking(
        self, ctx: AppContext, booking_id: str, seats: Iterable[Seat]
    ) -> None:
        """Commit seats under *booking_id* and register the booking.

        :param ctx: Application context.
        :type ctx: AppContext
        :param booking_id: Booking identifier to use for ownership.
        :type booking_id: str
        :param seats: Seats to assign.
        :type seats: Iterable[Seat]
        """
        for s in seats:
            row_idx = row_letter_to_index(s.row)
            ctx.theater.grid[row_idx][s.col - 1] = booking_id
        ctx.bookings[booking_id] = Booking(booking_id=booking_id, seats=list(seats))

    # ----- queries -----

    def get_booking(self, ctx: AppContext, booking_id: str) -> Booking:
        """Return a booking by ID or raise :class:`NotFound`.

        :param ctx: Application context.
        :type ctx: AppContext
        :param booking_id: Booking identifier.
        :type booking_id: str
        :return: Booking object.
        :rtype: Booking
        :raises NotFound: If booking does not exist.
        """
        b = ctx.bookings.get(booking_id)
        if not b:
            raise NotFound(f"Booking '{booking_id}' not found.")
        return b
