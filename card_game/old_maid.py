import dataclasses
import random

import ranks
import suites
from deck import Card, CardGroup, Deck

@dataclasses.dataclass(frozen=True, slots=True)
class Player:
    name: str
    hand: CardGroup

def plural(group_name: str, num: int) -> int:
    return f"{num} {group_name}{"" if num == 1 else "s"}"

def main():
    deck = Deck()
    
    old_maid = Card(ranks.QUEEN, random.choice(suites.SUITES))
    
    names_input = input("Enter player names, separated by comma: ")
    players = [Player(name.strip().title(), CardGroup()) for name in names_input.split(",")]

    deck.remove(old_maid)
    
    deck.shuffle()

    for i in range(len(deck)):
        current_player = players[i % len(players)]
        card = deck.draw()
        current_player.hand.append(card)

    turn_number = 0
    
    going = True
    
    while going:
        player_num = turn_number % len(players)
        current_player = players[player_num]
        
        print(f"\n{current_player.name}'s turn!\n")
        
        hand = current_player.hand
        
        next_player = players[(turn_number + 1) % len(players)]
        
        card_counter: dict[ranks.Rank, list[Card]] = {}
        for card in hand:
            card_counter[card.rank] = card_counter.get(card.rank, []) + [card]
        
        print(f"{current_player.name} has {plural("card", len(current_player.hand))} at start of turn:")
        print("No cards left!" if hand.is_empty() else hand.to_string(cards_per_row=8))
        
        num_of_duplicates = 0 
        for found_cards in card_counter.values():
            while len(found_cards) > 1:
                num_of_duplicates += 1
                hand.remove(found_cards.pop())
                hand.remove(found_cards.pop())
        
        if num_of_duplicates > 0:
            print(f"{current_player.name} removes {plural("pair", num_of_duplicates)} of duplicates:")
            print("No cards left!" if hand.is_empty() else hand.to_string(cards_per_row=8))
        
        if sum(len(player.hand) for player in players) == 1:
            going = False
        elif not hand.is_empty():
            card = hand.draw(draw_random=True)
            next_player.hand.append(card)
            
            print(f"{current_player.name} gives the {card.to_shorthand()} to {next_player.name}, now has {plural("card", len(current_player.hand))} left:")
            print("No cards left!" if hand.is_empty() else hand.to_string(cards_per_row=8))
            
        turn_number += 1 
    
    for player in players:
        if not player.hand.is_empty():
            print(f"{player.name} is the Old Maid!")       
    
        
if __name__ == "__main__":
    main()