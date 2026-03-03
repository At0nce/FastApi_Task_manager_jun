#app/routes/task_route.py

from fastapi import APIRouter, HTTPException
from app.schemas.tasks import TaskResponse, TaskCreate, TaskUpdate
from sqlalchemy import select, insert, delete
from app.database.database import DatabaseSession
from app.models.db_models import TaskModel


task_routers = APIRouter(prefix="/tasks", tags=["task"])

#TODO Create/Update/Delete/Read task

@task_routers.get("/info/{task_id}", response_model=TaskResponse)
async def get_task_info(task_id: int, db: DatabaseSession = DatabaseSession):
    query = select(TaskModel).where(TaskModel.task_id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Задача с id {task_id} не найдена"
        )

    return {
        "message": f"Задача найдена",
        "task": {
            "task_id": task.task_id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "creation_date": task.creation_date,
            "deadline_date": task.deadline_date,
        }
    }

@task_routers.post("/create_task", response_model=TaskResponse)
async def create_new_task(
        task_data: TaskCreate,
        db: DatabaseSession = DatabaseSession
):
    try:
        new_task = TaskModel(**task_data.model_dump())
        db.add(new_task)
        await db.flush()
        await db.refresh(new_task)

        return {
            "message": f"Задача создана",
            "task": new_task
        }
    except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка при создании задачи: {str(e)}"
            )

@task_routers.patch("/update_task", response_model=TaskResponse)
async def update_new_task(
        task_data: TaskUpdate,
        db: DatabaseSession = DatabaseSession
):
    try:
        query = select(TaskModel).where(TaskModel.task_id == task_data.task_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()

        if task is None:
            raise HTTPException(
                status_code=404,
                detail=f"Задача с id {task_data.task_id} не найдена"
            )

        update_data = task_data.model_dump(exclude_unset=True, exclude={'task_id'})

        for field, value in update_data.items():
            setattr(task, field, value)

        await db.flush()
        await db.refresh(task)

        return {
            "message": f"Задача обновлена",
            "task": task
        }
    except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка при обновлении задачи: {str(e)}"
            )

@task_routers.delete("/delete_task/{task_id}")
async def get_task_info(
        task_id: int,
        db: DatabaseSession = DatabaseSession
):
    query = select(TaskModel).where(TaskModel.task_id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Задача с id {task_id} не найдена"
        )

    await db.delete(task)
    await db.flush()

    return {
        "message": f"Задача {task_id} успешно удалена",
    }