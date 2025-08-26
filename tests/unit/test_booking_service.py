import pytest

from src.core.services.booking import BookingService
from src.core.errors import CapacityExceeded, NotFound
from src.models.entities import Seat, Theater
from src.models.context import AppContext


def test_preview_auto_and_commit() -> None:
    t = Theater("Film", rows=2, cols=3)
    ctx = AppContext(theater=t)
    svc = BookingService()

    preview = svc.preview_auto(ctx, 2)
    assert preview is not None and len(preview) == 2

    bid = svc.new_provisional_id(ctx)
    svc.commit_booking(ctx, bid, preview)

    # Grid should have exactly 2 occupied cells
    assert sum(1 for r in t.grid for c in r if c is not None) == 2
    assert bid in ctx.bookings
    assert len(ctx.bookings[bid].seats) == 2


def test_preview_manual_from_start() -> None:
    t = Theater("Film", rows=1, cols=4)
    ctx = AppContext(theater=t)
    svc = BookingService()

    preview = svc.preview_manual(ctx, 3, Seat("A", 2))
    # A2, A3, A4 should be chosen in this simple case
    assert preview and [s.code() for s in preview] == ["A02", "A03", "A04"]


def test_capacity_exceeded() -> None:
    t = Theater("Film", rows=1, cols=2)
    ctx = AppContext(theater=t)
    svc = BookingService()

    with pytest.raises(CapacityExceeded):
        svc.preview_auto(ctx, 3)


def test_get_booking_not_found() -> None:
    t = Theater("Film", rows=1, cols=2)
    ctx = AppContext(theater=t)
    svc = BookingService()

    with pytest.raises(NotFound):
        svc.get_booking(ctx, "GIC0001")
