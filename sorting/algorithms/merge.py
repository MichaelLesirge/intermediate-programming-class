"""
Time Complexity: O(N log(N))
Auxiliary Space: O(1)

split into sub arrays and merge back the arrays in order

Pros:
- worst case is O(N log(N)) performance 
- elements with same key maintain relative order
- easy to make parallel, but at cost of more memory making list copies  

Cons:
- uses recursion, so lots of stack frames
- not the best for small lists
"""

def merge(array: list, left: int, mid: int, right: int) -> None:
    start2 = mid + 1
 
    if array[mid] <= array[start2]:
        return
 
    while left <= mid and start2 <= right:
 
        if array[left] <= array[start2]:
            left += 1
        else:
            value = array[start2]
            index = start2
 
            while index != left:
                array[index] = array[index - 1]
                index -= 1
 
            array[left] = value

            left += 1
            mid += 1
            start2 += 1 

def merge_sort(array: list, left: int = None, right: int = None) -> None:
    if left is None: left = 0
    if right is None: right = len(array) - 1
    
    if left >= right: return
    
    mid = left + (right - left) // 2
    
    merge_sort(array, left, mid)
    merge_sort(array, mid + 1, right)

    merge(array, left, mid, right)