#!/bin/bash

# Применяем миграции Alembic
alembic upgrade head

# Запускаем FastAPI-приложение
gunicorn app.main:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker
