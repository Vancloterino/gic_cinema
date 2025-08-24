"""Unit tests for ASCII rendering of seat maps."""

from __future__ import annotations

from src.core.render import render_seat_map
from src.models.entities import Seat, Theater


def test_render_order_and_header_footer() -> None:
    t = Theater(title="Inception", rows=2, cols=4)
    # No bookings
    out = render_seat_map(t)
    lines = out.splitlines()

    # Header and divider
    assert "S C R E E N" in lines[0]
    assert set(lines[1]) == {"-"} and len(lines[1]) >= 18

    # Row order: back to front -> B first, then A
    assert lines[2].startswith("B")
    assert lines[3].startswith("A")

    # Footer seat numbers
    assert lines[-1].strip() == "1 2 3 4"


def test_render_highlights_current_booking() -> None:
    t = Theater(title="Inception", rows=2, cols=4)
    # Occupy A02 with booking 1, B03 with booking 2
    t.grid[0][1] = "GIC0001"  # A02
    t.grid[1][2] = "GIC0002"  # B03

    out = render_seat_map(t, current_booking_id="GIC0001")
    lines = out.splitlines()
    # Extract the A row line
    a_line = next(line for line in lines if line.startswith("A"))
    b_line = next(line for line in lines if line.startswith("B"))

    # A02 should be 'o' (current booking); others in A are '.'
    # A row cells after "A  " -> positions 0..3 map to cols 1..4
    a_cells = a_line.split()[1:]  # strip the "A"
    assert a_cells == [".", "o", ".", "."]

    # B03 is another booking -> '#'
    b_cells = b_line.split()[1:]
    assert b_cells == [".", ".", "#", "."]


def test_render_preview_overrides_and_other_bookings_marked() -> None:
    t = Theater(title="Inception", rows=2, cols=4)
    # Occupy B02 with existing booking
    t.grid[1][1] = "GIC9999"  # B02

    # Preview A03, A04 (draft booking)
    preview = [Seat("A", 3), Seat("A", 4)]
    out = render_seat_map(t, current_booking_id=None, preview_seats=preview)
    lines = out.splitlines()
    a_line = next(line for line in lines if line.startswith("A"))
    b_line = next(line for line in lines if line.startswith("B"))

    # Row A: A03 & A04 are 'o' for preview
    a_cells = a_line.split()[1:]
    assert a_cells == [".", ".", "o", "o"]

    # Row B: B02 is booked by someone else -> '#'
    b_cells = b_line.split()[1:]
    assert b_cells == [".", "#", ".", "."]
