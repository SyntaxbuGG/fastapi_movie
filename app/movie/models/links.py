from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


class MovieGenreLink(SQLModel, table=True):
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    genre_id: int = Field(foreign_key="genre.id", primary_key=True)


class UserMovieVote(SQLModel, table=True):
    user_id: int = Field(foreign_key="accountuser.id", primary_key=True)
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    rating: int | None = Field(default=None, ge=1, le=5, description="User rating from 1 to 5")
    vote_type: str = Field(default="favorite")
    created_at: datetime = Field(default_factory=lambda: datetime.now())


