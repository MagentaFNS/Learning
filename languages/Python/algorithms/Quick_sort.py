#Самый быстрый метод сортировки,очень нужен

import random

def Quick_sort(s):
    if len(s) <= 1:
        return s

    elem = random.choice(s)

    left = list(filter(lambda x:x < elem, s))
    center = [i for i in s if i==elem]
    right = list(filter(lambda x: x > elem, s))


    return Quick_sort(left) + center + Quick_sort(right)


#многие не понимают зачем elem = random.choice(s)
# все потому что если брать 1 элемент,то это будет плохо для скорости 
# лямбда работает по типу добовления в список.