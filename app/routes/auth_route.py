from fastapi import APIRouter, HTTPException, status, Depends, Form
from sqlalchemy import select

from app.database.database import DatabaseSession
from app.dependencies.auth import get_current_active_user
from app.models.db_models import UserModel
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token

auth_routers = APIRouter(prefix="/auth", tags=["auth"])


@auth_routers.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: DatabaseSession):
    # Проверяем, не занят ли username или email
    query = select(UserModel).where(
        (UserModel.username == user_data.username) |
        (UserModel.email == user_data.email)
    )
    result = await db.execute(query)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    hashed = get_password_hash(user_data.password)
    new_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed,
        is_superuser=False
    )

    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)

    return new_user


@auth_routers.post("/login", response_model=Token)
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: DatabaseSession = None
):
    # Ищем пользователя
    query = select(UserModel).where(UserModel.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_routers.get("/me", response_model=UserResponse)
async def get_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user