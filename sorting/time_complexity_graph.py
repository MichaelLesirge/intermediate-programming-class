import time

from matplotlib import pyplot as plt

from util import make_random
import algorithms

class Config:
    SORTING_ALGORITHMS = [algorithms.bubble_sort, algorithms.insertion_sort, algorithms.selection_sort, algorithms.merge_sort, algorithms.quick_sort]
    NUM_RANGE = (-100000, 100000)
    
    START_LENGTH = 100
    NUM_OF_TIMES_RUN = 7

def main() -> None:
    
    length = Config.START_LENGTH
    
    times = {algorithm: [] for algorithm in Config.SORTING_ALGORITHMS}
    
    for i in range(Config.NUM_OF_TIMES_RUN):        
        array = make_random(length, Config.NUM_RANGE)
        
        print(f"#{i}: Sorting array of length {length}")
        
        for algorithm in Config.SORTING_ALGORITHMS:
            array_copy = array.copy()
            
            start_time = time.perf_counter()
            algorithm(array_copy)
            end_time = time.perf_counter()

            total_time = end_time - start_time
            
            times[algorithm].append(total_time)
            
            print(f"{algorithm.__name__} took {total_time} seconds")
        
        print()
        
        length *= 2
    
    for key, times in times.items():
        plt.plot(range(len(times)), times, label=key.__name__)
    
    plt.legend()
    plt.show()
    
if __name__ == "__main__":
    main()