from dataclasses import dataclass
from color import Color

@dataclass
class Suite:
    symbol: str
    color: Color

    def __str__(self) -> str:
        return self.symbol

Diamonds = Suite("♦", Color.RED)
Clubs = Suite("♣", Color.BLACK)
Hearts = Suite("♥", Color.RED)
Spades = Suite("♠", Color.BLACK)