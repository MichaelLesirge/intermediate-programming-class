from . import CardGroup, Card, ranks, suites

class Deck(CardGroup):
    def __init__(self, num_decks: int = 1) -> None:
        for i in range(num_decks):
            for rank in ranks.ALL:
                for suite in suites.ALL:
                    self.append(Card(rank, suite))

    def deal(self, num_of_hands: int, size_of_hands: int = None, rotate: bool = True) -> list[CardGroup]:
        # if allow_uneven and (num_of_hands * size_of_hands) > len(self) != 0:
        #     raise ValueError("Uneven hands")

        hands = [CardGroup() for i in range(num_of_hands)]
        
        for i in range(num_of_hands * size_of_hands):
            hand_index = (i % num_of_hands) if rotate else (i // size_of_hands)
            current_hand = hands[hand_index]
            current_hand.take_from(self)

        return hands