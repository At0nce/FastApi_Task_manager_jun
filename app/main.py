import uvicorn as uvicorn
import datetime
from fastapi import FastAPI
from fastapi.responses import FileResponse
from typing import Annotated
from app.schemas.tasks import TaskSchema
from app.schemas.users import UserSchema
from app.routes import user_route, task_route

app = FastAPI()

app.include_router(user_route.user_routers)
app.include_router(task_route.task_routers)

users_list = []
tasks_list = []

@app.post("/user")
async def create_user(user: UserSchema):
    #TODO DATABASE MANAGEMENT
    users_list.append({"id": user.id, "username": user.username})
    return {"message": "user created"}

if __name__ == "__main__":
    uvicorn.run(
                app,
                host="127.0.0.1",
                port=8000
    )
