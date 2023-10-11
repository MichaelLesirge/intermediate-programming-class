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

def swap(array: list, a: int, b: int) -> None:
    array[a], array[b] = array[b], array[a]

def partition(array: list, left: int, right: int) -> int:
    pivot = array[right]
 
    i = left - 1
 
    for j in range(left, right):
        if array[j] <= pivot:
 
            i += 1
            
            swap(array, i, j)
 
    swap(array, i + 1, right)
 
    return i + 1
 
 
def quick_sort(array: list, left: int = None, right: int = None):
    if left is None: left = 0
    if right is None: right = len(array) - 1
    
    if left >= right: return
 
    partition_index = partition(array, left, right)
 
    quick_sort(array, left, partition_index - 1)
    quick_sort(array, partition_index + 1, right)