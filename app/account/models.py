from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from app.movie.models import Movie
from app.movie.models.links import UserMovieVote


class AccountUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=100)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    disabled: bool = False
    image_user: str| None = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    movies: list["Movie"] = Relationship(
        back_populates="accounts", link_model=UserMovieVote
    )
