from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING

from .links import MovieGenreLink, UserMovieVote




if TYPE_CHECKING:
    from .genre import Genre
    from .category import Category
    from app.account.models import AccountUser
    


class Movie(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_tmdb: int | None = Field(default=None, unique=True, index=True)
    title: str = Field(max_length=512, index=True)
    original_title: str | None = Field(default=None, max_length=512)
    original_language: str | None = Field(default=None, max_length=15)
    description: str | None = Field(default=None, max_length=2000)
    slug: str | None = Field(max_length=512, index=True)
    download_url: str | None = Field(max_length=512)
    age_rating: str | None = Field(default=None, max_length=20)
    duration: int | None = Field(default=None)
    trailer_url: str | None = Field(default=None, max_length=512)
    popularity: float | None = Field(default=None, ge=0.0, index=True)
    adult: bool = Field(default=False)
    poster: str | None = Field(default=None, max_length=255)
    backdrop: str | None = Field(default=None, max_length=255)
    release_date: str | None = Field(default=None, max_length=10, index=True)
    vote_average: float | None = Field(default=None, ge=0.0, le=10.0, index=True)
    vote_count: int | None = Field(default=None, ge=0, index=True)
    general_rating: int | None = Field(default=None)
    
    category_id: int | None = Field(
        default=None, foreign_key="category.id", sa_column_kwargs={"index": True}
    )
    #: List of genres associated with this movie.
    genres: list["Genre"] = Relationship(
        back_populates="movies",
        link_model=MovieGenreLink,
    )
    category: "Category" = Relationship(back_populates="movies")

    accounts: list["AccountUser"] = Relationship(
        back_populates="movies", link_model=UserMovieVote
    )

