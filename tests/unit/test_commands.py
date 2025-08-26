import pytest

from src.cli.commands.book import BookCommand
from src.cli.commands.check import CheckCommand
from src.cli.commands.exit import ExitCommand
from src.core.services.booking import BookingService
from src.core.renderers.ascii_renderer import AsciiRenderer
from src.models.context import AppContext
from src.models.entities import Theater


def test_book_command_accepts_default_selection(script_io_factory) -> None:
    # Inputs: ticket count "3", then blank to accept preview
    io = script_io_factory(["3", ""])
    ctx = AppContext(theater=Theater("Film", 2, 5))
    cmd = BookCommand(renderer=AsciiRenderer(), service=BookingService())

    cmd.run(ctx, io)

    assert len(ctx.bookings) == 1
    bid = next(iter(ctx.bookings))
    assert bid.startswith("GIC")
    assert len(ctx.bookings[bid].seats) == 3
    # Some output should include the booking id line emitted by the command
    assert any("Booking id:" in out for out in io.outputs)


def test_check_command_renders_when_found(script_io_factory) -> None:
    # Prepare a booking
    io = script_io_factory(["GIC0001", ""])  # then blank to exit
    ctx = AppContext(theater=Theater("Film", 1, 3))
    svc = BookingService()
    bid = ctx.generate_booking_id()
    preview = svc.preview_auto(ctx, 2)
    assert preview is not None
    svc.commit_booking(ctx, bid, preview)

    cmd = CheckCommand(renderer=AsciiRenderer(), service=svc)
    cmd.run(ctx, io)

    # Should have printed some ASCII map lines (e.g., SCREEN divider)
    assert any("S C R E E N" in out for out in io.outputs)


def test_exit_display_label() -> None:
    ctx = AppContext(theater=Theater("Film", 1, 1))
    cmd = ExitCommand()
    assert cmd.display_label(ctx).startswith("[3] Exit")


def test_exit_command_exits_with_message(script_io_factory) -> None:
    io = script_io_factory([])  # ExitCommand doesn't prompt
    ctx = AppContext(theater=Theater("Film", 1, 1))
    cmd = ExitCommand()

    with pytest.raises(SystemExit) as excinfo:
        cmd.run(ctx, io)

    assert excinfo.value.code == 0
    assert any(
        "Thank you for using GIC Cinemas system. Bye!" in out for out in io.outputs
    )
