from sqlmodel import Field, Relationship, SQLModel


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Используем строковые аннотации для избежания циклических импортов
    from .movie import Movie


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_tmdb: int | None = Field(default=None, unique=True, index=True)
    name: str = Field(max_length=100, unique=True, index=True)
    description: str | None = Field(default=None, max_length=500)
    slug: str | None = Field(default=None, max_length=100, unique=True)
    
    movies: list["Movie"] = Relationship(back_populates="category")


# Rebuild the model to ensure all relationships are correctly set up
Category.model_rebuild()
