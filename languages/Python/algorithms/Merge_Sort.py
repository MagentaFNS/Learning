def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    left_sort = merge_sort(left)
    right_sort = merge_sort(right)

    return merge(left_sort,right_sort)

def merge(left, right):
    result = []
    i=j=0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
        
    result.extend(left[i:])
    result.extend(right[j:])
    return result
    

arr = [38, 27, 43, 3, 9, 82, 10]
sorted_arr = merge_sort(arr)
print(f"Исходный: {arr}")
print(f"Отсортированный: {sorted_arr}")