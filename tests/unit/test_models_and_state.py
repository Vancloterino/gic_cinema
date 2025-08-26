from src.models.entities import Seat, Booking, Theater
from src.models.context import AppContext


def test_seat_code_zero_pad() -> None:
    s = Seat("B", 3)
    assert s.code() == "B03"


def test_booking_dataclass_defaults() -> None:
    b = Booking(booking_id="GIC0001")
    assert b.booking_id == "GIC0001"
    assert b.seats == []


def test_theater_capacity_and_available() -> None:
    t = Theater(title="Inception", rows=3, cols=4)
    assert t.capacity() == 12
    assert t.available() == 12

    # occupy a couple of seats
    t.grid[0][0] = "GIC0001"
    t.grid[2][3] = "GIC0002"
    assert t.available() == 10


def test_app_context_generate_booking_id_sequence(theater_4x6: Theater) -> None:
    ctx = AppContext(theater=theater_4x6)
    assert ctx.generate_booking_id() == "GIC0001"
    assert ctx.generate_booking_id() == "GIC0002"
    assert ctx.next_seq == 3
