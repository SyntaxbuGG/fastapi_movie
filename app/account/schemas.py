from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
from fastapi import Depends


class UserBase(BaseModel):
    username: str = Field(max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int | None = Field(default=None)


class UserUpdate(UserBase):
    pass


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
