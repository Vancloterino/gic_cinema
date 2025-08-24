"""Console application loop for the GIC Cinemas booking system.

This module implements a small finite-state loop:
- Initialize theater from a single line: ``[Title] [Rows] [SeatsPerRow]``.
- Show main menu (book / check / exit).
- Booking flow supports auto-allocation and manual reseating preview.
- Check flow renders a specific booking with highlighted seats.

The module uses reST-style docstrings and aims to be Pylint/Black friendly.
"""

from __future__ import annotations

from typing import Iterable, Optional

from src.core.allocation import auto_allocate, manual_allocate
from src.core.validators import (
    parse_booking_id,
    parse_init_line,
    parse_menu_choice,
    parse_ticket_count,
    validate_start_seat,
)
from src.core.render import render_seat_map
from src.models.entities import Booking, Seat, Theater
from src.state.context import AppContext
from src.utils.seat_utils import parse_seat_code


def _prompt(prompt: str) -> str:
    """Read a line of input with basic Ctrl+C handling.

    :param prompt: Prompt text displayed to the user.
    :type prompt: str
    :return: User input without the trailing newline.
    :rtype: str
    """
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print()  # newline for clean exit
        raise SystemExit(130)  # typical SIGINT exit code


def _commit_booking(ctx: AppContext, seats: Iterable[Seat], provisional_id: str) -> None:
    """Persist a booking into the theater grid and registry.

    :param ctx: Application context.
    :type ctx: AppContext
    :param seats: Finalized set of seats to reserve.
    :type seats: Iterable[Seat]
    :param provisional_id: Booking ID reserved for this transaction.
    :type provisional_id: str
    """
    # Mark seats in the grid
    for s in seats:
        row_idx = ord(s.row.upper()) - ord("A")
        ctx.theater.grid[row_idx][s.col - 1] = provisional_id

    # Save booking and clear draft
    ctx.bookings[provisional_id] = Booking(booking_id=provisional_id, seats=list(seats))
    ctx.draft = None


def _book_tickets(ctx: AppContext) -> None:
    """Handle the ticket-booking flow (auto-allocate, optional reseat, confirm).

    :param ctx: Application context.
    :type ctx: AppContext
    """
    while True:
        raw = _prompt(
            "Enter number of tickets to book, or enter blank to go back to main menu:\n> "
        ).strip()
        if raw == "":
            return
        try:
            count = parse_ticket_count(raw)
        except ValueError as exc:
            print(str(exc))
            continue

        available = ctx.theater.available()
        if count > available:
            print(f"Sorry, there are only {available} seats available.")
            continue

        # Provisional ID
        provisional_id = ctx.generate_booking_id()

        # Default allocation preview
        preview = auto_allocate(ctx.theater, count)
        if not preview:
            print("Unable to allocate seats. Please try a smaller number.")
            continue

        print(f"Successfully reserved {count} {ctx.theater.title} tickets.")
        print(f"Booking id: {provisional_id}")
        print("Selected seats:")
        print(render_seat_map(ctx.theater, preview_seats=preview))

        # Re-seat loop
        while True:
            raw_pos = _prompt(
                "Enter blank to accept seat selection, or enter new seating position:\n> "
            ).strip()
            if raw_pos == "":
                _commit_booking(ctx, preview, provisional_id)
                print(f"Booking id: {provisional_id} confirmed.")
                return

            # Try manual allocation from a user-provided start seat
            try:
                start_seat = parse_seat_code(raw_pos)
                validate_start_seat(ctx.theater, start_seat)
            except ValueError as exc:
                print(str(exc))
                continue

            mpreview = manual_allocate(ctx.theater, count, start_seat)
            if not mpreview:
                print(
                    "Unable to allocate from that position. Please try another start seat or press Enter to accept the suggestion."
                )
                continue

            preview = mpreview
            print("Updated selection:")
            print(render_seat_map(ctx.theater, preview_seats=preview))


def _check_bookings(ctx: AppContext) -> None:
    """Handle the booking-check flow by booking ID.

    :param ctx: Application context.
    :type ctx: AppContext
    """
    while True:
        raw = _prompt("Enter booking id, or enter blank to go back to main menu:\n> ")
        bid = raw.strip()
        if bid == "":
            return
        try:
            bid_norm = parse_booking_id(bid)
        except ValueError as exc:
            print(str(exc))
            continue

        booking = ctx.bookings.get(bid_norm)
        if not booking:
            print("Booking id not found. Please try again.")
            continue

        print(render_seat_map(ctx.theater, current_booking_id=bid_norm))


def main() -> None:
    """Application entry point.

    Initializes the theater, then loops on the main menu until the user exits.
    """
    # Initialization
    while True:
        init = _prompt("Please enter [Title] [Rows] [SeatsPerRow]:\n> ")
        try:
            title, rows, cols = parse_init_line(init)
            break
        except ValueError as exc:
            print(str(exc))

    theater = Theater(title=title, rows=rows, cols=cols)
    ctx = AppContext(theater=theater)

    # Menu loop
    while True:
        available = ctx.theater.available()
        print("\nWelcome to GIC Cinemas")
        print(f"[1] Book tickets for {ctx.theater.title} ({available} seats available)")
        print("[2] Check bookings")
        print("[3] Exit")
        choice_raw = _prompt("Please enter your selection:\n> ")

        try:
            choice = parse_menu_choice(choice_raw)
        except ValueError as exc:
            print(str(exc))
            continue

        if choice == 1:
            _book_tickets(ctx)
        elif choice == 2:
            _check_bookings(ctx)
        else:
            print("Thank you for using GIC Cinemas system. Bye!")
            raise SystemExit(0)
