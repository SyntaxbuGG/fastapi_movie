from sqlmodel.ext.asyncio.session import AsyncSession


from ..schemas import user as schms
from ..services.hashing import hash_password, verify_password
from ..repositories import user_repo
from app.core.exceptions import (
    ResourceNotFoundError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
)


async def register_user_logic(session: AsyncSession, user_data: schms.UserCreate):
    existing_user = await user_repo.check_username_or_email_exists(
        session=session, user_data=user_data
    )
    if existing_user:
        raise UserAlreadyExistsError()
    hashed_pw = await hash_password(user_data.password)
    user = await user_repo.save_user_db(
        session=session, user_data=user_data, hashed_password=hashed_pw
    )
    return user


async def authenticate_user(
    session: AsyncSession, username_or_email: str, password: str
):
    user = await user_repo.find_by_username_or_email(
        session=session, identifier=username_or_email
    )
    if not user:
        raise ResourceNotFoundError(
            resource="user", message="Username or Email is not found"
        )
    if not await verify_password(password, user.hashed_password):
        raise InvalidCredentialsError(message="Password cannot verify")
    return user
