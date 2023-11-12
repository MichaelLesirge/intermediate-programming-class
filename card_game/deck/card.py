from . import ranks
from . import suites
from .colors import make_color, Color, Modifier

import dataclasses
import random
import typing

class Settings:
    CARD_SIZE = 1


@dataclasses.dataclass(frozen=True, slots=True, order=True)
class Card:
    rank: ranks.Rank
    suite: suites.Suite

    sort_index: int = dataclasses.field(init=False, repr=False)

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.rank.number)

    def to_special_unicode(self, hide=False) -> str:
        if hide: return chr(0x1F0A0)
        return chr(0x1F0A0 + self.rank.number + self.suite.order * 0x10)
    
    def to_shorthand(self):
        return make_color(self.rank.letter + self.suite.symbol, self.suite.color, modifiers=[Modifier.BOLD])

    def to_string_lines(self, size: int = Settings.CARD_SIZE, hide=False) -> list[str]:
        space_between = size
        width = size * 4 + 3

        lines = []

        lines.append("┌" + ("─" * width) + "┐")

        if hide:
            color = Color.NONE
            lines.extend(["│" + ("░" * width) + "│"] * (space_between * 2 + 3))
        else:
            color = self.suite.color
            lines.append("│" + format(self.rank.letter, f"<{width}") + "│")
            lines.extend(["│" + (" " * width) + "│"] * space_between),
            lines.append("│" + format(self.suite.symbol, f"^{width}") + "│")
            lines.extend(["│" + (" " * width) + "│"] * space_between),
            lines.append("│" + format(self.rank.letter, f">{width}") + "│")

        lines.append("└" + ("─" * width) + "┘")

        return [make_color(line, color, modifiers=[Modifier.BOLD]) for line in lines]

    def to_string(self, size: int = Settings.CARD_SIZE, hide=False):
        return "\n".join(self.to_string_lines(size, hide))

    def __str__(self) -> str:
        return self.to_string()


class CardGroup(list[Card]):
    def __init__(self, cards: list[Card] = []) -> None:
        super().__init__(cards)

    def shuffle(self) -> None:
        random.shuffle(self)

    def draw(self, draw_random = False) -> Card:
        return self.pop(random.randrange(len(self)) if random else -1)

    def is_empty(self) -> bool:
        return len(self) == 0

    def sort(self, suite_first=False, reverse=False):
        def suite_first_key(card): return card.suite.order * \
            len(ranks.RANKS) + card.rank.number
        def rank_first_key(card): return card.rank.number * \
            len(suites.SUITES) + card.suite.order

        return super().sort(key=(suite_first_key if suite_first else rank_first_key), reverse=reverse)
    
    def take_from(self, other: "CardGroup", num_to_take: int = 1):
        for i in range(num_to_take):
            self.append(other.draw())
        

    @typing.overload
    def __getitem__(self, __s: slice) -> "CardGroup[Card]": pass

    @typing.overload
    def __getitem__(self, __i: typing.SupportsIndex) -> Card: pass

    def __getitem__(self, index):
        output = super().__getitem__(index)
        if isinstance(output, list):
            output = CardGroup(output)
        return output

    def to_string(self, size=Settings.CARD_SIZE, cards_per_row=len(suites.SUITES)) -> str:
        # Join was the worst thing to happen to the readability of my code since goto.
        return "\n".join("\n".join(" ".join(line) for line in zip(*[card.to_string_lines(size=size) for card in self[i:i+cards_per_row]])) for i in range(0, len(self), cards_per_row))

    def __str__(self) -> str:
        return self.to_string()