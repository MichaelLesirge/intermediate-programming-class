"""
Time Complexity: O(N log(N))
Auxiliary Space: O(N)

split into sub arrays and merge back the arrays in order

Pros:
- worst case is O(N log(N)) performance 
- elements with same key maintain relative order
- easy to make parallel, but at cost of more memory making list copies  

Cons:
- not the best for small lists
- use extra arrays
"""

def merge(array: list, left_array: list, right_array: list) -> None:
    left_count = right_count = total_count = 0
    
    while left_count < len(left_array) and right_count < len(right_array):
        if left_array[left_count] <= right_array[right_count]:
            array[total_count] = left_array[left_count]
            left_count += 1
        else:
            array[total_count] = right_array[right_count]
            right_count += 1
        total_count += 1

    while left_count < len(left_array):
        array[total_count] = left_array[left_count]
        left_count += 1
        total_count += 1

    while right_count < len(right_array):
        array[total_count] = right_array[right_count]
        right_count += 1
        total_count += 1
        

def merge_sort(array: list) -> None:
    if len(array) < 2: return
 
    mid = len(array) // 2

    left_array = array[:mid]

    right_array = array[mid:]

    merge_sort(left_array)

    merge_sort(right_array)

    merge(array, left_array, right_array)

"""Merge no copy is much slower, but it does not use any more memory, and more importantly it looks much nicer in the animation"""    

def merge_no_copy(array: list, left: int, mid: int, right: int) -> None:
    left2 = mid + 1
 
    if array[mid] <= array[left2]:
        return
 
    while left <= mid and left2 <= right:
 
        if array[left] <= array[left2]:
            left += 1
        else:
            value = array[left2]
            index = left2
 
            while index != left:
                array[index] = array[index - 1]
                index -= 1
 
            array[left] = value

            left += 1
            mid += 1
            left2 += 1
            
def merge_sort_no_copy(array: list, left: int = None, right: int = None) -> None:
    if left is None: left = 0
    if right is None: right = len(array) - 1
    
    if left >= right: return
    
    mid = left + (right - left) // 2
    
    merge_sort_no_copy(array, left, mid)
    merge_sort_no_copy(array, mid + 1, right)

    merge_no_copy(array, left, mid, right) 
 