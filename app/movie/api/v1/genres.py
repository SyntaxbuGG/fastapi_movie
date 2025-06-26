from typing import Annotated
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import not_, select, or_
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.responses import BaseApiResponse
from ...schemas import genre as schemas
from app.db import get_db
from ...models.genre import Genre
from ...models.movie import Movie
from ...schemas.movie import MovieRead


genre_router = APIRouter()


SessionDep = Annotated[AsyncSession, Depends(get_db)]


@genre_router.get("/", response_model=BaseApiResponse[list[schemas.GenreRead]])
async def get_list_genres(session: SessionDep):
    result = await session.exec(select(Genre))
    list_genre = result.all()

    return BaseApiResponse.ok(data=list_genre, message="Ok succesfully")
