#Рекурсия - это когда функция вызывает саму себя.
#у рекурсии есть лимит 1000 - это пайтон,так она работает бесконечно.
#Лимит можно увеличить таким способом 
#import sys
#sys.setrecursionlimit(10000) лимит 10000

#стандартный вариант рекурсии - это факториал

print('\n Пример 1 \n')

def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)

print(f"Ответ: {factorial(5)}")

print('\n Пример 2 \n')

#Рекурсия медленнее циклов,лучше использовать циклы,чем рекурсию
#Рекурсия может испоьзоваться и для перебора всех папок и файлов системы 
import os

def scan_folder(path):
    for item in os.listdir(path):
        full_path = os.path.join(path,item)
        if os.path.isdir(full_path):
            scan_folder(full_path) #рекурсия
        else:
            print(f"Файл: {full_path}")

scan_folder("/home/magenta/Avatar") #моя папка с аватарками(можешь заменить на свою)