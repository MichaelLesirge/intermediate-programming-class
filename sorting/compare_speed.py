import time

import algorithms
from util import make_random

class Config:
    SORTING_ALGORITHMS: list["function"] = [algorithms.quick_sort, algorithms.merge_sort]
    NUM_RANGE = (-1000, 1000)
    
    LENGTHS = [2, 5, 10, 100, 1000, 10000]
    
    NUM_TESTS = 100
    

def main() -> None:

    arrays = [make_random(length, Config.NUM_RANGE) for length in Config.LENGTHS]
        
    for i, array in enumerate(arrays):
        
        algorithm_times: dict["function", int] = {}
                        
        for algorithm in Config.SORTING_ALGORITHMS:
            
            times = []
            
            for _ in range(Config.NUM_TESTS):
                array_copy = array.copy()
                
                start_time = time.perf_counter()
                algorithm(array_copy)
                end_time = time.perf_counter()

                total_time = end_time - start_time
                
                times.append(total_time)
            
            average_time = sum(times) / len(times)
            algorithm_times[algorithm] = average_time
            
            # print(f"Average time for {algorithm.__name__} is {average_time}")
            # print(f"The fasted time was {min(times)} while the max was {max(times)}.")
            
            # variance = (sum(time - average_time for time in times) ** 2) / len(times)
            # standard_deviation = variance ** 0.5
            # if standard_deviation > 0.000001:
            #     print(f"The standard deviation is {standard_deviation:%}")
            
            # print()
            
        
        print(f"#{i + 1}: Sorting array of length {len(array)}")
        
        print()
        
        for algorithm, base_time in algorithm_times.items():
            print(f"{algorithm.__name__} took an average of {base_time} seconds")
            for compare_algorithm, compare_time in algorithm_times.items():
                if algorithm is compare_algorithm: continue
                
                difference = compare_time - base_time
                percentage_difference = difference / base_time
                
                print(f"{algorithm.__name__} is {abs(percentage_difference):%} {["worse", "better"][percentage_difference > 0]} that {compare_algorithm.__name__}")
            print()
        
        print()
        
        
                                  
if __name__ == "__main__":
    main()