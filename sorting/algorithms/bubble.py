"""
Time Complexity: O(N^2)
Auxiliary Space: O(1)

Bubbles value up by swapping them so the higher is on the left side

Pros:
- simple
- no extra memory
- elements with same key maintain relative order

Cons:
- O(N^2) so slow for long lists
"""

def swap(array: list, a: int, b: int) -> None:
    array[a], array[b] = array[b], array[a]

def bubble_sort(array: list):
    n = len(array)
    
    for i in range(n):
        done = True
        
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                swap(array, j, j + 1)
                done = False
        
        if done: break