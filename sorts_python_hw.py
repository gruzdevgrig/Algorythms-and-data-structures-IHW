'''------------------------------------------------Сортировка подсчетом-----------------------------------------------------------'''
def counting_sort(arr: list) -> None:
    max_val = max(arr) 
    min_val = min(arr) 
    count_list = [0] * (max_val - min_val +1)
    for num in arr:
        count_list[num - min_val] += 1
    arr.clear()
    for i in range(min_val, max_val + 1):
        index = i - min_val
        for j in range(count_list[index]):
            arr.append(i)
        
'''------------------------------------------------------ Сортировка вставкой -----------------------------------------'''
def ins_sort(arr: list) -> None:
    for i in range(1, len(arr)):
        base_el = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > base_el:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = base_el
    return arr

'''------------------------------------------------------ Сортировка пузырьком -----------------------------------------------'''
def bubble_sort(arr: list) -> None:
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr 
