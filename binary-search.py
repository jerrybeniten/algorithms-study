import time
from arraySmallSet import arraySmallSet

start_time = time.time()

def binarySearch(itemsToSort: list[int], val: int, start: int, end: int) -> int:

    while start <= end:
        mid = (start + end) // 2
        if itemsToSort[mid] < val:
            start = mid + 1
        else:
            end = mid - 1
    return start    

result = binarySearch(arraySmallSet, 9, 0, 6)
print('Binary Search')
print('Output: \t', result)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.4f} seconds")