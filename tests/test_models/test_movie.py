import pytest
from app.movie.models.movie import Movie


def test_movie_model_fields():
    movie = Movie(
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
    )

    assert movie.title == "Inception"
    assert movie.original_language == "en"
    assert movie.adult is False
    assert movie.release_date == "2010-07-16"


def test_movie_forward_refs():
    Movie.model_rebuild()
    # Check that relationships are intact
    assert hasattr(Movie, "model_fields")
    assert hasattr(Movie, "genres")
    assert hasattr(Movie, "category")
    assert "genres" in Movie.__annotations__
    assert "category" in Movie.__annotations__
