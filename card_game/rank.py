from dataclasses import dataclass

@dataclass
class Rank:
    name: str
    value: int
    
    is_face: bool
    letter: str = ""
    
    def __post_init__(self):
        self.letter = self.name[0].upper() if self.name.isalpha() else str(self.value)

    def __str__(self) -> str:
        return self.letter

ACE = Rank("ace", 1, True)
TWO = Rank("two", 2, False)
THREE = Rank("three", 3, False)
FOUR = Rank("four", 4, False)
FIVE = Rank("five", 5, False)
SIX = Rank("six", 6, False)
SEVEN = Rank("seven", 7, False)
EIGHT = Rank("eight", 8, False)
NINE = Rank("nine", 9, False)
JACK = Rank("jack", 10, True)
QUEEN = Rank("queen", 11, True)
KING = Rank("king", 12, True)