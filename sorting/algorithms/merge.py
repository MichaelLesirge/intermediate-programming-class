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
    start2, end2 = mid, right

    merged_area = []
    while start1 < end1 and start2 < end2:
        if array[start1] < array[start2]:
            merged_area.append(array[start1])
            start1 += 1
        else:
            merged_area.append(array[start2])
            start2 += 1

    if start1 < end1: merged_area.extend(array[start1:end1])
    if start2 < end2: merged_area.extend(array[start2:end2])

    array[left:right] = merged_area


def merge_sort(array: list, left: int = None, right: int = None) -> None:
    if left is None: left = 0
    if right is None: right = len(array)

    if left >= right - 1: return

    mid = left + (right - left) // 2

    merge_sort(array, left, mid)
    merge_sort(array, mid, right)

    merge(array, left, mid, right)
