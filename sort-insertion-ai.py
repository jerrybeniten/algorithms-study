import time
from arraySmallSet import arraySmallSet

start_time = time.time()

def insertionSort(itemsToSort: list[int]) -> list[int]:
    totalItemCount = len(itemsToSort)

    for selector in range(1, totalItemCount):
        selectedValue = itemsToSort[selector]
        position = selector

        # Shift larger values to the right
        while position > 0 and itemsToSort[position - 1] > selectedValue:
            itemsToSort[position] = itemsToSort[position - 1]
            position -= 1
        
        itemsToSort[position] = selectedValue
        print(selector, itemsToSort)

    return itemsToSort

result = insertionSort(arraySmallSet)
print('Sort: INSERTION AI')
print('Output: \t', result)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.4f} seconds")
