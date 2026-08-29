import secrets
import string
import time
import random 
import os

#Можно генерировать ключи 
# Только буквы и цифры (без спецсимволов)
alphabet = string.ascii_letters + string.digits
safe_key = ''.join(secrets.choice(alphabet) for _ in range(64))
print(safe_key)

#Hello world
def HelloWorld(name):
    if name == "print":
        print("Hello World!")

HelloWorld("print")

def textwr(text,delay=0.05):
    for char in text:
        print(char,end="",flush=True)
        time.sleep(delay)
    print()

textwr("Привет,меня зовут Magenta. Я пытаюсь научиться программировать!",0.07)

def matrix_effect(text):

    display = [' '] * len(text)

    for cycles in range(10):
        for i in range(len(text)):
            if random.random() < 0.3:
                display[i] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            else:
                display[i] = ' '
        print(f"\r{''.join(display)}",end='',flush=True)
        time.sleep(0.1)

    print(f"\r{text}")

matrix_effect("Hello, im magenta")

text = str(input("Введите текст: "))
for _ in range(5):
    os.system('cls' if os.name== 'nt' else 'clear')

    print(text)
    time.sleep(0.3)

    os.system('cls' if os.name == 'nt' else 'clear')
    print('' + text + '')
    time.sleep(0.3)