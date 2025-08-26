from src.core.allocation import center_col_order, auto_allocate, manual_allocate
from src.models.entities import Seat, Theater


def test_center_col_order_even() -> None:
    # 10 seats -> [5,6,4,7,3,8,2,9,1,10]
    assert center_col_order(10) == [5, 6, 4, 7, 3, 8, 2, 9, 1, 10]


def test_center_col_order_odd() -> None:
    # 9 seats -> [5,4,6,3,7,2,8,1,9]
    assert center_col_order(9) == [5, 4, 6, 3, 7, 2, 8, 1, 9]


def test_auto_allocate_basic_center_first() -> None:
    t = Theater(title="Inception", rows=3, cols=6)
    seats = auto_allocate(t, 4)
    assert seats is not None
    assert [s.code() for s in seats] == ["A03", "A04", "A02", "A05"]


def test_auto_allocate_overflow_to_next_row() -> None:
    t = Theater(title="Inception", rows=2, cols=4)
    # Row A capacity 4, need 6 total -> should overflow to row B for 2 seats
    seats = auto_allocate(t, 6)
    assert seats is not None
    # Row A in order: [2,3,1,4], then Row B: [2,3]
    assert [s.code() for s in seats] == ["A02", "A03", "A01", "A04", "B02", "B03"]


def test_auto_allocate_skips_already_booked() -> None:
    t = Theater(title="Inception", rows=1, cols=6)
    # Occupy A03 and A04 (center pair)
    t.grid[0][2] = "GIC0001"
    t.grid[0][3] = "GIC0001"
    seats = auto_allocate(t, 3)
    assert seats is not None
    # Next available by order: A02, A05, A01
    assert [s.code() for s in seats] == ["A02", "A05", "A01"]


def test_manual_allocate_from_start_rightward() -> None:
    t = Theater(title="Inception", rows=2, cols=6)
    seats = manual_allocate(t, 4, Seat("B", 3))
    assert seats is not None
    assert [s.code() for s in seats] == ["B03", "B04", "B05", "B06"]


def test_manual_allocate_overflow_uses_default_on_next_rows() -> None:
    t = Theater(title="Inception", rows=2, cols=4)
    seats = manual_allocate(t, 6, Seat("A", 3))
    assert seats is not None
    # Same row to the right: A03, A04 (2 seats), need 4 more
    # Next row default order: B02, B03, B01, B04
    assert [s.code() for s in seats] == ["A03", "A04", "B02", "B03", "B01", "B04"]


def test_allocate_insufficient_capacity_returns_none() -> None:
    t = Theater(title="Inception", rows=1, cols=4)
    # Occupy three seats -> only one left
    t.grid[0][0] = "GIC0001"
    t.grid[0][1] = "GIC0001"
    t.grid[0][2] = "GIC0001"
    assert auto_allocate(t, 2) is None
    assert manual_allocate(t, 2, Seat("A", 1)) is None

def test_manual_allocate_scans_right_skipping_taken() -> None:
    t = Theater("Film", rows=2, cols=10)
    # Mark some seats in B row as taken: B03..B06
    t.grid[1][2] = "X"  # B03
    t.grid[1][3] = "X"  # B04
    t.grid[1][4] = "X"  # B05
    t.grid[1][5] = "X"  # B06
    # Start at B05
    # Expect it to pick B07, B08 for k=2 (scan right, skip taken, don't jump to C row)
    seats = manual_allocate(t, 2, Seat("B", 5))
    assert seats is not None
    assert [s.code() for s in seats] == ["B07", "B08"]
