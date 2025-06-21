from turtle import back
from sqlmodel import Relationship, SQLModel, Field


class MovieBase(SQLModel):
    name: str = Field(max_length=100, unique=True)
    description: str | None = Field(default=None, max_length=500)


class Category(MovieBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str | None = Field(max_length=100, unique=True)
    # загружает связанные фильмы пакетно (SELECT ... WHERE category_id IN ...), избегая N+1 запросов
    movies: list["Movie"] = Relationship(
        back_populates="category", sa_relationship_kwargs={"lazy": "selectin"}
    )


class MovieGenreLink(SQLModel, table=True):
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    genre_id: int = Field(foreign_key="genre.id", primary_key=True)


class Genre(MovieBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str | None = Field(max_length=100, unique=True)
    movies: list["Movie"] = Relationship(
        back_populates="genres",
        link_model=MovieGenreLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class Movie(MovieBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_tmdb: int | None = Field(default=None, unique=True, index=True)
    slug: str | None = Field(max_length=100, unique=True)
    popularity: float | None = Field(default=None, ge=0.0, index=True)
    adult: bool = Field(default=False)
    poster: str | None = Field(default=None, max_length=255)
    backdrop: str | None = Field(default=None, max_length=255)
    release_date: str | None = Field(default=None, max_length=10, index=True)
    vote_average: float | None = Field(default=None, ge=0.0, le=10.0, index=True)
    vote_count: int | None = Field(default=None, ge=0, index=True)
    category_id: int | None = Field(
        default=None, foreign_key="category.id", sa_column_kwargs={"index": True}
    )
    genres: list[Genre] = Relationship(
        back_populates="movies",
        link_model=MovieGenreLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    category: Category | None = Relationship(
        back_populates="movies", sa_relationship_kwargs={"lazy": "selectin"}
    )
