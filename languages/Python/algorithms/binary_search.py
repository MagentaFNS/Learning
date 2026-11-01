# бинарный поиск - лучший способ работы с списками,оличие его от линейного,тем что он быстрее намного.

def binary_search(list,item):
    L = 0                   #лево
    R = len(list) - 1       #право

    while L<=R:
        Centre = (L + R) // 2 # по середине 

        if list[Centre] == item:
            return Centre
        if list[Centre] < item:
            L = Centre + 1
        else:
            R = Centre - 1

    return None

