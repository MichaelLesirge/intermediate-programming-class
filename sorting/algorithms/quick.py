"""
Time Complexity: average O(N log(N)), worst O(N^2)
Auxiliary Space: O(1)

divide and conquer that picks pivot then partisans array around it
"""

def swap(array: list, a: int, b: int) -> None:
    array[a], array[b] = array[b], array[a]

def partition(array: list, left: int, right: int) -> int:
    pivot = array[right]
 
    slow = left - 1
 
    for i in range(left, right):
        if array[i] <= pivot:
 
            slow += 1
            
            swap(array, slow, i)
            
    slow += 1
    
    swap(array, slow, right)
    return slow
 
 
def quick_sort(array: list, left: int = None, right: int = None):
    if left is None: left = 0
    if right is None: right = len(array) - 1
    
    if left >= right: return
 
    pivot = partition(array, left, right)
 
    quick_sort(array, left, pivot - 1)
    quick_sort(array, pivot + 1, right)