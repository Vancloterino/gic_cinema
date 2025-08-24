"""Unit tests for seat utilities (row/col conversions, parsing, formatting)."""

from __future__ import annotations

import pytest

from src.utils.seat_utils import (
    row_index_to_letter,
    row_letter_to_index,
    parse_seat_code,
    format_seat_code,
)


def test_row_index_to_letter_valid() -> None:
    assert row_index_to_letter(0) == "A"
    assert row_index_to_letter(25) == "Z"


@pytest.mark.parametrize("bad", [-1, 26, 100])
def test_row_index_to_letter_invalid(bad: int) -> None:
    with pytest.raises(ValueError):
        row_index_to_letter(bad)


def test_row_letter_to_index_valid() -> None:
    assert row_letter_to_index("A") == 0
    assert row_letter_to_index("a") == 0
    assert row_letter_to_index("Z") == 25


@pytest.mark.parametrize("bad", ["", "AA", "1", "-", "_"])
def test_row_letter_to_index_invalid(bad: str) -> None:
    with pytest.raises(ValueError):
        row_letter_to_index(bad)


def test_parse_seat_code_ok() -> None:
    seat = parse_seat_code("B03")
    assert seat.row == "B" and seat.col == 3

    seat2 = parse_seat_code("c9")
    assert seat2.row == "C" and seat2.col == 9


@pytest.mark.parametrize("bad", ["", "3B", "B0x", "BB03", "B"])
def test_parse_seat_code_invalid(bad: str) -> None:
    with pytest.raises(ValueError):
        parse_seat_code(bad)


def test_format_seat_code() -> None:
    assert format_seat_code(0, 1) == "A01"
    assert format_seat_code(2, 12) == "C12"
