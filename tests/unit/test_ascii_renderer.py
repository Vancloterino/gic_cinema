"""Unit tests for ASCII rendering of seat maps."""

from __future__ import annotations

from src.core.renderers.ascii_renderer import AsciiRenderer
from src.models.entities import Seat, Theater


def test_render_order_and_header_footer() -> None:
    t = Theater(title="Inception", rows=2, cols=4)
    out = AsciiRenderer().seat_map(t)
    lines = out.splitlines()

    # Header and divider
    assert "S C R E E N" in lines[0]
    assert set(lines[1]) == {"-"} and len(lines[1]) >= 18

    # Row order: back to front -> B first, then A
    assert lines[2].startswith("B")
    assert lines[3].startswith("A")

    # Footer seat numbers aligned under seats
    assert lines[-1].strip().startswith("1 2 3 4")


def test_render_highlights_current_booking() -> None:
    t = Theater(title="Inception", rows=2, cols=4)
    # Occupy A02 with booking 1, B03 with booking 2
    t.grid[0][1] = "GIC0001"  # A02
    t.grid[1][2] = "GIC0002"  # B03

    out = AsciiRenderer().seat_map(t, current_booking_id="GIC0001")
    lines = out.splitlines()
    a_line = next(line for line in lines if line.startswith("A"))
    b_line = next(line for line in lines if line.startswith("B"))

    a_cells = a_line.split()[1:]  # after "A"
    assert a_cells == [".", "o", ".", "."]

    b_cells = b_line.split()[1:]
    assert b_cells == [".", ".", "#", "."]


def test_render_preview_overrides_and_other_bookings_marked() -> None:
    t = Theater(title="Inception", rows=2, cols=4)
    # Occupy B02 with existing booking
    t.grid[1][1] = "GIC9999"  # B02

    preview = [Seat("A", 3), Seat("A", 4)]
    out = AsciiRenderer().seat_map(t, preview_seats=preview)
    lines = out.splitlines()
    a_line = next(line for line in lines if line.startswith("A"))
    b_line = next(line for line in lines if line.startswith("B"))

    a_cells = a_line.split()[1:]
    assert a_cells == [".", ".", "o", "o"]

    b_cells = b_line.split()[1:]
    assert b_cells == [".", "#", ".", "."]
