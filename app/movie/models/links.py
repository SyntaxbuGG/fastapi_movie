from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


class MovieGenreLink(SQLModel, table=True):
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    genre_id: int = Field(foreign_key="genre.id", primary_key=True)



class UserMovieVote(SQLModel, table=True):
    user_id: int = Field(foreign_key="accountuser.id", primary_key=True)
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    vote_type: str = Field(default="favorite")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
