from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from slugify import slugify
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_db
from app.core.responses import BaseApiResponse
from app.movie.schemas import category as schemas
from app.movie.models import Category, Movie
from app.movie.schemas.movie import MovieRead


SessionDep = Annotated[AsyncSession, Depends(get_db)]

category_router = APIRouter()


@category_router.get(
    "/category/", response_model=BaseApiResponse[list[schemas.CategoryRead]]
)
async def list_category(session: SessionDep):
    data_categories = (await session.exec(select(Category))).all()
    return BaseApiResponse.ok(
        data=data_categories, message="Category retrieved successfully"
    )


@category_router.post("/category/", response_model=schemas.CategoryCreate)
async def create_category(category: schemas.CategoryCreate, session: SessionDep):
    generated_slug = slugify(category.name)
    db_movie = Category(**category.model_dump(exclude={"slug"}), slug=generated_slug)

    session.add(db_movie)
    await session.commit()
    await session.refresh(db_movie)
    return db_movie


@category_router.get(
    "/category/{category_id}",
    response_model=BaseApiResponse[schemas.CatPaginationMovieRead],
)
async def get_category_movies(
    category_id: int,
    session: SessionDep,
    last_id: int = Query(default=None, ge=1),
    per_page: int = Query(default=10, le=100, ge=10),
    title: str | None = None,
    release_date: str | None = Query(default=None, example="2023-01-01"),
):
    if not await session.get(Category, category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    stmt = select(Movie).where(Movie.category_id == category_id)

    if title:
        stmt = stmt.where(Movie.title.ilike(f"%{title}%"))
    if release_date:
        stmt = stmt.where(Movie.release_date.ilike(f"{release_date}"))
    if last_id is not None:
        stmt = stmt.where(Movie.id > last_id)

    stmt = stmt.order_by(Movie.id).limit(per_page + 1)
    stmt = stmt.options(selectinload(Movie.genres), selectinload(Movie.category))
    movies = (await session.exec(stmt)).all()
    movies = movies[:per_page]
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found for this category")
    total_movies = len(movies)

    has_more = total_movies > per_page

    category_movies_list = [MovieRead.model_validate(movie) for movie in movies]

    next_last_id = movies[-1].id if has_more else None

    data_movie_cat = schemas.CatPaginationMovieRead(
        last_id=next_last_id,
        next_cursor=next_last_id,
        per_page=per_page,
        items=category_movies_list,
    )

    return BaseApiResponse.ok(
        data=data_movie_cat, message="Category movies retrieved successfully"
    )
