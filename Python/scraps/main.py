import secrets
import string
import time

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