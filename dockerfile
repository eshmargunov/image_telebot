FROM python:3.11-slim

# Установка рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY . .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Создание не-root пользователя для безопасности
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Запуск бота
CMD ["python", "main.py"]