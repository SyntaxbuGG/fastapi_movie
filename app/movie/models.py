from sqlmodel import SQLModel, Field


class MovieBase(SQLModel):
    name: str = Field(max_length=100, unique=True)
    description: str | None = Field(default=None, max_length=500)


class Category(MovieBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str | None = Field(max_length=100, unique=True)


class Genre(MovieBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str | None = Field(max_length=100, unique=True)


class Movie(MovieBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str | None = Field(max_length=100, unique=True)
    poster: str | None = Field(default=None, max_length=255)
    release_year: int | None = Field(default=None, ge=1888, le=2100, index=True)
    rating: float | None = Field(default=None, ge=0.0, le=10.0, index=True)
    category_id: int | None = Field(default=None, foreign_key="category.id")
    genre_id: int | None = Field(default=None, foreign_key="genre.id")
