#app/routes/user_route.py

from fastapi import APIRouter, HTTPException
from app.schemas.users import UserResponse
from sqlalchemy import select
from app.database.database import DatabaseSession
from app.models.db_models import UserModel


user_routers = APIRouter(prefix="/users", tags=["user"])


@user_routers.get("/info/{user_id}", response_model=UserResponse)
async def get_userinfo(user_id: int, db: DatabaseSession = DatabaseSession):
    query = select(UserModel).where(UserModel.user_id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"Пользователь с id {user_id} не найден"
        )

    return {
        "message": f"Пользователь найден",
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "login": user.login,
            "email": user.email
        }
    }