# 📦 Настройка виртуального окружения Python

Руководство по созданию и активации виртуального окружения для изоляции зависимостей проекта.

---

## 📋 Требования

- Python 3.8 или выше
- pip (устанавливается вместе с Python)

---

## 🐧 Linux (Ubuntu/Debian)

# Перейдите в папку проекта
cd ~/Learning/fastapi

# Активируйте виртуальное окружение FastAPI
source ../venv/bin/activate

# Проверьте, что все пакеты установлены
pip list | grep -E "(fastapi|uvicorn|sqlalchemy|psycopg2)"

# Запустите сервер
python main.py # Перейдите в папку проекта
cd ~/Learning/fastapi/project_practic

# Активируйте виртуальное окружение FastAPI
source ../venv/bin/activate

# Проверьте, что все пакеты установлены
pip list | grep -E "(fastapi|uvicorn|sqlalchemy|psycopg2)"

# Запустите сервер
python main.py