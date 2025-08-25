"""Book tickets command."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.cli.command import Command, CommandMeta, IO
from src.core.renderers.base import Renderer
from src.core.services.booking import BookingService
from src.core.validators import parse_ticket_count, validate_start_seat
from src.models.context import AppContext
from src.models.entities import Seat
from src.core.seat_utils import parse_seat_code


@dataclass(slots=True)
class BookContext:
    """Ephemeral state for the book-tickets flow.

    :param requested_tickets: Number of requested tickets.
    :type requested_tickets: int
    :param provisional_id: Provisional booking identifier.
    :type provisional_id: str
    :param preview_seats: Current preview seats for confirmation or reseat.
    :type preview_seats: list[Seat]
    """

    requested_tickets: int = 0
    provisional_id: str = ""
    preview_seats: list[Seat] = field(default_factory=list)


class BookCommand(Command):
    """Reserve seats via auto-allocation with optional manual reseating."""

    meta = CommandMeta(
        key="1",
        label="Book tickets",
        help="Reserve seats with auto-allocation and optional manual reseating.",
    )

    def __init__(self, renderer: Renderer, service: BookingService) -> None:
        """Create the command with injected dependencies.

        :param renderer: Seat map renderer.
        :type renderer: Renderer
        :param service: Booking service for preview/commit.
        :type service: BookingService
        """
        self._r = renderer
        self._svc = service

    def display_label(self, ctx: AppContext) -> str:
        """Return a dynamic menu label including availability.

        :param ctx: Application context.
        :type ctx: AppContext
        :return: Menu label with title and available seats.
        :rtype: str
        """
        available = ctx.theater.available()
        return f"[{self.meta.key}] {self.meta.label} for {ctx.theater.title} ({available} seats available)"

    def run(self, ctx: AppContext, io: IO) -> None:
        """Run the booking flow.

        Steps
        -----
        1. Ask for ticket count.
        2. Show default auto-allocation preview.
        3. Allow manual reseat from a start seat (optional).
        4. Commit on acceptance.
        """
        flow = BookContext()

        while True:
            raw = io.prompt(
                "Enter number of tickets to book, or enter blank to go back to main menu:\n> "
            ).strip()
            if raw == "":
                return
            try:
                flow.requested_tickets = parse_ticket_count(raw)
            except ValueError as exc:
                io.write(str(exc))
                continue

            try:
                preview = self._svc.preview_auto(ctx, flow.requested_tickets)
            except Exception as exc:
                io.write(str(exc))
                continue

            if not preview:
                io.write("Unable to allocate seats. Please try a smaller number.")
                continue

            flow.preview_seats = preview
            flow.provisional_id = self._svc.new_provisional_id(ctx)

            io.write(
                f"Successfully reserved {flow.requested_tickets} {ctx.theater.title} tickets."
            )
            io.write(f"Booking id: {flow.provisional_id}")
            io.write("Selected seats:")
            io.write(self._r.seat_map(ctx.theater, preview_seats=flow.preview_seats))

            # Reseat loop
            while True:
                raw_pos = io.prompt(
                    "Enter blank to accept seat selection, or enter new seating position:\n> "
                ).strip()
                if raw_pos == "":
                    self._svc.commit_booking(
                        ctx, flow.provisional_id, flow.preview_seats
                    )
                    io.write(f"Booking id: {flow.provisional_id} confirmed.")
                    return

                try:
                    start_seat = parse_seat_code(raw_pos)
                    validate_start_seat(ctx.theater, start_seat)
                except ValueError as exc:
                    io.write(str(exc))
                    continue

                mpreview = self._svc.preview_manual(
                    ctx, flow.requested_tickets, start_seat
                )
                if not mpreview:
                    io.write(
                        "Unable to allocate from that position. Please try another start seat or press Enter to accept the suggestion."
                    )
                    continue

                flow.preview_seats = mpreview
                io.write("Updated selection:")
                io.write(
                    self._r.seat_map(ctx.theater, preview_seats=flow.preview_seats)
                )
