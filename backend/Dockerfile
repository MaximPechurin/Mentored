FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput

# Для SQLite ничего дополнительно ставить не нужно

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]