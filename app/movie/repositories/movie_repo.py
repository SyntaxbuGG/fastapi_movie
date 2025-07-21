from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from datetime import datetime
from sqlalchemy.orm import selectinload

from ..models.movie import Movie


async def get_movie(session: AsyncSession, movie_id):
    result = await session.get(Movie, movie_id)
    return result
