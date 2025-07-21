from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime

from app.account.repositories import user_repo
from app.movie.repositories import movie_repo
from app.core.exceptions import ResourceNotFoundError, InvalidInputError
from ..schemas import user as schms
from app.shared.links.movie_account_links import UserMovieVote
from app.shared.links.repositories import user_movie_repo


async def delete_user_logic(session: AsyncSession, user_id: int) -> dict:
    user = await user_repo.get_active_user(session=session, user_id=user_id)
    if not user:
        raise ResourceNotFoundError(resouce="User")
    await user_repo.soft_delete_user(session=session, user=user)
    return {"ok": True}


async def update_user_logic(
    session: AsyncSession,
    user_id: int,
    update_data: schms.UserUpdate,
) -> schms.UserUpdate:
    user = await user_repo.get_active_user(session=session, user_id=user_id)

    if not user:
        raise ResourceNotFoundError("User")

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    await session.commit()
    await session.refresh(user)

    return user


async def get_user_details_logic(
    session: AsyncSession, user_id: int
) -> schms.UserDetails:
    user = await user_repo.get_user_with_votes(session, user_id)
    if not user:
        raise ResourceNotFoundError("User")

    return schms.UserDetails(
        id=user.id,
        username=user.username,
        email=user.email,
        user_image=user.user_image,
        created_at=user.created_at,
        subscription=user.subscription,
    )


async def add_user_favorites_logic(
    session: AsyncSession,
    user_id: int,
    movie_id: int,
    rating: int | None = None,
    is_favorite: bool | None = None,
) -> str:
    movie = await movie_repo.get_movie(session=session, movie_id=movie_id)
    if not movie:
        raise ResourceNotFoundError(resource="Movie")
    if rating is None and is_favorite is None:
        raise InvalidInputError(
            field="rate_favorite",
            message="You must provide at least one of 'rating' or 'is_favorite'.",
        )

    existingvote = await user_movie_repo.get_user_vote(session, user_id, movie_id)
    if existingvote:
        if rating is not None:
            existingvote.user_rating = rating
        if is_favorite is not None:
            existingvote.is_favorite = is_favorite
        existingvote.updated_at = datetime.now()
        await session.commit()
        return "Vote changed"
    else:
        new_vote = UserMovieVote(
            user_id=user_id,
            movie_id=movie_id,
            is_favorite=is_favorite,
            rating=rating,
        )
        session.add(new_vote)
        await session.commit()
        return "added"


async def get_favorites_logic(session: AsyncSession, user_id: int):
    votes = await user_movie_repo.get_users_favorites(session, user_id)
    data_response = [
        schms.UserFavorites(
            id=mov.movie.id,
            title=mov.movie.title,
            poster=mov.movie.poster,
            backdrop=mov.movie.backdrop,
            download_url=mov.movie.download_url,
            genre=mov.movie.genres[0].name if mov.movie.genres else None,
            rating=mov.movie.rating,
        )
        for mov in votes
        if mov.movie is not None
    ]
    return data_response
