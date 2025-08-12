import time
from arrayMediumSet import arrayMediumSet

start_time = time.time()

def bubbleSort(itemsToSort: list[int]) -> list[int]:

    continueScanning = True
    swapCount = 0
    totalItemCount = len(itemsToSort)

    while continueScanning:
        swapCount = 0
        for index, iteratedNumber in enumerate(itemsToSort):
            selector = index
            toCompareWith = index+1
            
            # Bound within the array total length            
            if (toCompareWith <= totalItemCount - 1 and itemsToSort[selector] > itemsToSort[toCompareWith]):                
                swapCount = swapCount + 1
                print(itemsToSort)                
                forSwap = itemsToSort[selector]
                itemsToSort[selector] = itemsToSort[toCompareWith]
                itemsToSort[toCompareWith] = forSwap
        
    
        if swapCount == 0:
            continueScanning = False
                    
    return itemsToSort

result = bubbleSort(arrayMediumSet)
print('Sort: BUBBLE')
print('Output: \t', result)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.4f} seconds")
