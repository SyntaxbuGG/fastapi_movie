from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    name: str = Field(max_length=100, unique=True)
    description: str | None = Field(default=None, max_length=500)


class MovieRead(MovieBase):
    id: int
    slug: str = Field(
        title="slugify of name",
        description="You can user this slug for readable for user and escapes",
    )
    poster: str | None = None
    release_year: int | None = None
    rating: float | None = None
    category_id: int | None = Field(default=None, foreign_key="category.id")
    genre_id: int | None = None


class MovieCreate(MovieBase):
    release_year: int | None = Field(
        default=None,
        ge=1888,
        le=2100,
        index=True,
        title="slugify of name",
        description="You can user this slug for readable for user and escapes",
    )
    rating: float | None = Field(default=None, ge=0.0, le=10.0)
    category_id: int | None = Field(default=None, foreign_key="category.id")
    genre_id: int | None = Field(default=None)


class MovieUpdate(MovieBase):
    slug: str | None = None
    poster: str | None = None
    release_year: int | None = Field(default=None, ge=1888, le=2100)
    rating: float | None = Field(default=None, ge=0.0, le=10.0)
    category_id: int | None = Field(default=None)
    genre_id: int | None = Field(default=None)


class CategoryRead(MovieBase):
    id: int
    slug: str


class GenreRead(MovieBase):
    id: int
    slug: str
