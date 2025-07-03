from pydantic import BaseModel, Field, ConfigDict, field_serializer


class MovieBase(BaseModel):
    title: str = Field(max_length=512)
    original_title: str | None = Field(default=None, max_length=512)
    description: str | None = Field(default=None, max_length=2000)


class MovieRead(MovieBase):
    # Позволяет создавать схему из ORM-объекта (например, SQLModel), а не только из dict
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str | None = None
    id_tmdb: int | None = None
    original_language: str | None = Field(default=None, max_length=15)
    poster: str | None = None
    backdrop: str | None = None
    release_date: str | None = Field(default=None, max_length=10)
    popularity: float | None = Field(default=None, ge=0.0)
    vote_average: float | None = Field(default=None, ge=0.0, le=10.0)
    vote_count: int | None = Field(default=None, ge=0)
    adult: bool = Field(default=False)
    genres: list["GenreRead"] = Field(
        default_factory=list, title="List of genres", description="List of genre slugs"
    )
    category: "CategoryRead" = Field(alias="categories",
        title="Category",
        description="Category to which the movie belongs",
    )


class MovieReadMainPage(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    release_date: str | None = None
    age_rating: str | None = None
    genres: str | None = Field(
        default=None, title="List of genres", description="List of genre slugs"
    )
    categories: str | None = Field(
        default=None,
        title="Category",
        description="Category to which the movie belongs",
    )

    duration: int | None = None
    poster: str | None = None
    backdrop: str | None = None
    trailer_url: str | None = None
    download_url: str | None = None


class MetaDataOffset(BaseModel):
    page: int
    per_page: int
    total_items: int
    total_pages: int
    has_more: bool


class MetaDataCursor(BaseModel):
    next_cursor: int | None = None
    per_page: int
    has_more: bool


class PaginatedOffsetMovieRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    meta: MetaDataOffset
    items: list[MovieReadMainPage]


class PaginatedCursorMovieRead(BaseModel):
    model_config = {"from_attributes": True}

    meta: MetaDataCursor
    items: list[MovieReadMainPage]


class MovieCreate(MovieBase):
    release_date: str | None = Field(
        default=None,
        max_length=10,
        title="Release date in YYYY-MM-DD format",
        json_schema_extra="2023-10-01",
        description="The release date of the movie in YYYY-MM-DD format.",
    )
    poster: str | None = Field(
        default=None,
        max_length=255,
        title="Poster URL Base URL= https://image.tmdb.org/t/p/",
        description="Put the full URL to the poster image to get the image"
        + "\n"
        + "w92-w154-w185-w342-500-780-original",
        json_schema_extra="https://image.tmdb.org/t/p/w342/your_image.jpg",
    )
    backdrop: str | None = Field(
        default=None,
        max_length=255,
        title="Backdrop URL Base URL= https://image.tmdb.org/t/p/",
        description="Put the full URL to the backdrop image to get the image"
        + "\n"
        + "w300-w780-w1280-original",
        json_schema_extra="https://image.tmdb.org/t/p/w780/your_image.jpg",
    )
    popularity: float | None = Field(default=None, ge=0.0, title="Popularity score")
    vote_average: float | None = Field(
        default=None, ge=0.0, le=10.0, title="Average rating"
    )
    vote_count: int | None = Field(default=None, ge=0, title="Number of votes")
    adult: bool = Field(default=False, title="Is the movie for adults?")
    id_tmdb: int | None = Field(default=None, title="TMDB ID")
    slug: str | None = Field(
        default=None,
        max_length=512,
        title="slugify of name",
        description="Slugified version of the title. URL-friendly and human-readable.",
    )
    original_language: str | None = Field(default=None, max_length=15)
    genres: list[int] = Field(
        default_factory=list,
        title="List of genre ids",
        description="list of genre IDs to assign to the movie",
    )
    category_id: int | None = None


class MovieUpdate(MovieBase):
    slug: str | None = None
    id_tmdb: int | None = None
    original_language: str | None = Field(default=None, max_length=15)
    backdrop: str | None = None
    poster: str | None = None
    popularity: float | None = Field(default=None, ge=0.0)
    release_date: str | None = Field(default=None, max_length=10)
    vote_count: int | None = Field(default=None, ge=0)
    vote_average: float | None = Field(default=None, ge=0.0, le=10.0)
    adult: bool = Field(default=False)
    genres: list[str] = Field(
        default_factory=list, title="List of genres", description="List of genre slugs"
    )
    category: str | None = Field(
        default=None,
        title="Category",
        description="category to which the movie belongs",
    )
    category_id: int | None = Field(default=None)
    genre_id: int | None = Field(default=None)


class MovieReadAccount(BaseModel):
    title: str
    genres: list[str] = Field(
        default_factory=list, title="List of genres", description="List of genre slugs"
    )
    category: str | None = Field(
        default=None,
        title="Category",
        description="category to which the movie belongs",
    )
    general_rating: int | None = None
    poster: str | None = None


from app.movie.schemas.category import CategoryRead, CategoryReadMainPage  # noqa: E402
from app.movie.schemas.genre import GenreRead, GenreReadMainPage  # noqa: E402


# Rebuild the model to ensure forward references are resolved
MovieRead.model_rebuild()
