"""
Time Complexity: O(N log(N))
Auxiliary Space: O(N)

split into sub arrays and merge back the arrays in order

Pros:
- worst case is O(N log(N)) performance 
- elements with same key maintain relative order
- easy to make parallel

Cons:
- not the best for small lists
- uses extra memory for another array
"""

def merge(array: list, left: int, mid: int, right: int) -> None:
    start1, end1 = left, mid
    start2, end2 = mid + 1, right
    
    sorted_section = []
        
    while start1 <= end1 and start2 <= end2:
        if array[start1] < array[start2]:
            sorted_section.append(array[start1])
            start1 += 1
        else:   
            sorted_section.append(array[start2])
            start2 += 1

    while start1 <= end1:
        sorted_section.append(array[start1])
        start1 += 1

    while start2 <= end2:
        sorted_section.append(array[start2])
        start2 += 1
    
    array[left : right + 1] = sorted_section
        

def merge_sort(array: list, left: int = None, right: int = None) -> None:
    if left is None: left = 0
    if right is None: right = len(array) - 1
    
    if left >= right: return
    
    mid = left + (right - left) // 2
        
    merge_sort(array, left, mid)
    merge_sort(array, mid + 1, right)

    merge(array, left, mid, right) 