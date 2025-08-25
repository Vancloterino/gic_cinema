"""Application router (entry point).

This module initializes the theater context, constructs CLI commands,
and routes user input to the selected command.

All functions and classes here avoid business logic; they are orchestration only.
"""

from __future__ import annotations

from typing import Dict, List

from src.cli.command import Command, IO
from src.cli.io import ConsoleIO
from src.cli.registry import get_commands
from src.core.renderers.ascii_renderer import AsciiRenderer
from src.core.services.booking import BookingService
from src.core.validators import parse_init_line
from src.models.context import AppContext
from src.models.entities import Theater


def _render_menu(commands: List[Command], ctx: AppContext, io: IO) -> None:
    """Render the dynamic main menu.

    :param commands: List of command instances in menu order.
    :type commands: list[Command]
    :param ctx: Application context (used for dynamic labels).
    :type ctx: AppContext
    :param io: IO adapter used for printing.
    :type io: IO
    """
    io.newline()
    io.write("Welcome to GIC Cinemas")
    for cmd in commands:
        io.write(cmd.display_label(ctx))


def main() -> None:
    """Program entry point.

    - Prompt user for ``[Title] [Rows] [SeatsPerRow]``.
    - Build command objects (Book, Check, Exit).
    - Loop on user selection and dispatch to the chosen command.
    """
    io: IO = ConsoleIO()

    # Initialization
    while True:
        init = io.prompt("Please enter [Title] [Rows] [SeatsPerRow]:\n> ")
        try:
            title, rows, cols = parse_init_line(init)
            break
        except ValueError as exc:
            io.write(str(exc))

    theater = Theater(title=title, rows=rows, cols=cols)
    ctx = AppContext(theater=theater)

    # Dependencies for commands
    renderer = AsciiRenderer()
    service = BookingService()
    commands: List[Command] = get_commands(renderer=renderer, service=service)
    index: Dict[str, Command] = {cmd.meta.key: cmd for cmd in commands}

    # Main loop
    while True:
        _render_menu(commands, ctx, io)
        choice = io.prompt("Please enter your selection:\n> ").strip()
        cmd = index.get(choice)
        if not cmd:
            io.write("Invalid selection. Please choose one of the listed options.")
            continue
        cmd.run(ctx, io)
