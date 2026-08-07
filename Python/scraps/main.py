import secrets
import string

#Можно генерировать ключи 
# Только буквы и цифры (без спецсимволов)
alphabet = string.ascii_letters + string.digits
safe_key = ''.join(secrets.choice(alphabet) for _ in range(64))
print(safe_key)