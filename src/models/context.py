"""Application context (in-memory state)."""

from dataclasses import dataclass, field
from typing import Dict

from src.models.entities import Theater, Booking


@dataclass(slots=True)
class AppContext:
    """In-memory application context.

    :param theater: Theater configuration and occupancy.
    :type theater: Theater
    :param bookings: Booking registry mapping ``booking_id → Booking``.
    :type bookings: dict[str, Booking]
    :param next_seq: Next numeric sequence for booking IDs.
    :type next_seq: int
    """

    theater: Theater
    bookings: Dict[str, Booking] = field(default_factory=dict)
    next_seq: int = 1

    def generate_booking_id(self) -> str:
        """Return a new booking ID like ``GIC0001`` and advance the sequence.

        :return: Booking identifier string.
        :rtype: str
        """
        bid = f"GIC{self.next_seq:04d}"
        self.next_seq += 1
        return bid
