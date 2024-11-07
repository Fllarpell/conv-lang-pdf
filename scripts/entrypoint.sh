#!/bin/bash

# Запуск миграций и сбор статических файлов
python /app/scripts/migrate_and_collect.py

# Запуск Gunicorn-сервера
exec gunicorn pdf_translator_web.wsgi:application --bind 0.0.0.0:8000 --workers 3
