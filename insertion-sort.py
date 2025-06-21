import time
from arraySet import arraySet

start_time = time.time()

def insertionSort(itemsToSort: list[int]) -> list[int]:
    selector = 1    
    totalItemCount = len(itemsToSort)
    while selector < totalItemCount:
        
        toCompare = selector - 1
        comparedValue = itemsToSort[toCompare]
        selectedValue = itemsToSort[selector]
        
        if comparedValue > selectedValue:
            itemsToSort[toCompare] = selectedValue
            itemsToSort[selector] = comparedValue

            if selector == 1:
                selector += 1
            
            if selector > 1:
                selector -= 1

        if comparedValue < selectedValue or comparedValue == selectedValue:
            selector += 1        

    return itemsToSort

result = insertionSort(arraySet)
print(result)

end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time: {execution_time:.4f} seconds")
