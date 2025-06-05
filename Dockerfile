# Використовуємо офіційний Python-образ (наприклад, Python 3.9)
FROM python:3.13.0

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо requirements.txt та встановлюємо залежності
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо увесь код застосунку в контейнер
COPY . /app/

# RUN python manage.py collectstatic --noinput
# RUN python manage.py migrate

EXPOSE 8080

# Запускаємо застосунок через gunicorn (якщо це Django-проєкт)
# або через іншу команду, залежно від вашої логіки запуску
CMD ["gunicorn", "Orion.wsgi:application", "--bind", "0.0.0.0:8000"]
