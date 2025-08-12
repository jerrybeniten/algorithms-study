import time
from arrayMediumSet import arrayMediumSet

start_time = time.time()

def pySort(itemsToSort: list[int]) -> list[int]:    
    return sorted(itemsToSort)

result = pySort(arrayMediumSet)
print('Sort: Sort')
print('Output: \t', result)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.4f} seconds")