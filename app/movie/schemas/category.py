from pydantic import BaseModel, Field
from .movie import MovieRead


example_data = {
    "name": "Live",
    "description": "концерты, спортивные трансляции, шоу",
    "id_tmdb": None,
}


class CategoryRead(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str | None = Field(max_length=512)
    


class CategoryReadMainPage(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None
    id_tmdb: int | None = None

    model_config = {"json_schema_extra": {"example": example_data}}


class CatPaginationMovieRead(BaseModel):
    model_config = {"from_attributes": True}

    last_id: int | None = None
    next_cursor: int | None = None
    per_page: int

    items: list[MovieRead]
