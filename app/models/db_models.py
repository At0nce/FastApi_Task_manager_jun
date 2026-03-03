#app/models/db_models.py
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import date
from app.database.database import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    tasks = relationship("TaskModel", back_populates="owner")


class TaskModel(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, nullable=False)
    creation_date = Column(Date, server_default=func.current_date())
    deadline_date = Column(DateTime(timezone=True), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    owner = relationship("UserModel", back_populates="tasks")


