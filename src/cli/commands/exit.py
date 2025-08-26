"""Exit command."""

from src.cli.command import Command, CommandMeta, IO
from src.models.context import AppContext


class ExitCommand(Command):
    """Terminate the application gracefully."""

    meta = CommandMeta(
        key="3",
        label="Exit",
        help="Quit the application.",
    )

    def display_label(self, ctx: AppContext) -> str:  # noqa: ARG002
        """Return the static menu label.

        :param ctx: Application context (unused).
        :type ctx: AppContext
        :return: Menu label for the exit command.
        :rtype: str
        """
        return f"[{self.meta.key}] {self.meta.label}"

    def run(self, ctx: AppContext, io: IO) -> None:  # noqa: ARG002
        """Exit the application with status code 0.

        :param ctx: Application context (unused).
        :type ctx: AppContext
        :param io: IO adapter to print the farewell message.
        :type io: IO
        :raises SystemExit: Always raised with code ``0``.
        """
        io.write("Thank you for using GIC Cinemas system. Bye!")
        raise SystemExit(0)
