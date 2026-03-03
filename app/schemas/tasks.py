#app/schemas/tasks.py

from pydantic import BaseModel, field_validator
from typing import Annotated, Optional
from datetime import datetime


class TaskSchema(BaseModel):
    task_id: int
    title : str
    description : Optional[str] = None
    status : str
    creation_date : datetime
    deadline_date : datetime

class TaskResponse(BaseModel):
    message: str
    task: TaskSchema

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    deadline_date: datetime

class TaskUpdate(BaseModel):
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    deadline_date: Optional[datetime] = None
