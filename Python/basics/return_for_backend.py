from math import factorial,isqrt


#Возвращаемся в бэкэнд
#по задачам

print('\n Пример 1 \n')

def max_of_two(a,b):
    if a > b:
        return a
    else:
        return b

print(max_of_two(int(input("Введите 1 число:")),int(input("Введите 2 число:"))))

print('\n Пример 2 \n')

#Легкий способ

def min_of_list(arr):
    return min(arr)

print(f"Ваше число:{min_of_list([1,3,3,5,1,5,7])}")

#Cпособ тяжелее

def min_of_list_hard(arr):
    for run in range(len(arr) - 1):
        for i in range(len(arr) - run - 1):
            if arr[i] > arr[i + 1]:
                arr[i],arr[i + 1] = arr[i + 1],arr[i]
    return arr[0]

print(f"Ваше число:{min_of_list_hard([4,1882,213,523424,-1])}")

print('\n Пример 3 \n')

#Легкий способ

def sum_of_list(arr):
    return sum(arr)

print(f"Сумма:{sum_of_list([2,5,1,5,23242,4])}")

#Сложнее способ

def sum_of_list_hard(arr):
    total = 0
    for i in range(len(arr)):
        total += arr[i]
    return total

print(f"Сумма:{sum_of_list_hard([2,5,1,5,8,2,1])}")

print('\n Пример 4 \n')

#Легкий способ

def factorial_1(n):
    return factorial(n)

n = int(input("Ваше число:"))
print(f"Результат: {factorial_1(n)}")

#Сложнее способ

def factorial_hard(n):
    total = 1
    for i in range(1,n+1):
        total *= i
    return total

n = int(input("Ваше число:"))
print(f"Результат: {factorial_hard(n)}")

print('\n Пример 5 \n')

def is_prime(n):
    if n < 2:
        return False
    for i in range(2,isqrt(n) + 1):
        if n % i == 0:
            return False
    return True

print(is_prime(17))

print('\n Пример 6 \n')

def reverse_string(s):
    reverse = s[::-1]
    return reverse

s = str(input("Ваша фраза: "))

print(f'Реверс вид:{reverse_string(s)}')

print('\n Пример 7 \n')

#итерактивный 

def fibonacci(n):
    if n < 0:
        raise ValueError('Число должно быть положительным')
    a,b = 0,1
    for _ in range(n):
        a,b = b,a+b
    return a

#рекурсивный

def fibonacci_rec(n):
    if n <= 1:
        return n
    return fibonacci_rec(n-1) + fibonacci_rec(n-2)


print('\n Пример 8 \n')

def unique_elements(arr):
    elements = []
    for element in arr:
        if element not in elements:
            elements.append(element)
    return elements

print(unique_elements([1,4,2,7,2,4,7,8,8]))

print('\n Пример 9 \n')

def filter_even(arr):
    total = []
    for i in range(len(arr)):
        if arr[i] % 2 == 0:
            total.append(arr[i])
    return total

print(filter_even([1,2,3,4,5,6,7,8,9]))

print('\n Пример 10 \n')

def map_square(arr):
    total = []
    for i in range(len(arr)):
        total.append(arr[i]**2)

    return total

print(map_square([1,2,3,4,5,6,7,8,9]))