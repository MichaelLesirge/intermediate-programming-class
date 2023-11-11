"""
Time Complexity: O(N^2) 
Auxiliary Space: O(1)

Selects lowest value each iteration and moves it to start

Pros:
- simple
- no extra memory
- best case is O(N)

Cons:
- O(N^2) so slow for long lists
"""

def swap(array: list, a: int, b: int) -> None:
    array[a], array[b] = array[b], array[a]

def selection_sort(array: list) -> None:
    n = len(array)
    
    for i in range(n-1):
        
        min_index = min(range(i, n), key = array.__getitem__)     
        
        swap(array, min_index, i)

def selection_sort_one_line(array): [swap(array, min(range(i, len(array)), key = array.__getitem__), i) for i in range(len(array))]