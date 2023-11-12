import time

from matplotlib import pyplot as plt

from util import make_random
import algorithms

class Config:
    SORTING_ALGORITHMS = algorithms.__all__ 
    # SORTING_ALGORITHMS = [algorithms.bubble_sort, algorithms.insertion_sort, algorithms.selection_sort, algorithms.merge_sort, algorithms.quick_sort]
    NUM_RANGE = (-100000, 100000)
    
    LENGTHS = [int(1.5 ** i) for i in range(18)]
    # LENGTHS = [(2 ** i) for i in range(13)]
    # LENGTHS = list(range(0, 10)) + list(range(10, 1000, 10))
    
def main() -> None:

    arrays = [make_random(length, Config.NUM_RANGE) for length in Config.LENGTHS]
    
    times = {algorithm: [] for algorithm in Config.SORTING_ALGORITHMS}
    
    for i, array in enumerate(arrays):
                
        print(f"#{i + 1}: Sorting array of length {len(array)}")
        
        for algorithm in Config.SORTING_ALGORITHMS:
            array_copy = array.copy()
            
            start_time = time.perf_counter()
            algorithm(array_copy)
            end_time = time.perf_counter()

            total_time = end_time - start_time
            
            times[algorithm].append(total_time)
            
            print(f"{algorithm.__name__} took {total_time} seconds")
        
        print()
            
    for key, times in times.items():
        plt.plot(Config.LENGTHS, times, label=key.__name__)
    
    plt.title("Times for different sorts") 
    plt.xlabel("Array Length")
    plt.ylabel("Time In Seconds")
    plt.legend()
    plt.show()
    
if __name__ == "__main__":
    main()