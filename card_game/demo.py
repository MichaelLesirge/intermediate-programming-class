from deck import Card, CardGroup, Deck, ranks, suites

card = Card(ranks.ACE, suites.CLUBS)
print(f"Print different sizes of {card.to_shorthand()}")

for i in range(4):
    print(card.to_string(size = i))

deck = Deck()

deck.shuffle()

hands = deck.deal(num_of_hands=3, size_of_hands=7, rotate=False)

CardGroup.CARD_SIZE = 1
CardGroup.CARDS_PER_ROW = 7

for i, hand in enumerate(hands):
    hand.sort()
    
    print(f"Hand #{i+1}")  
    print(hand)
    print()

