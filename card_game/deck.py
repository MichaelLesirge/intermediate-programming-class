import rank, suite
import color

import random

class Card:   
    def __init__(self, rank: rank.Rank, suite: suite.Suite) -> None:
        self.rank = rank
        self.suite = suite    
    
    def get_lines(self, hidden = False) -> list[str]:   
        if hidden:
            return ["┌─────────┐"] + (["│░░░░░░░░░│"] * 7) + ["└─────────┘"]
        lines = [
            "┌─────────┐",
            "│%s        │" % self.rank,
            "│         │",
            "│         │",
            "│    %s    │" % self.suite,
            "│         │",
            "│         │",
            "│        %s│" % self.rank,
            "└─────────┘",
        ]
        return [color.make_color(line, self.suite.color) for line in lines]
    
    @staticmethod
    def display_cards(cards: list["Card"]) -> None:
        lines = []
        for line in zip(*[card.get_lines() for card in cards]):
            lines.append(" ".join(line))
                
        return "\n".join(lines)
    
    def __str__(self) -> str:
        return color.make_color(f"{self.suite}{self.rank}", self.suite.color)

class Deck:
    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> None:
        self.deck = []
    
    def shuffle(self) -> None:
        random.shuffle(self.deck)
    
card1 = Card(rank.ACE, suite.Clubs)
card2 = Card(rank.KING, suite.Hearts)
card3 = Card(rank.THREE, suite.Hearts)
print(Card.display_cards([card1, card2, card3]))
