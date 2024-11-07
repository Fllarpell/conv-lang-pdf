# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменные окружения для продакшн-окружения
ENV DJANGO_SECRET_KEY='your_production_secret_key'
ENV DJANGO_SETTINGS_MODULE='pdf_translator_web.settings'

# Собираем статические файлы (однократная сборка для подготовки образа)
RUN python manage.py collectstatic --noinput

# Добавляем права на выполнение для entrypoint.sh
RUN chmod +x /app/scripts/entrypoint.sh

# Устанавливаем entrypoint
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
