import time
from arraySmallSet import arraySmallSet

start_time = time.time()

def insertionSort(itemsToSort: list[int]) -> list[int]:

    INCREMENTOR_DECRIMENTOR = 1
    selector = 1    
    totalItemCount = len(itemsToSort)
    while selector < totalItemCount:
        
        toCompare = selector - INCREMENTOR_DECRIMENTOR
        comparedValue = itemsToSort[toCompare]
        selectedValue = itemsToSort[selector]
        
        if comparedValue > selectedValue:
            itemsToSort[toCompare] = selectedValue
            itemsToSort[selector] = comparedValue

            if selector == 1:
                selector += INCREMENTOR_DECRIMENTOR
            
            if selector > 1:
                selector -= INCREMENTOR_DECRIMENTOR

        if comparedValue < selectedValue or comparedValue == selectedValue:
            selector += INCREMENTOR_DECRIMENTOR

        print(selector, itemsToSort)  

    return itemsToSort

result = insertionSort(arraySmallSet)
print('Sort: INSERTION')
print('Output: \t', result)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.4f} seconds")