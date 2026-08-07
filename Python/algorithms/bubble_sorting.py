#Используется для сортировки по возрастанию.
def bubble_sorting(List,n):
    swapped = False
    for run in range(n - 1):
        for i in range(n - 1 - run):
            if List[i] > List[i + 1]:
                List[i],List[i + 1] = List[i + 1], List[i]
                swapped = True
        if not swapped:
            break
    return List

# N - число чисел в списке.
# и сам лист>)