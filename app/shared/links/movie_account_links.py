from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.account.models.user import AccountUser
    from app.movie.models.movie import Movie


class UserMovieVote(SQLModel, table=True):
    user_id: int = Field(foreign_key="accountuser.id", primary_key=True)
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    user_rating: int | None = Field(
        default=None, ge=1, le=5, description="User rating from 1 to 5"
    )
    is_favorite: bool = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime | None = Field(default=None)
    user: "AccountUser" = Relationship(back_populates="votes")
    movie: "Movie" = Relationship(back_populates="votes")
