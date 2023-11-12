"""
Time Complexity: average O(N log(N)), worst O(N^2)
Auxiliary Space: O(1)

divide and conquer that picks pivot then partisans array around it

Pros:
- almost always O(N log(N)) performance 
- good on long lists

Cons:
- worst case O(N^2) if there is a bad pivot
- not the best for small lists

"""

def swap(array: list, i: int, j: int) -> None:
    array[i], array[j] = array[j], array[i]

def partition(array: list, left: int, right: int) -> None:
    # pivot index first, center, last, random, or median-of-three
    pivot = right-1
    pivot_value = array[pivot]
    
    pivot_center = left
    
    for i in range(left, right):
        if array[i] < pivot_value:
            swap(array, i, pivot_center)
            pivot_center += 1
            
    swap(array, pivot, pivot_center)
        
    return pivot_center

def quick_sort(array: list, left: int = None, right: int = None) -> None:
    if left is None: left = 0
    if right is None: right = len(array)
    
    if left >= right - 1: return
    
    pivot = partition(array, left, right)
    quick_sort(array, left, pivot)
    quick_sort(array, pivot+1, right)
