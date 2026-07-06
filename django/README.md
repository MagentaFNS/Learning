# 📦 Настройка виртуального окружения Python

Руководство по созданию и активации виртуального окружения для изоляции зависимостей проекта.

---

## 📋 Требования

- Python 3.8 или выше
- pip (устанавливается вместе с Python)

---

## 🐧 Linux (Ubuntu/Debian)

### 1. Установка venv
```bash
cd django
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```
---
### 🪟 Windows (CMD / PowerShell)

### 1. Установка venv
```bash
cd django
python -m venv venv
CMD:
venv\Scripts\activate.bat 
PowerShell:
venv\Scripts\Activate.ps1
pip install -r requirements.txt
deactivate