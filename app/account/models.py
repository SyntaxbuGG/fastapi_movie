from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from app.movie.models.links import UserMovieVote


class SubscriptionType(str,Enum):
    free = "free"
    premium = "premium"
    vip = "vip"



class AccountUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=100)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    disabled: bool = False
    user_image: str | None = Field(default=None)
    subscription: SubscriptionType = Field(default=SubscriptionType.free, nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())

    votes: list["UserMovieVote"] = Relationship(back_populates="user")
