import shutil
from turtle import back
import uuid


from typing import Annotated, Literal
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, status
from sqlmodel import select, func, or_, not_
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.responses import BaseApiResponse
from ...models.movie import Movie
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


@movies_router.get(
    "/", response_model=BaseApiResponse[schemas.PaginatedOffsetMovieRead]
)
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
            return BaseApiResponse.fail(status_code=204, detail="Movie not found")
        offset = (page - 1) * per_page
        movies = (await session.exec(stmt.offset(offset).limit(per_page))).all()
    has_more = page < total_pages
    items = [
        schemas.MovieReadMainPage(
            id=mov.id,
            title=mov.title,
            release_date=mov.release_date,
            age_rating=mov.age_rating,
            genre=mov.genres[0].name if mov.genres else None,
            category=mov.category.name,
            duration=mov.duration,
            poster=mov.poster,
            backdrop=mov.backdrop,
            is_premium=mov.is_premium,
            is_vip_only=mov.is_vip_only,
        )
        for mov in movies
    ]

    response_data = schemas.PaginatedOffsetMovieRead(
        meta=schemas.MetaDataOffset(
            page=page,
            per_page=per_page,
            total_items=total_items,
            total_pages=total_pages,
            has_more=has_more,
        ),
        items=items,
    )
    return BaseApiResponse.ok(
        data=response_data, message="Movies retrieved successfully"
    )


@movies_router.get(
    "/get_movies",
    response_model=BaseApiResponse[schemas.PaginatedCursorMovieRead],
)
async def list_movies_filter_cursor(
    session: SessionDep,
    last_id: int = Query(
        default=None,
        gt=0,
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
        return BaseApiResponse.fail(
            code=status.HTTP_204_NO_CONTENT, message="Movie not found"
        )
    count_movies = len(movies)

    movies = movies[:per_page]
    has_more = count_movies > per_page

    next_last_id = movies[-1].id if has_more else None
    items_movie = [
        schemas.MovieReadMainPage(
            id=mov.id,
            title=mov.title,
            release_date=mov.release_date,
            age_rating=mov.age_rating,
            genre=mov.genres[0].name if mov.genres else None,
            category=mov.category.name,
            duration=mov.duration,
            poster=mov.poster,
            backdrop=mov.backdrop,
            is_premium=mov.is_premium,
            is_vip_only=mov.is_vip_only,
        )
        for mov in movies
    ]
    response_data = schemas.PaginatedCursorMovieRead(
        meta=schemas.MetaDataCursor(
            next_cursor=next_last_id, per_page=per_page, has_more=has_more
        ),
        items=items_movie,
    )

    return BaseApiResponse.ok(data=response_data, message="Succes")


@movies_router.get("/{movie_id}", response_model=BaseApiResponse[schemas.MovieRead])
async def read_movie(movie_id: int, session: SessionDep):
    stmt = (
        select(Movie)
        .options(selectinload(Movie.category), selectinload(Movie.genres))
        .where(Movie.id == movie_id)
    )

    movie = (await session.exec(stmt)).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return BaseApiResponse.ok(
        data=schemas.MovieRead.model_validate(movie).model_dump(by_alias=True),
        message="Succesfullu get details Movie",
    )


@movies_router.patch("/{movie_id}", response_model=schemas.MovieUpdate)
async def update_movie(
    movie_id: int, updated: schemas.MovieUpdate, session: SessionDep
):
    movie = await session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in updated.model_dump(exclude_unset=True).items():
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
