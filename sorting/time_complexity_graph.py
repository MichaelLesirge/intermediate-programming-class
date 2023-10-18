import time

from matplotlib import pyplot as plt

from util import make_random
import algorithms

class Config:
    SORTING_ALGORITHMS = [algorithms.bubble_sort, algorithms.insertion_sort, algorithms.selection_sort, algorithms.merge_sort, algorithms.quick_sort]
    NUM_RANGE = (-100000, 100000)
    
    NUM_OF_TIMES_RUN = 15

def main() -> None:

    lengths = [(2 ** i) for i in range(Config.NUM_OF_TIMES_RUN)]
    arrays = [make_random(length, Config.NUM_RANGE) for length in lengths]
    
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
        plt.plot(lengths, times, label=key.__name__)
    
    plt.title("Times for different sorts") 
    plt.xlabel("Array Length")
    plt.ylabel("Time In Seconds")
    plt.legend()
    plt.show()
    
if __name__ == "__main__":
    main()