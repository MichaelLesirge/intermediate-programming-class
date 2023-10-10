"""
Time Complexity: O(N^2)
Auxiliary Space: O(1)

Advantages:
- simple
- no extra memory
- elements with same key maintain order

Disadvantages:
- O(N^2) so slow for long lists
"""

def swap(l: list, a: int, b: int):
    l[a], l[b] = l[b], l[a]

def bubble_sort(array: list):
    n = len(array)
    
    for i in range(n):
        done = True
        
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                swap(array, j, j + 1)
                done = False
        
        if done: break