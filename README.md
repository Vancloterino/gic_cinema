# GIC Cinemas Booking System

A small, testable **console booking app** demonstrating seat allocation, manual reseating, booking IDs, and an ASCII seat map — now refactored with a clean **command framework**, **service layer**, and **renderer abstraction**. All in-code docstrings follow **reStructuredText (reST)** format.

---

## ✨ Highlights
- **Command-per-option** CLI (`Book`, `Check`, `Exit`) with small, focused contexts.
- **Service layer** (`BookingService`) centralizes preview/commit logic.
- **Renderer abstraction** with an **ASCII** implementation (easy to swap later).
- **Pure functions** for allocation & validation, making tests simple.
- **reST docstrings** everywhere for future Sphinx/doc builds.
- **Coverage** configured to measure only `src/` (tests excluded).

---

## 📦 Project Layout (current)

```
gic-cinemas/
├─ run_booking_system.py # ▶️ Optional dev entry (if present): python run_booking_system.py
├─ pyproject.toml # Tooling, deps, pytest & coverage settings
├─ README.md
└─ src/
├─ app.py # ▶️ Installed entry point: router (exposes main())
├─ init.py
├─ cli/
│ ├─ command.py # Command base, IO protocol, CommandMeta
│ ├─ io.py # ConsoleIO (prompt/write/newline)
│ ├─ registry.py # Central command registration
│ └─ commands/
│ ├─ book.py # BookCommand (+BookContext)
│ ├─ check.py # CheckCommand
│ └─ exit.py # ExitCommand
├─ core/
│ ├─ allocation.py # Seat allocation (auto/manual), pure functions
│ ├─ errors.py # Domain exceptions
│ ├─ seat_utils.py # Parse/format seats, bounds/vacancy, row/col helpers
│ ├─ validators.py # Parse init/menu/ticket count/booking id; validate start seat
│ ├─ renderers/
│ │ ├─ base.py # Renderer protocol
│ │ └─ ascii_renderer.py # ASCII seat map implementation
│ └─ services/
│ └─ booking.py # BookingService (previews + commits)
└─ models/
├─ context.py # AppContext (bookings, theater, id sequence)
└─ entities.py # Dataclasses: Seat, Booking, Theater
```

---

## ▶️ Running the App

**Option A — installed console script (recommended):**
```bash
book
```

**Option B — dev entry script:**
If your repo has run_booking_system.py at the root:
```bash
python run_booking_system.py
```

**⚙️ Setup **
```bash
# 1) Create & activate venv
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# 2) Install (editable) with dev tools
pip install -U pip
pip install -e ".[dev]"

```

**🧪 Tests & Coverage**
```bash
pytest
```

**🧠 Design & Assumptions (Brief)**

Architecture

* CLI layer: one command per menu option; each has a tiny context and uses injected dependencies.

* Service layer: BookingService is the single mutation surface (previews/commits).

* Core (pure): allocation, validators, seat utils are fast to test and reuse.
 
* Renderer: protocol-based; currently ASCII. Easy to add TUI/HTML later.
 
* Models: minimal dataclasses (Seat, Booking, Theater) and AppContext for state.

Assumptions

* One screen per run; rectangular grid.

* Row A rendered at the bottom; “SCREEN” at top.

* Auto allocation uses center-outwards priority per row; manual reseat starts from the chosen seat rightwards.

* Booking IDs: GIC0001, GIC0002, … monotonic per session.

* In-memory single-user session; no persistence or concurrency.

**➕ Adding a new CLI option**

* Create a new command in src/cli/commands/<name>.py:

* Subclass Command, define meta, implement display_label() and run().

* Use injected renderer/service (get from get_commands()).

* Register it in src/cli/registry.py in the return list.

* Add focused unit tests with a scripted IO (see ScriptIO in tests/conftest.py).