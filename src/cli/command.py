"""Command abstractions and IO protocol."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

from src.models.context import AppContext


class IO(Protocol):
    """I/O protocol abstraction for testability.

    Implementations should provide console-like behavior, but tests may use
    scripted or in-memory stubs.

    .. method:: prompt(text)
       :noindex:

       Display *text* and return a single input line.

    .. method:: write(text)
       :noindex:

       Write *text* with a trailing newline.

    .. method:: newline()
       :noindex:

       Write a single newline for spacing.
    """

    def prompt(self, text: str) -> str: ...
    def write(self, text: str) -> None: ...
    def newline(self) -> None: ...


@dataclass(frozen=True, slots=True)
class CommandMeta:
    """Metadata describing a CLI command.

    :param key: Unique menu key, e.g. ``"1"``.
    :type key: str
    :param label: Human-readable menu label.
    :type label: str
    :param help: Brief description shown in help.
    :type help: str
    """

    key: str
    label: str
    help: str


class Command(ABC):
    """Base class for CLI commands."""

    meta: CommandMeta

    @abstractmethod
    def display_label(self, ctx: AppContext) -> str:
        """Return the label shown in the menu (may be dynamic).

        :param ctx: Application context.
        :type ctx: AppContext
        :return: Menu label.
        :rtype: str
        """

    @abstractmethod
    def run(self, ctx: AppContext, io: IO) -> None:
        """Execute the command.

        :param ctx: Application context.
        :type ctx: AppContext
        :param io: IO adapter.
        :type io: IO
        """
