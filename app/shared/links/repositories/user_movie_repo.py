from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload

from ..movie_account_links import UserMovieVote
from app.movie.models.movie import Movie


async def get_user_vote(
    session: AsyncSession, user_id: int, movie_id: int
) -> UserMovieVote | None:
    result = await session.exec(
        select(UserMovieVote).where(
            UserMovieVote.user_id == user_id,
            UserMovieVote.movie_id == movie_id,
        )
    )
    return result.first()


async def get_users_favorites(
    session: AsyncSession,
    user_id,
):
    stmt = (
        select(UserMovieVote)
        .where(UserMovieVote.user_id == user_id, UserMovieVote.is_favorite.is_(True))
        .options(selectinload(UserMovieVote.movie).selectinload(Movie.genres))
    )
    result = (await session.exec(stmt)).all()
    return result
