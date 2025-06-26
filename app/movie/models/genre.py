from sqlmodel import Relationship, SQLModel, Field


from typing import TYPE_CHECKING
from .links import MovieGenreLink

if TYPE_CHECKING:
    from .movie import Movie


class Genre(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_tmdb: int | None = Field(default=None, unique=True, index=True)
    name: str = Field(max_length=100, unique=True,index=True)
    description: str | None = Field(default=None, max_length=500)
    slug: str | None = Field(default=None, max_length=100, unique=True, index=True)
    movies: list["Movie"] = Relationship(
        back_populates="genres",
        link_model=MovieGenreLink,
    )


# Rebuild the model to ensure all relationships are correctly set up
Genre.model_rebuild()
