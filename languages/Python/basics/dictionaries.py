#Словарь — это неупорядоченная коллекция пар «ключ → значение».
#Пример словаря:
person = {
    'Name':'Alice',
    'Age':30,
    'City':'Moscow',
}

#Можно создать и пустой словарь.
empty = {}
empty = dict()

#или передать значение
dicti = dict(a=1,b=2)
squars = {x: x**2 for x in range(5)}


print('\n Пример 1 \n')

# и вот так выглядит вывод:

print(person['Name'])
print(person['Age']) #Если ключа нет будет выводить None 

print('\n Пример 2 \n')

#можно добавить и убрать значение 
person['Game'] = 'Fortnite'
print(person)

# и удалять
del person['Game'] # удаляет ключ (KeyError если нет)
print(person)

#Можно использовать pop и popitem или clear
# можно перебирать ключ и значение 
for key,value in person.items():
    print(f'Ключ:{key}, Значение:{value}')


print('\n Пример 3 \n')

#или можно проверять на наличие чего-то
if "Age" in person:
    print('Есть')

print('\n Пример 4 \n')

#Пример где может пригодиться:

text = 'Hello World'
freq = {}
for char in text:
    freq[char] = freq.get(char,0) + 1
print(freq)

data = [("apple", 1), ("banana", 2), ("apple", 3)]
grup = {}
for key,value in data:
    grup.setdefault(key,[]).append(value)
print(grup)

