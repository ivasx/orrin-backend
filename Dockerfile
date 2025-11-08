# Використовуємо офіційний образ Python
FROM python:3.13-slim

# Встановлюємо змінні середовища
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Створюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файл залежностей та встановлюємо їх
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копіюємо весь код проєкту в контейнер
COPY . .