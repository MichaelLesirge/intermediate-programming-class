from dataclasses import dataclass
import enum

@dataclass(slots=True, frozen=True, order=True)
class Rank:
    letter: str
    number: int
    
    is_face: bool
    
    def __str__(self) -> str:
        return self.letter
    
RANKS = [
    Rank("A", 1, False),
    Rank("2", 2, False),
    Rank("3", 3, False),
    Rank("4", 4, False),
    Rank("5", 5, False),
    Rank("6", 6, False),
    Rank("7", 7, False),
    Rank("8", 8, False),
    Rank("9", 9, False),
    Rank("10", 10, False),
    Rank("J", 11, True),
    Rank("Q", 12, True),
    Rank("K", 13, True),
]

ACE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING = RANKS
    