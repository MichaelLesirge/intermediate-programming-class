from dataclasses import dataclass
import enum

@dataclass(slots=True, frozen=True, order=True)

class RankType:
    letter: str
    number: int
    
    is_face: bool
    
    def __str__(self) -> str:
        return self.letter

class Ranks(enum.Enum):
    ACE = RankType("A", 1, True)
    TWO = RankType("2", 2, False)
    THREE = RankType("3", 3, False)
    FOUR = RankType("4", 4, False)
    FIVE = RankType("5", 5, False)
    SIX = RankType("6", 6, False)
    SEVEN = RankType("7", 7, False)
    EIGHT = RankType("8", 8, False)
    NINE = RankType("9", 9, False)
    TEN = RankType("10", 10, False)
    JACK = RankType("J", 11, True)
    QUEEN = RankType("Q", 12, True)
    KING = RankType("K", 13, True)
    