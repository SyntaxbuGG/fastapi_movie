from sqlalchemy import null
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.account.models.user import AccountUser
    from app.movie.models.movie import Movie


class MovieGenreLink(SQLModel, table=True):
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    genre_id: int = Field(foreign_key="genre.id", primary_key=True)


