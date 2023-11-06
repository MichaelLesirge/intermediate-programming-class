import random
from deck import Deck, CardGroup, Card
import ranks, suites

def deal_initial_cards(deck: CardGroup) -> tuple[CardGroup, CardGroup]:
    player_hand = CardGroup([deck.draw(), deck.draw()])
    dealer_hand = CardGroup([deck.draw(), deck.draw()])
    return player_hand, dealer_hand

def place_bet(balance: int):
    while True:
        try:
            bet = int(input(f"Your balance: {balance}. Place your bet: ").strip())
            if bet <= balance:
                return bet
            else:
                print("Insufficient balance. Please enter a valid bet.")
        except ValueError:
            print("Invalid input. Please enter a valid bet amount.")

def get_hand_total(hand: CardGroup):
    total = sum(10 if card.rank.is_face else card.rank.number for card in hand)
    num_aces = sum(card.rank == ranks.ACE for card in hand)

    while total > 21 and num_aces:
        total -= 10 + ranks.ACE.number
        num_aces -= 1

    return total

def player_turn(player_hand: CardGroup, deck):
    while True:
        print("\nYour hand:")
        print(player_hand.to_string())
        print("Total:", get_hand_total(player_hand))

        choice = input("Do you want to hit or stand: ").lower().strip()
        if choice in {"h", "hit"}:
            player_hand.append(deck.draw())
            if get_hand_total(player_hand) > 21:
                print("Bust! You lose.")
                return False
        elif choice in {"s", "stand"}:
            return True
        else:
            print("Invalid choice. Please enter hit or stand.")

def dealer_turn(dealer_hand, deck):
    while get_hand_total(dealer_hand) < 17:
        dealer_hand.append(deck.draw())

def play_round(balance):
    twenty_one = 21
    
    print("New round!")

    deck = Deck()
    deck.shuffle()
    player_hand, dealer_hand = deal_initial_cards(deck)

    bet_amount = place_bet(balance)

    player_turn_complete = player_turn(player_hand, deck)
    if player_turn_complete:
        dealer_turn(dealer_hand, deck)

    player_total = get_hand_total(player_hand)
    dealer_total = get_hand_total(dealer_hand)

    if player_total > twenty_one:
        print(f"Player total of {player_total} greater than {twenty_one}, you lose.")
        return -bet_amount
    elif dealer_total > twenty_one:
        print(f"Dealer total of {dealer_total} greater than {twenty_one}, you lose.")
        return bet_amount
    
    if player_total > dealer_total:
        print(f"Player total of {player_total} greater dealer total of {dealer_total}, you win.")
        return bet_amount
    elif dealer_total > player_total:
        print(f"Dealer total of {dealer_total} greater player total of {player_total}, you lose.")
        return -bet_amount
    
    print("Push. It's a tie.")
    return 0

def main():
    balance = 1000

    going = True
    
    while going:
        
        print()
        
        balance += play_round(balance)
        
        print()
        
        if balance <= 0:
            print("Game Over, out of money!")
            going = False
        else:
            going = input("Do you want to play another round? (y/n): ").lower().strip() in {"y", "yes", ""}
     
    print()   
     
    print("Thanks for playing!")

if __name__ == "__main__":
    main()