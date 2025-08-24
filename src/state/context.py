"""Application state containers for the GIC Cinemas booking system."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from src.models.entities import Theater, Booking, Seat


@dataclass(slots=True)
class DraftBooking:
    """Ephemeral state for an in-progress booking.

    :param requested_tickets: Number of tickets requested by the user.
    :type requested_tickets: int
    :param provisional_id: Temporary booking ID reserved for this draft.
    :type provisional_id: str
    :param proposed_seats: Current preview allocation of seats.
    :type proposed_seats: list[Seat]
    :param start_override: User-specified starting seat if reseating manually.
    :type start_override: Optional[Seat]
    """

    requested_tickets: int
    provisional_id: str
    proposed_seats: list[Seat] = field(default_factory=list)
    start_override: Optional[Seat] = None


@dataclass(slots=True)
class AppContext:
    """Durable application state across the lifetime of the program.

    :param theater: The current theater configuration and grid.
    :type theater: Theater
    :param bookings: Dictionary of confirmed bookings keyed by booking ID.
    :type bookings: dict[str, Booking]
    :param next_seq: Sequence counter for generating new booking IDs.
    :type next_seq: int
    :param draft: Current in-progress booking (``None`` if no booking underway).
    :type draft: Optional[DraftBooking]
    """

    theater: Theater
    bookings: dict[str, Booking] = field(default_factory=dict)
    next_seq: int = 1
    draft: Optional[DraftBooking] = None

    def generate_booking_id(self) -> str:
        """Generate the next booking ID and increment the sequence.

        :return: Booking ID of the form ``GIC0001``.
        :rtype: str
        """
        booking_id = f"GIC{self.next_seq:04d}"
        self.next_seq += 1
        return booking_id
