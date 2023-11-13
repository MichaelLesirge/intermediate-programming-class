from dataclasses import dataclass
from .colors import Color
import enum

@dataclass(slots=True, frozen=True)
class Suite:
    order: int 
    symbol: str
    color: Color

    def __str__(self) -> str:
        return self.symbol

ALL = [
    Suite(0, "♠", Color.BLACK),
    Suite(1, "♥", Color.RED),
    Suite(2, "♦", Color.RED),
    Suite(3, "♣", Color.BLACK),
]

SPADES, HEARTS, DIAMONDS, CLUBS = ALL