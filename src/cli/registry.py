"""Command registry."""

from typing import List

from src.cli.command import Command
from src.cli.commands.book import BookCommand
from src.cli.commands.check import CheckCommand
from src.cli.commands.exit import ExitCommand
from src.core.renderers.base import Renderer
from src.core.services.booking import BookingService


def get_commands(renderer: Renderer, service: BookingService) -> List[Command]:
    """Return command instances in menu order.

    :param renderer: Seat map renderer to inject.
    :type renderer: Renderer
    :param service: Booking service to inject.
    :type service: BookingService
    :return: Commands in display order.
    :rtype: list[Command]
    """
    return [
        BookCommand(renderer=renderer, service=service),
        CheckCommand(renderer=renderer, service=service),
        ExitCommand(),
    ]
