from dataclasses import dataclass
import enum

@dataclass(slots=True, frozen=True, order=True)
class Rank:
    letter: str
    number: int
    
    is_face: bool
    
    def __str__(self) -> str:
        return self.letter

ACE = Rank("A", 1, False)
TWO = Rank("2", 2, False)
THREE = Rank("3", 3, False)
FOUR = Rank("4", 4, False)
FIVE = Rank("5", 5, False)
SIX = Rank("6", 6, False)
SEVEN = Rank("7", 7, False)
EIGHT = Rank("8", 8, False)
NINE = Rank("9", 9, False)
TEN = Rank("10", 10, False)
JACK = Rank("J", 11, True)
QUEEN = Rank("Q", 12, True)
KING = Rank("K", 13, True)
    
RANKS = [ACE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING]