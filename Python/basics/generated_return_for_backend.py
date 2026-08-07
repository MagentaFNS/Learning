print('\n Пример 1 \n')

def squares(n):
    for i in range(1,n+1):
        yield i * i

n = squares(3)
print(next(n))
print(next(n))
print(next(n))

print('\n Пример 2 \n')

def even_numbers(n):
    for i in range(1,n+1):
        if i % 2 == 0:
            yield i

n = even_numbers(10)
print(next(n))
print(next(n))
print(next(n))

print('\n Пример 3 \n')

def fibonacci_gen(n):
    a,b = 0,1
    for _ in range(n):
        yield a
        a,b = b,a + b

n = fibonacci_gen(10)
print(next(n))
print(next(n))
print(next(n))

print('\n Пример 4 \n')

def read_lines(filename):
    with open(filename,'r') as f:
        for line in f:
            yield line.strip()

file_gen = read_lines('basics/cycles.py')
print(next(file_gen))
print(next(file_gen))
print(next(file_gen))
print(next(file_gen))

print('\n Пример 5 \n')

def infinite_counter():
    n = 0
    while True:
        yield n
        n += 1

n = infinite_counter()
print(next(n))
print(next(n))
print(next(n))