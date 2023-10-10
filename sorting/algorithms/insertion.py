"""
Time Complexity: O(N^2) 
Auxiliary Space: O(1)

Move all higher values than key up one

Pros:
- simple
- no extra memory
- pretty efficient when the list is small
- best case is O(N)

Cons:
- O(N^2) so slow for long lists
"""

def insertion_sort(array: list) -> None:
    for i in range(1, len(array)):
 
        key = array[i]
 
        j = i - 1
        
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j -= 1
                
        array[j + 1] = key