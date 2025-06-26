from sqlmodel import SQLModel, Field
from datetime import datetime


class AccountUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=100)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    disabled: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
