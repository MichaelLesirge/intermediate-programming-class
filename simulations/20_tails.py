import random

def run_simulation() -> str:
    return ['tails', 'heads'][random.randrange(2)]

    
def main() -> None:
    sim_times = 1_000_000
    win_count = 0
    
    get_to = 20
    winning_result = "tails"
    
    current_count = 0
    
    for i in range(sim_times):
        
        if run_simulation() == winning_result:
            current_count += 1
        else:
            current_count = 0
        
        if current_count >= get_to:
            current_count = 0
            win_count += 1
        
        # did_win_toss = run_simulation() == winning_result
        # current_count += did_win_toss
        # current_count *= did_win_toss 
        
        # did_win_game = current_count == get_to
        # current_count *= not did_win_game
        # win_count += did_win_game
        
        
    max_wins = sim_times // get_to
    print(f"Got {get_to} in a row {win_count} times with {sim_times} flips.")
    print(f"The maximum you could get to is {max_wins}, so you got {win_count/max_wins:%} of all opportunities")
    

if __name__ == "__main__":
    main()