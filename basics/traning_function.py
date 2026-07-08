from math import factorial,sqrt

List = [2,3,5,7,2,4,8]
n = 7


print('\n Пример 1 \n')

def max(List,n):
    for run in range(n - 1):
        for i in range(n - 1 - run):
            if List[i] > List[i + 1]:
                List[i],List[i + 1] = List[i + 1], List[i]
    return List[-1]

print(max(List,n))

print('\n Пример 2 \n')

def min(List,n):
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if List[i] > List[i + 1]:
                List[i],List[i + 1] = List[i + 1],List[i]
    return List[0]

print(min(List,n))

print('\n Пример 3 \n')

def sum(List,n):
    count = 0
    for i in range(n):
        count += List[i]
    return count

print(sum(List,n))

print('\n Пример 4 \n')

def get_welcome():
    welcome_art = '''
         ______________
        /             /|
       /             / |
      /____________ /  |
     | ___________ |   |
     ||           ||   |
     ||           ||   |
     ||           ||   |
     ||___________||   |
     |   _______   |  /
    /|  (_______)  | /
   ( |_____________|/
    \\
.=======================.
| ::::::::::::::::  ::: |
| ::::::::::::::[]  ::: |
|   -----------     ::: |
`-----------------------'
    '''
    return welcome_art

print(get_welcome())

print('\n Пример 5 \n')

def arithmetic_mean(List,n):
    cout = 0
    for i in range(n):
        cout += List[i]
        return f'{cout / len(List):20f}' #Для красоты

print(arithmetic_mean(List,n))

print('\n Пример 6 \n')

def bin_cof(n,k):
    if n > k:
        return f'Вот биноминальный коэффицент: {factorial(n) / (factorial(k) * factorial(n - k))}'
    else:
        return 'No'

n = int(input('Введите коэффицент n: '))
k = int(input('Введите коэффицент k: '))
print(bin_cof(n,k))

print('\n Пример 7 \n')

def discrimenent(a,b,c):
    D = b**2 - 4*a*c
    if D > 0:
        x_1 = ((-1*b) + sqrt(D)) / (2*a)
        x_2 = ((-1*b) - sqrt(D)) / (2*a)
        return f'1 корень: {x_1}\n2 корень: {x_2}'
    elif D == 0:
        x = (-(b) + sqrt(D)) / (2*a)
        return f'Корень:{x}'
    elif D < 0:
        print('Нет корней')

a_1 = int(input('Введите коэффицент a(может быть с -): '))
b_2 = int(input('Введите коэффицент b(может быть с -): '))
c_3 = int(input('Введите коэффицент c(может быть с -): '))

print(discrimenent(a_1,b_2,c_3))

print('\n Пример 8 \n')

def sigma(a,n,i):
    cout = 0
    for j in range(i,n+1):
        cout += a
    return cout

a_2 = int(input('Введите число a:'))
n_1 = int(input('Введите количество:'))
i = int(input('Введите с чего начать:'))

print(sigma(a_2,n_1,i))