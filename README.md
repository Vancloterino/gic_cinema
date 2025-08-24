# GIC Cinemas Booking System

A small, testable **console booking app** that demonstrates seat allocation, manual reseating, booking IDs, and an ASCII seat map.

> Tech focus: clear separation of concerns, reST-style docstrings in code, unit/integration tests, and Black + Pylint for quality.


## ✅ Features
- Initialize with `[Title] [Rows] [SeatsPerRow]` (e.g., `Inception 8 10`).
- Book tickets with **default auto-allocation** (center-outwards, row A first), or **manual reseating** from a start seat (e.g., `B03`).
- Check a booking by ID (`GIC0001`, `GIC0002`, …).
- ASCII seat map with legend: `.` empty, `o` highlighted (current/preview), `#` other bookings.


## 🗂️ Project Layout (Entry Points Marked)
```
gic-cinemas/
├─ run_booking_system.py # ▶️ Dev entry point (run directly with Python)
├─ pyproject.toml # Project config: deps, Black, Pylint, console script
├─ README.md # This file
├─ src/
│ ├─ app.py # ▶️ Installed entry point: exposes main() (console script book)
│ ├─ core/
│ │ ├─ allocation.py # Seat allocation logic (auto + manual)
│ │ ├─ render.py # ASCII seat map renderer
│ │ └─ validators.py # Parse/validate init line, menu, ticket counts, booking ids, seat starts
│ ├─ models/
│ │ └─ entities.py # Dataclasses: Seat, Booking, Theater
│ ├─ state/
│ │ └─ context.py # AppContext (durable), DraftBooking (ephemeral)
│ └─ utils/
│ └─ seat_utils.py # Row/col conversions, seat code parse/format, bounds & vacancy
└─ tests/
├─ conftest.py # Shared fixtures & (optional) sys.path setup
├─ unit/
│ ├─ test_seat_utils.py
│ ├─ test_models_and_state.py
│ ├─ test_validators.py
│ └─ test_allocation.py
└─ integration/
└─ test_app_flow.py # Simulated I/O for end-to-end menu/booking/check
```


## 🧰 Prerequisites
- Python **3.11+**
- (Recommended) A virtual environment


## ⚙️ Setup (development)

```bash
# 1) Create and activate a venv
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

```

▶️ Run the App
```
python run_booking_system.py
```

# 🧪 Tests

Run the test suite:
```
pytest
```

# 🏗️ Design Notes

Separation of Concerns:

- models/: data structures only
- state/: durable app state + draft state
- core/: allocation, validators, rendering
- utils/: seat parsing/conversions
- app.py: small CLI loop, uses pure services

Allocation: center-outwards per row; row A filled first; overflow to next rows.
Rendering: single pure function that highlights either preview seats or a booking ID.
FSM-lite: booking flow is transactional—nothing is committed until user accepts.

# 📎 Best Practices Included

- reST docstrings for functions/classes (future Sphinx-friendly).
- Unit/integration tests with fixtures.
- Black + Pylint config in pyproject.toml (88 chars, Python 3.11).
- Editable install for clean imports & console script (book).

🧠 Design & Underlying Assumptions (Brief)

**Guiding principles**
- **Separation of concerns:** `models/` are pure dataclasses, `state/` holds durable UI-independent state, `core/` contains business logic (allocation, validators, rendering), `utils/` houses small helpers, and `app.py` is the thin CLI orchestrator.
- **Purity & testability:** Allocation and rendering are **pure functions** (no I/O, no mutation of shared state), enabling straightforward unit tests and snapshot-style checks.
- **Single commit point:** During booking, the grid is **not** mutated until the user confirms; previews are ephemeral → easy rollback.

**Key assumptions from the spec**
- **One movie per run** with a **rectangular** grid.
- **Row A is treated as furthest from the screen** for allocation (matches examples), even though the word “SCREEN” is printed at the top of the map.
- **Default allocation:** center-outwards within a row; **even seat counts prefer the left-of-center first**; overflow proceeds to the **next row closer** to the screen.
- **Manual reseating:** starts at the user’s seat code (e.g., `B03`), fills **rightward** in that row, then overflows to subsequent rows using the default rule.
- **Contiguity intent:** The algorithm tries to produce adjacent seats by consuming the center-first order; strict contiguity across overflow rows is **not guaranteed**, but behavior aligns with the provided examples.
- **Seat labels:** `A01` format (row A–Z, 1-based columns). Validation enforces bounds (**max 26 rows, 50 columns**) and nonzero column values.
- **Rendering orientation:** rows render **from back to front** (e.g., `H..A`), footer numbers are **indented to align** underneath seats, legend is: `.` empty, `o` current/preview, `#` other bookings.
- **Booking IDs:** monotonic `GIC####` sequence, starting at `GIC0001`.
- **No persistence/concurrency:** All state is in-memory for a **single-user** console session; no file/database storage and no multi-user locking.

**Edge-case behavior**
- Requesting more tickets than available → polite error with current availability.
- Manual start seat must be **in bounds and free**; otherwise, the CLI explains and re-prompts.
- Invalid inputs (menu choice, ticket count, seat code, booking ID) trigger clear validation messages and return to the previous prompt.
- **Check bookings** view highlights only the chosen booking’s seats as `o`, all other booked seats as `#`.

**Extensibility hooks**
- Swap-in persistence (JSON/SQLite) without touching business logic.
- Alternative allocation strategies (e.g., seat pricing, “best view” heuristics).
- Multiple shows/titles (expand `state/` to manage sessions and schedules).