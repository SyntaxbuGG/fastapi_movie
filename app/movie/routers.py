from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from app.movie.models import Category, Movie
from slugify import slugify
from . import schemas
import shutil
import uuid
import logging
from app.db import get_db

logger = logging.getLogger(__name__)

movies_router = APIRouter()


SessionDep = Annotated[Session, Depends(get_db)]


@movies_router.post("/", response_model=schemas.MovieCreate)
async def create_movie(
    movie: schemas.MovieCreate,
    session: SessionDep,
):
    generated_slug = slugify(movie.name)

    db_movie = Movie(
        **movie.dict(exclude={"slug"}),
        slug=generated_slug,
    )
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie


@movies_router.post("/{movie_id}/poster", response_model=schemas.MovieRead)
async def upload_movie_poster(
    movie_id: int,
    session: SessionDep,
    poster: UploadFile = File(...),
):
    filename = f"{uuid.uuid4().hex[:8]}_{poster.filename}"
    file_location = f"app/static/posters/{filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(poster.file, buffer)

    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie.poster = file_location

    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


@movies_router.get("/", response_model=list[schemas.MovieRead])
async def list_movies(session: SessionDep):
    return session.exec(select(Movie)).all()


@movies_router.get("/{movie_id}", response_model=schemas.MovieRead)
async def read_movie(movie_id: int, session: SessionDep):
    movie = session.get(Movie, movie_id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@movies_router.put("/{movie_id}", response_model=schemas.MovieUpdate)
async def update_movie(
    movie_id: int, updated: schemas.MovieUpdate, session: SessionDep
):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(movie, key, value)
    session.commit()
    session.refresh(movie)
    return movie


@movies_router.delete("/{movie_id}")
async def delete_movie(movie_id: int, session: SessionDep):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    session.delete(movie)
    session.commit()
    session.refresh(movie)
    return {"ok": True}


@movies_router.get("/category/", response_model=list[schemas.CategoryRead])
async def list_category(session: SessionDep):
    return session.exec(select(Category)).all()


@movies_router.post("/category/", response_model=schemas.MovieBase)
async def create_category(category: schemas.MovieBase, session: SessionDep):
    generated_slug = slugify(category.name)
    db_movie = Category(**category.dict(exclude={"slug"}), slug=generated_slug)

    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie
