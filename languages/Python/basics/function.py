print('\n Пример 1 \n')

def test_func():
    pass

test_func() #ничего не выведет

print('\n Пример 2 \n')

# задача напечатать функцию которая выводит данные о тебе 
def func(name,age,city):
    return f'имя:{name}\nвозраст:{age}\nгород:{city}' # \n означает переход на новуюстроку,а f означает format

name = input('Введите имя: ')
age = int(input('Введите возраст: '))
city = input('Введите город: ')

print(func(name,age,city))

# функции могут пригодиться для больших проектов,чтобы код был понятнее и не надо было задачу решать 2 и более раза

print('\n Пример 3 \n')

#например будем писать дату по данным
def show_date(year,month,day):
    return f'Сегодня:{year},{month},{day}'

year,month,day = int(input('Год: ')),input('Месяц: '),input('День: ')
print(show_date(year,month,day))

