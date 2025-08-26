import pytest

from src.models.entities import Theater
from src.models.context import AppContext
from src.core.renderers.ascii_renderer import AsciiRenderer
from src.core.services.booking import BookingService


@pytest.fixture()
def theater_4x6() -> Theater:
    """A small theater with 4 rows and 6 columns."""
    return Theater(title="Inception", rows=4, cols=6)


class ScriptIO:
    """Tiny scripted IO for command tests."""

    def __init__(self, inputs: list[str]) -> None:
        self._inputs = list(inputs)
        self.outputs: list[str] = []

    def prompt(self, text: str) -> str:
        self.outputs.append(text)
        return self._inputs.pop(0) if self._inputs else ""

    def write(self, text: str) -> None:
        self.outputs.append(text)

    def newline(self) -> None:
        self.outputs.append("\n")


@pytest.fixture
def theater_3x5() -> Theater:
    return Theater(title="Demo", rows=3, cols=5)


@pytest.fixture
def ctx_empty(theater_3x5: Theater) -> AppContext:
    return AppContext(theater=theater_3x5)


@pytest.fixture
def renderer() -> AsciiRenderer:
    return AsciiRenderer()


@pytest.fixture
def service() -> BookingService:
    return BookingService()


@pytest.fixture
def script_io_factory():
    def _make(inputs: list[str]) -> ScriptIO:
        return ScriptIO(inputs)

    return _make
