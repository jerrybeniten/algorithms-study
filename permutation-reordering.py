def sort(numbers: list[int], orderBy: str = 'ASC') -> None:

    INSTANCE_TO_AVOID = 1
    INITIAL_ZERO = 0
    arrayCount = len(numbers)
    sortedResult = [0] * arrayCount

    for iteratedNumber in numbers:
        rank = 0
        identicalInstance = 0                
        
        for compareNumber in numbers:

            if iteratedNumber == compareNumber:
                identicalInstance += 1
            
            if orderBy == 'ASC':
                if iteratedNumber > compareNumber or (iteratedNumber == compareNumber and identicalInstance > INSTANCE_TO_AVOID) :
                    rank += 1

            if orderBy == 'DESC':
                if iteratedNumber < compareNumber or (iteratedNumber == compareNumber and identicalInstance > INSTANCE_TO_AVOID) :
                    rank += 1
                                  
        while sortedResult[rank] is not None and sortedResult[rank] != INITIAL_ZERO:
            rank -= 1
        
        sortedResult[rank] = iteratedNumber                
            
        rank = 0
    return sortedResult

result = sort([200,200,31,41,200,59,26,41,58,15,200,15], 'DESC')
print(result)
