from datetime import datetime, timezone
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int | None = Field(default=None)

    model_config = {"from_attributes": True}


class UserUpdate(UserBase):
    pass


class UserMovieVote(BaseModel):
    user_id: int 
    movie_id: int 
    vote_type: str 
    created_at: datetime 

class UserDetails(UserBase):
    id: int
    image_user: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    movies: list[UserMovieVote] = Field(default_factory=list)

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
