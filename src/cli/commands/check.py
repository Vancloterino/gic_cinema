"""Check bookings command."""

from dataclasses import dataclass

from src.cli.command import Command, CommandMeta, IO
from src.core.renderers.base import Renderer
from src.core.services.booking import BookingService
from src.core.validators import parse_booking_id
from src.models.context import AppContext


@dataclass(slots=True)
class CheckContext:
    """Ephemeral state for the check-booking flow.

    :param last_id: Last successfully viewed booking ID.
    :type last_id: str
    """

    last_id: str = ""


class CheckCommand(Command):
    """Render the seat map highlighting a specific booking."""

    meta = CommandMeta(
        key="2",
        label="Check bookings",
        help="View seat map highlighting a given booking ID.",
    )

    def __init__(self, renderer: Renderer, service: BookingService) -> None:
        """Create the command with injected dependencies.

        :param renderer: Seat map renderer.
        :type renderer: Renderer
        :param service: Booking service (not used yet, but reserved for symmetry).
        :type service: BookingService
        """
        self._r = renderer
        self._svc = service  # reserved for future features

    def display_label(self, ctx: AppContext) -> str:  # noqa: ARG002
        """Return the static menu label for this command.

        :param ctx: Application context (unused).
        :type ctx: AppContext
        :return: Menu label.
        :rtype: str
        """
        return f"[{self.meta.key}] {self.meta.label}"

    def run(self, ctx: AppContext, io: IO) -> None:
        """Run the check-booking flow.

        Prompts for a booking ID; if found, renders the seat map with that
        booking highlighted. Entering a blank line returns to the main menu.
        """
        flow = CheckContext()

        while True:
            raw = io.prompt(
                "Enter booking id, or enter blank to go back to main menu:\n> "
            )
            bid = raw.strip()
            if bid == "":
                return
            try:
                flow.last_id = parse_booking_id(bid)
            except ValueError as exc:
                io.write(str(exc))
                continue

            if flow.last_id not in ctx.bookings:
                io.write("Booking id not found. Please try again.")
                continue

            io.write(self._r.seat_map(ctx.theater, current_booking_id=flow.last_id))
