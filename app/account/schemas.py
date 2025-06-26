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
