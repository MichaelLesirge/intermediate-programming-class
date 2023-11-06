from ranks import Ranks
from suites import Suites
from colors import make_color, Color, Modifier

import random
import typing

class Settings:
    CARD_SIZE = 1

class Card:   
    def __init__(self, rank: Ranks, suite: Suites) -> None:
        self.rank = rank.value
        self.suite = suite.value
                
        self.hidden = False
    
    def hide(self) -> None:
        self.hidden = True
        
    def unhide(self) -> None:
        self.hidden = False
    
    def get_special_character(self, override_hide = None) -> str:
        if override_hide is None: override_hide = self.hidden
        
        return chr(0x1F0A0 + self.rank.number + self.suite.order * 0x10)
        
    def get_lines(self, size: int = Settings.CARD_SIZE, override_hide = None) -> list[str]:   
        if override_hide is None: override_hide = self.hidden
        
        space_between = size
        width = size * 4 + 3
                
        lines = []
        
        lines.append("┌" + ("─" * width) + "┐")
        
        if override_hide:
            color = Color.NONE
            lines.extend(["│" + ("░" * width) + "│"] * (space_between * 2 + 3))
        else:
            color = self.suite.color
            lines.append("│" + format(self.rank.letter, f"<{width}") + "│")
            lines.extend(["│" + (" " * width)  + "│"] * space_between),
            lines.append("│" + format(self.suite.symbol, f"^{width}") + "│")
            lines.extend(["│" + (" " * width) + "│"] * space_between),
            lines.append("│" + format(self.rank.letter, f">{width}") + "│")
            
        lines.append("└" + ("─" * width) + "┘")
        
        return [make_color(line, color, modifiers=[Modifier.BOLD]) for line in lines]
    
    def __str__(self) -> str:
        return "\n".join(self.get_lines())

class CardGroup(list[Card]):
    def __init__(self, cards: list[Card]) -> None:
        super().__init__(cards)
    
    def shuffle(self) -> None:
        random.shuffle(self.cards)
        
    def sort(self, suite_first = False,  reverse = False):
        if suite_first: key = lambda card: card.suite.order * len(Ranks) + card.rank.number
        else: key = lambda card: card.rank.number * len(Suites) + card.suite.order
        
        return super().sort(key=key, reverse=reverse)
    
    @typing.overload
    def __getitem__(self, __s: slice) -> "CardGroup[Card]": pass
     
    @typing.overload
    def __getitem__(self, __i: typing.SupportsIndex) -> Card: pass
    
    def __getitem__(self, index):
        output = super().__getitem__(index)
        if isinstance(output, list): output = CardGroup(output)
        return output
                
    def _get_cards(self, size=Settings.CARD_SIZE, cards_per_row = len(Suites)) -> str:
        # Join was the worst thing to happen to the readability of my code since goto.        
        return "\n".join("\n".join(" ".join(line) for line in zip(*[card.get_lines(size=size) for card in self[i:i+cards_per_row]])) for i in range(0, len(self), cards_per_row))
    
    def __str__(self) -> str:
        return self._get_cards()

class Deck(CardGroup):
    def __init__(self) -> None:
        for rank in Ranks:
            for suite in Suites:
                self.append(Card(rank, suite))