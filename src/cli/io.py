"""Console I/O implementation."""

class ConsoleIO:
    """Console-backed IO adapter using :func:`input` and :func:`print`."""

    def prompt(self, text: str) -> str:
        """Prompt the user and return a line of input.

        :param text: Prompt text.
        :type text: str
        :return: User input line without trailing newline.
        :rtype: str
        :raises SystemExit: If interrupted via ``Ctrl+C``.
        """
        try:
            return input(text)
        except KeyboardInterrupt:
            print()  # newline for cleanliness
            raise SystemExit(130)

    def write(self, text: str) -> None:
        """Write a line to standard output.

        :param text: Text line to print.
        :type text: str
        """
        print(text)

    def newline(self) -> None:
        """Print a single blank line."""
        print()
