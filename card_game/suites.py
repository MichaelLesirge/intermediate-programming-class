from dataclasses import dataclass
from colors import Color
import enum

@dataclass(slots=True, frozen=True)
class SuiteType:
    order: int 
    symbol: str
    color: Color

    def __str__(self) -> str:
        return self.symbol

class Suites(enum.Enum):
    SPADES = SuiteType(0, "♠", Color.BLACK)
    HEARTS = SuiteType(1, "♥", Color.RED)
    DIAMONDS = SuiteType(2, "♦", Color.RED)
    CLUBS = SuiteType(3, "♣", Color.BLACK)