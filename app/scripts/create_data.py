#app/scripts/create_data.py

import asyncio
import json
from datetime import datetime, date

from sqlalchemy import insert, delete
from app.models.db_models import UserModel, TaskModel
from app.database.database import engine


def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def prepare_tasks_data(tasks_data):
    """Преобразует строки с датами в объекты datetime"""
    prepared = []
    for task in tasks_data:
        task_dict = {
            'task_id': task['task_id'],
            'title': task['title'],
            'description': task.get('description'),
            'status': task['status'],
        }
        if task.get('deadline_date'):
            task_dict['deadline_date'] = datetime.fromisoformat(task['deadline_date'])

        if task.get('creation_date') is not None:
            if isinstance(task['creation_date'], str):
                task_dict['creation_date'] = date.fromisoformat(task['creation_date'])

        prepared.append(task_dict)
    return prepared


async def clear_table(table):
    """Очищает таблицу перед вставкой"""
    async with engine.connect() as conn:
        await conn.execute(delete(table))
        await conn.commit()
        print(f"Таблица {table.__tablename__} очищена")


async def create_table_with_inserted_data(table, data, clear_before=False):
    if clear_before:
        await clear_table(table)

    async with engine.connect() as conn:
        await conn.execute(insert(table), data)
        await conn.commit()
        print(f"Добавлено {len(data)} записей в {table.__tablename__}")


async def main():
    users_data = load_data("users.json")
    await create_table_with_inserted_data(UserModel, users_data, clear_before=True)


    tasks_data = load_data("tasks.json")
    tasks_formatted = prepare_tasks_data(tasks_data)
    await create_table_with_inserted_data(TaskModel, tasks_formatted, clear_before=True)

    print('create data')

if __name__ == '__main__':
    asyncio.run(main())