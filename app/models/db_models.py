#app/models/db_models.py
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from datetime import date

from app.database.database import Base

class TaskModel(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, nullable=False)
    creation_date = Column(Date, server_default=func.current_date())
    deadline_date = Column(DateTime(timezone=True), nullable=False)


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    login = Column(String, nullable=False)
    email = Column(String, nullable=False)