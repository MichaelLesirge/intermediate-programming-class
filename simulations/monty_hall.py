import random

def run_simulation(switch = True, doors: list = [0, 0, 1]) -> bool:
    n_doors = len(doors)
    
    random.shuffle(doors)
    
    guess = random.randrange(n_doors)
    
    if switch:
        door_indexes = set(range(n_doors))
        open_door_with_goat = (door_indexes - {guess, doors.index(1)}).pop()
        guess = (door_indexes - {guess, open_door_with_goat}).pop()
            
    return doors[guess]
    
    
    
def main() -> None:
    sim_times = 100_000
    win_count = 0
    
    doors = [0, 0, 1]
    
    for i in range(sim_times):
        should_switch = random.randrange(2)
        win_count += run_simulation(should_switch, doors=doors)
        
    print(f"Won {win_count} out of {sim_times}. {win_count/sim_times:.1%}")

if __name__ == "__main__":
    main()