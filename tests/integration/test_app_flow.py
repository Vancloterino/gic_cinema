"""Integration tests for the console app flow.

These tests simulate keyboard input and assert on printed output.
"""

import re
from typing import Iterator, List

import pytest

from src.app import run_app


def _input_feeder(lines: List[str]) -> Iterator[str]:
    """Yield successive inputs for monkeypatched ``input``."""
    for line in lines:
        yield line


def test_flow_book_accept_exit(
    monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture[str]
) -> None:
    """Initialize, book 3 tickets (accept default), then exit."""
    inputs = [
        "Inception 2 4",  # init
        "1",  # menu -> book
        "3",  # ticket count
        "",  # accept default selection
        "3",  # exit
    ]
    feeder = _input_feeder(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(feeder))

    with pytest.raises(SystemExit) as ei:
        run_app()
    assert ei.value.code == 0

    out = capfd.readouterr().out
    # Booking id announced and confirmed
    assert re.search(r"Booking id:\s+GIC\d{4}", out)
    assert "confirmed" in out
    # Seat map printed at least once
    assert "S C R E E N" in out
    # Menu shown with updated available seats (2x4=8 total; after 3 seats -> 5 left)
    assert "Welcome to GIC Cinemas" in out
    assert "(5 seats available)" in out
    # Exit message
    assert "Thank you for using GIC Cinemas system. Bye!" in out


def test_flow_book_reseat_check_exit(
    monkeypatch: pytest.MonkeyPatch, capfd: pytest.CaptureFixture[str]
) -> None:
    """Initialize, book 3 tickets, reseat from B02, check the booking, then exit."""
    inputs = [
        "Inception 2 4",  # init
        "1",  # menu -> book
        "3",  # ticket count
        "B02",  # reseat starting at B02
        "",  # accept updated selection
        "2",  # menu -> check bookings
        "GIC0001",  # check first booking
        "",  # back to menu from check
        "3",  # exit
    ]
    feeder = _input_feeder(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(feeder))

    with pytest.raises(SystemExit) as ei:
        run_app()
    assert ei.value.code == 0

    out = capfd.readouterr().out
    # Ensure reseat message and updated map appeared
    assert "Updated selection:" in out
    # Check bookings flow renders the map highlighting the booking
    assert "Check bookings" in out
    assert re.search(r"Booking id:\s+GIC0001", out) or "GIC0001" in out
    assert "S C R E E N" in out
    assert "Thank you for using GIC Cinemas system. Bye!" in out
