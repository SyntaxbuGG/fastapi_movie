import shutil
from urllib import response
import uuid


from typing import Annotated, Literal
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlmodel import select, func, or_, not_
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.responses import BaseApiResponse
from ...models import Movie
from slugify import slugify
from ...schemas import movie as schemas
from app.db import get_db
from ...models.genre import Genre


movies_router = APIRouter()


SessionDep = Annotated[AsyncSession, Depends(get_db)]


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
    await session.commit()
    await session.refresh(db_movie)
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

    movie = await session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie.poster = file_location

    session.add(movie)
    await session.commit()
    session.refresh(movie)
    return movie


@movies_router.get("/", response_model=BaseApiResponse[schemas.PaginatedMovies])
async def list_movies_filter_offset(
    session: SessionDep,
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    per_page: int = Query(10, le=100, ge=10, description="Number of movies per page"),
    categories: list[int] = Query([], description="Filter by category IDs"),
    genres: list[int] = Query([], description="Filter by genre IDs"),
    title: str | None = Query(None, description="Search by movie title"),
    adult: bool = Query(default=False, description="Include adult content"),
    release_date_from: str | None = Query(
        default=None, description="Show movies released on or after this date"
    ),
    release_date_to: str | None = Query(
        default=None, description="Show movies released on or before this date"
    ),
    release_year: int | None = Query(
        default=None, description="Show movies released in a specific year"
    ),
    sort_by: Literal["latest", "newest", "popular"] = Query(
        default="latest",
        description="Sort by: latest (ID), newest (release date), or popular (popularity)",
    ),
):
    per_page = min(per_page, 100)
    stmt = select(Movie).options(
        selectinload(Movie.genres), selectinload(Movie.category)
    )

    if categories:
        stmt = stmt.where(Movie.category_id.in_(categories))
    if genres:
        stmt = stmt.where(or_(*[Movie.genres.any(Genre.id == g) for g in genres]))
    if title:
        stmt = stmt.where(Movie.title.ilike(f"%{title}%"))
    if not adult:
        stmt = stmt.where(not_(Movie.adult))
    if release_date_from:
        stmt = stmt.where(Movie.release_date >= release_date_from)
    if release_date_to:
        stmt = stmt.where(Movie.release_date <= release_date_to)
    if release_year:
        stmt = stmt.where(Movie.release_date.ilike(f"{release_year}-%"))
    if sort_by == "latest":
        stmt = stmt.order_by(Movie.id.desc())
    elif sort_by == "newest":
        stmt = stmt.order_by(Movie.release_date.desc())
    elif sort_by == "popular":
        stmt = stmt.order_by(Movie.popularity.desc())

    total_items = (
        await session.exec(select(func.count()).select_from(stmt.subquery()))
    ).one()
    if total_items == 0:
        movies = []
        total_pages = 0
    else:
        total_pages = (total_items + per_page - 1) // per_page
        if page > total_pages:
            raise HTTPException(status_code=404, detail="Page not found")
        offset = (page - 1) * per_page
        movies = (await session.exec(stmt.offset(offset).limit(per_page))).all()
    has_more = page < total_pages
    movie_read_list = [schemas.MovieRead.model_validate(movie) for movie in movies]

    response_data = schemas.PaginatedOffsetMovieRead(
        page=page,
        per_page=per_page,
        total_items=total_items,
        total_pages=total_pages,
        has_more=has_more,
        items=movie_read_list,
    )
    return BaseApiResponse.ok(
        data=response_data, message="Movies retrieved successfully"
    )


@movies_router.get(
    "/get_movies",
    response_model=BaseApiResponse[schemas.GenrePaginationMovieRead],
)
async def list_movies_filter_cursor(
    session: SessionDep,
    last_id: int = Query(
        default=None,
        ge=0,
        description="Cursor ID to get movies before this ID (used for pagination)",
    ),
    per_page: int = Query(10, le=100, ge=10, description="Number of movies per page"),
    categories: list[int] = Query([], description="Filter by category IDs"),
    genres: list[int] = Query([], description="Filter by genre IDs"),
    title: str | None = Query(None, description="Search by movie title"),
    adult: bool = Query(default=False, description="Include adult content"),
    release_date_from: str | None = Query(
        default=None, description="Show movies released on or after this date"
    ),
    release_date_to: str | None = Query(
        default=None, description="Show movies released on or before this date"
    ),
    release_year: int | None = Query(
        default=None, description="Show movies released in a specific year"
    ),
):
    stmt = select(Movie).options(
        selectinload(Movie.genres), selectinload(Movie.category)
    )

    if last_id is not None:
        stmt = stmt.where(Movie.id < last_id)
    if categories:
        stmt = stmt.where(Movie.category_id.in_(categories))
    if genres:
        stmt = stmt.where(or_(*[Movie.genres.any(Genre.id == g) for g in genres]))
    if title:
        stmt = stmt.where(Movie.title.ilike(f"%{title}%"))
    if not adult:
        stmt = stmt.where(not_(Movie.adult))
    if release_date_from:
        stmt = stmt.where(Movie.release_date >= release_date_from)
    if release_date_to:
        stmt = stmt.where(Movie.release_date <= release_date_to)
    if release_year:
        stmt = stmt.where(Movie.release_date.ilike(f"{release_year}-%"))

    stmt = stmt.order_by(Movie.id.desc()).limit(per_page + 1)
    result = await session.exec(stmt)
    movies = result.all()

    if not movies:
        raise HTTPException(status_code=404, detail="Page not found")
    count_movies = len(movies)

    movies = movies[:per_page]
    has_more = count_movies > per_page
    genre_movie_list = [schemas.MovieRead.model_validate(movie) for movie in movies]
    next_last_id = movies[-1].id if has_more else None

    response_data = schemas.PaginatedOffsetMovieRead(
        next_cursor=next_last_id,
        per_page=per_page,
        has_more=has_more,
        items=genre_movie_list,
    )

    return BaseApiResponse.ok(
        data=response_data, message="Category movies retrieved successfully"
    )


@movies_router.get("/{movie_id}", response_model=BaseApiResponse[schemas.MovieRead])
async def read_movie(movie_id: int, session: SessionDep):
    movie = await session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return BaseApiResponse.ok(data=movie, message="Succesfullu get details Movie")


@movies_router.put("/{movie_id}", response_model=schemas.MovieUpdate)
async def update_movie(
    movie_id: int, updated: schemas.MovieUpdate, session: SessionDep
):
    movie = await session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(movie, key, value)
    await session.commit()
    await session.refresh(movie)
    return movie


@movies_router.delete("/{movie_id}")
async def delete_movie(movie_id: int, session: SessionDep):
    movie = await session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    session.delete(movie)
    await session.commit()
    await session.refresh(movie)
    return {"ok": True}
