#app/schemas/users.py

from pydantic import BaseModel
from typing import Annotated
from datetime import datetime


class UserSchema(BaseModel):
    user_id: int
    username: str
    login : str
    email: str
    #login : str
    #password : str #TODO rework into auth

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    message: str
    user: UserSchema