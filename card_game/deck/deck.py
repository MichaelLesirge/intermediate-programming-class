from . import CardGroup, Card, ranks, suites

class Deck(CardGroup):
    def __init__(self, num_decks: int = 1) -> None:
        for i in range(num_decks):
            for rank in ranks.RANKS:
                for suite in suites.SUITES:
                    self.append(Card(rank, suite))

