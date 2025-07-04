from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from app.movie.schemas.movie import MovieReadAccount
from .models import SubscriptionType

class UserBase(BaseModel):
    username: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int | None = Field(default=None)
    subscription: SubscriptionType
    model_config = {"from_attributes": True}


class UserUpdate(UserBase):
    user_image: str | None = None


class UserFavorites(BaseModel):
    id: int | None = None
    title: str | None = None
    poster: str | None = None
    backdrop: str | None = None
    download_url: str | None = None
    genre: str | None = None
    rating: int | None = None



class UserDetails(UserBase):
    id: int
    user_image: str | None = None
    created_at: datetime
    subscription: SubscriptionType 

    model_config = {"from_attributes": True}


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class GetRefreshToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CreateToken(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class Succes(BaseModel):
    ok: str = "Succes"
