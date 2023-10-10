from .util import swap, Marker

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

def bubble_sort(l: list, yield_state: bool = False):
    n = len(l)
    
    for i in range(n):
        done = True
                
        for j in range(n - i - 1):
            if l[j] > l[j + 1]:
                swap(l, j, j + 1)
                                
                done = False
        
        if done: break