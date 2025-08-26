# GIC Cinemas Booking System

A small, testable **console booking app** demonstrating seat allocation, manual reseating, booking IDs, and a seat map.



## Design and Assumptions

**Design**


* CLI layer: one command per menu option; each has a tiny context and uses injected dependencies.
* Service layer: BookingService is the single mutation surface (previews/commits).
* Pure functions: allocation, validators, seat utils for ease of test and reuse.
* Renderer: protocol-based; currently ASCII.
* Models: minimal dataclasses (Seat, Booking, Theater) and AppContext for state.
* reST docstrings format for future Sphinx/doc builds.

**Assumptions** $$TBD

* One screen per run; rectangular grid.
* Row A rendered at the bottom; “SCREEN” at top.
* Auto allocation uses center-outwards priority per row; manual reseat starts from the chosen seat rightwards.
* In-memory single-user session; no persistence or concurrency.


---

## 📦 Project Layout

```
gic-cinemas/
├─ src/
│  ├─ __init__.py
│  ├─ app.py
│  ├─ cli/
│  │  ├─ __init__.py
│  │  ├─ command.py           # Command base, IO protocol, CommandMeta
│  │  ├─ io.py                # ConsoleIO (prompt/write/newline)
│  │  ├─ registry.py          # Central command registration
│  │  └─ commands/
│  │     ├─ __init__.py
│  │     ├─ book.py           # BookCommand (+BookContext)
│  │     ├─ check.py          # CheckCommand
│  │     └─ exit.py           # ExitCommand
│  ├─ core/
│  │  ├─ __init__.py
│  │  ├─ allocation.py        # Seat allocation (auto/manual)
│  │  ├─ errors.py            # Domain exceptions
│  │  ├─ seat_utils.py        # Parse/format seats, row/col helpers
│  │  ├─ validators.py        # Parse init/menu/ticket count/booking id
│  │  └─ renderers/
│  │     ├─ __init__.py
│  │     ├─ base.py           # Renderer protocol
│  │     └─ ascii_renderer.py # Seat map implementation
│  └─ services/
│     ├─ __init__.py
│     └─ booking.py           # BookingService (previews + commits)
│
│  └─ models/
│     ├─ __init__.py
│     ├─ context.py           # AppContext (bookings, theater, id sequence)
│     └─ entities.py          # Dataclasses: Seat, Booking, Theater
├─ tests/                      # Test suite
├─ poetry.lock
├─ pyproject.toml              # Tooling, deps, pytest & coverage settings
├─ README.md
└─ run_booking_system.py       # ▶️ Script entry point: `python run_booking_system.py`

```




## ⚙️ Setup

**Prerequisites:**  
- Python `^3.11`  
- Poetry `^2.0.0`


Installing dependencies:
Using Poetry

```bash
poetry env activate
poetry install
```


## ▶️ Usage

Run the ETL pipeline
```bash
python run_booking_system.py
```

## 🧪 Tests & Coverage
```bash
pytest --cov-report=term
```

