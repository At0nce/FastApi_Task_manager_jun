# Task Manager API

FastAPI проект с PostgreSQL, SQLAlchemy и Alembic.

## Функционал
- CRUD для задач
- Работа с PostgreSQL
- Миграции через Alembic
- Асинхронные эндпоинты

## Установка
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Миграции
alembic -c app/alembic.ini upgrade head


## Тестовые данные
cd app/scripts
python create_data.py

