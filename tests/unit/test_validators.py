import pytest

from src.core.validators import (
    parse_init_line,
    parse_ticket_count,
    parse_booking_id,
    validate_start_seat,
)
from src.models.entities import Theater, Seat


def test_validate_start_seat_ok() -> None:
    t = Theater(title="Inception", rows=2, cols=4)
    validate_start_seat(t, Seat("A", 1))  # should not raise


def test_validate_start_seat_out_of_bounds() -> None:
    t = Theater(title="Inception", rows=2, cols=4)
    with pytest.raises(ValueError):
        validate_start_seat(t, Seat("C", 1))  # row out of bounds
    with pytest.raises(ValueError):
        validate_start_seat(t, Seat("A", 5))  # col out of bounds


def test_validate_start_seat_already_taken() -> None:
    t = Theater(title="Inception", rows=2, cols=4)
    t.grid[0][0] = "GIC9999"  # A01 occupied
    with pytest.raises(ValueError):
        validate_start_seat(t, Seat("A", 1))


def test_parse_init_line_basic() -> None:
    title, rows, cols = parse_init_line("Inception 8 10")
    assert title == "Inception"
    assert rows == 8
    assert cols == 10


def test_parse_init_line_title_with_spaces() -> None:
    title, rows, cols = parse_init_line("The Dark Knight 12 20")
    assert title == "The Dark Knight"
    assert rows == 12
    assert cols == 20


@pytest.mark.parametrize(
    "text",
    [
        "",  # empty
        "OnlyTitle",  # too few parts
        "NoNumbers x y",  # not integers
        "Film 0 5",  # invalid rows
        "Film 27 5",  # invalid rows
        "Film 5 0",  # invalid cols
        "Film 5 51",  # invalid cols
        "  7  9",  # missing title
    ],
)
def test_parse_init_line_invalid(text: str) -> None:
    with pytest.raises(ValueError):
        parse_init_line(text)


@pytest.mark.parametrize("good,expected", [("1", 1), ("03", 3), ("10", 10)])
def test_parse_ticket_count_valid(good: str, expected: int) -> None:
    assert parse_ticket_count(good) == expected


@pytest.mark.parametrize("bad", ["", "0", "-1", "x", "  "])
def test_parse_ticket_count_invalid(bad: str) -> None:
    with pytest.raises(ValueError):
        parse_ticket_count(bad)


@pytest.mark.parametrize("good", ["GIC0001", "gic1234", "GIC9999"])
def test_parse_booking_id_valid(good: str) -> None:
    assert parse_booking_id(good).startswith("GIC")


@pytest.mark.parametrize("bad", ["", "GIC1", "GIC00001", "ABC1234", "GIC12A4"])
def test_parse_booking_id_invalid(bad: str) -> None:
    with pytest.raises(ValueError):
        parse_booking_id(bad)
