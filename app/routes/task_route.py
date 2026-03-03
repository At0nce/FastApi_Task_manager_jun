#app/routes/task_route.py


from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from typing import List

from app.database.database import DatabaseSession
from app.models.db_models import TaskModel, UserModel
from app.schemas.tasks import TaskCreate, TaskUpdate, TaskResponse
from app.dependencies.auth import get_current_active_user, check_task_permission

task_routers = APIRouter(prefix="/tasks", tags=["task"])


@task_routers.get("/info/{task_id}", response_model=TaskResponse)
async def get_task_info(
        task_id: int,
        db: DatabaseSession = DatabaseSession,
        current_user: UserModel = Depends(get_current_active_user)
):
    task = await check_task_permission(task_id, current_user, db)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Задача с id {task_id} не найдена"
        )

    return {
        "message": f"Задача найдена",
        "task": task
    }


@task_routers.get("/my_tasks", response_model=List[TaskResponse])
async def get_my_tasks(
        db: DatabaseSession,
        current_user: UserModel = Depends(get_current_active_user)
):
    query = select(TaskModel).where(TaskModel.owner_id == current_user.user_id)
    result = await db.execute(query)
    tasks = result.scalars().all()

    return tasks


@task_routers.post("/create_task", response_model=TaskResponse)
async def create_new_task(
        task_data: TaskCreate,
        db: DatabaseSession = DatabaseSession,
        current_user: UserModel = Depends(get_current_active_user)
):
    try:
        new_task = TaskModel(
            **task_data.model_dump(),
            owner_id=current_user.user_id
        )
        db.add(new_task)
        await db.flush()
        await db.refresh(new_task)

        return {
            "message": f"Задача создана",
            "task": new_task,
            "owner_id": new_task.owner_id
        }
    except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка при создании задачи: {str(e)}"
            )

@task_routers.patch("/update_task")
async def update_new_task(
        task_data: TaskUpdate,
        task_id: int,
        db: DatabaseSession = DatabaseSession,
        current_user: UserModel = Depends(get_current_active_user)
):
    try:
        task = await check_task_permission(task_id, current_user, db)

        if task is None:
            raise HTTPException(
                status_code=404,
                detail=f"Задача с id {task_id} не найдена"
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
        db: DatabaseSession = DatabaseSession,
        current_user: UserModel = Depends(get_current_active_user)
):
    task = await check_task_permission(task_id, current_user, db)

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


@task_routers.get("/all_tasks", response_model=List[TaskResponse])
async def get_all_tasks(
        db: DatabaseSession,
        current_user: UserModel = Depends(get_current_active_user)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Only superuser can access all tasks"
        )

    query = select(TaskModel)
    result = await db.execute(query)
    tasks = result.scalars().all()

    return tasks