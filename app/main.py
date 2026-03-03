import uvicorn as uvicorn
import datetime
from fastapi import FastAPI
from fastapi.responses import FileResponse
from typing import Annotated
from app.schemas.tasks import TaskSchema
from app.schemas.users import UserSchema
from app.routes import user_route, task_route, auth_route

app = FastAPI()

app.include_router(user_route.user_routers)
app.include_router(task_route.task_routers)
app.include_router(auth_route.auth_routers)

users_list = []
tasks_list = []

@app.post("/user")
async def create_user(user: UserSchema):
    #TODO DATABASE MANAGEMENT
    users_list.append({"id": user.user_id, "username": user.username})
    return {"message": "user created"}


# @app.get("/userinfo/{user_id}")
# async def get_userinfo(user_id: int):
#     #TODO connect to db and extract user data
#     for user in users_list:
#         if user["id"] == user_id:
#             return {"message": user["username"]}
#     return {"message": "user not found"}


@app.post("/task")
async def create_task(task: TaskSchema):
    # TODO DATABASE MANAGEMENT
    tasks_list.append({
                       "id": task.id,
                       "title": task.title,
                       "description": task.description,
                       "status": task.status,
                       "creation_date": task.creation_date,
                       "deadline_date": task.deadline_date,
    })
    return {"message": "Task created"}

@app.get("/taskinfo/{task_id}")
async def get_taskinfo(task_id: int):
    for task in tasks_list:
        if task["id"] == task_id:
            return task
    return {"message": "task not found"}



if __name__ == "__main__":
    uvicorn.run(
                app,
                host="127.0.0.1",
                port=8000
    )
