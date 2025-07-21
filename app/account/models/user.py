from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from app.shared.links.movie_account_links import UserMovieVote


class SubscriptionType(str, Enum):
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
    subscription: SubscriptionType = Field(default=SubscriptionType.free)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    is_active: bool = Field(default=True)
    deleted_at: datetime = Field(nullable=True)
    votes: list["UserMovieVote"] = Relationship(back_populates="user")
