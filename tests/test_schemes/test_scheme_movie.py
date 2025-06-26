import pytest
from app.movie.schemas.movie import  MovieRead
from app.movie.schemas.genre import GenreRead
from app.movie.schemas.category import CategoryRead


class DummyMovie:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def test_movie_read_model_validation():
    genre = GenreRead(id=1, name="Action")
    genre2 = GenreRead(id=2, name="Sci-Fi")
    category = CategoryRead(id=1, name="Movie")
    orm_movie = DummyMovie(
        id=1,
        title="Inception",
        original_title="Inception",
        original_language="en",
        slug="inception",
        popularity=9.8,
        adult=False,
        poster="inception.jpg",
        backdrop="bg.jpg",
        release_date="2010-07-16",
        vote_average=8.8,
        vote_count=21000,
        id_tmdb=27205,
        category_id=1,
        description="A mind-bending thriller by Christopher Nolan.",
        genres=[genre, genre2],
        category=category,
    )
    movie = MovieRead.model_validate(orm_movie)
    assert movie.title == "Inception"
    assert movie.original_language == "en"
    assert movie.adult is False
    assert movie.genres[0] == genre
    assert movie.genres[1] == genre2
    assert movie.genres[0].id == 1


def test_movie_read_invalid_field():
    # Ошибка при указании неверного типа
    with pytest.raises(ValueError):
        MovieRead(
            id="not-an-int",
            title="Test",
            original_language=None,
            vote_average=5.5,
            genres=[],
            category=None,
        )

