from datetime import datetime, timezone, timedelta
from jose import jwt, ExpiredSignatureError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from ..schemas import user as schms
from app.core.exceptions import (
    ResourceNotFoundError,
    InvalidCredentialsError,
    UserAccessForbiddenError,
)
from ..repositories import user_repo


def create_token(sub: str, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": sub, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(sub: str, expires_delta: timedelta | None = None) -> str:
    return create_token(sub, expires_delta)


def create_refresh_token(sub: str, expires_delta: timedelta | None = None) -> str:
    return create_token(sub, expires_delta)


async def refresh_access_token_logic(
    session: AsyncSession, data: schms.TokenRefreshRequest
) -> str:
    try:
        refresh_token = data.refresh_token
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        username_or_email = payload.get("sub")
        if not username_or_email:
            raise InvalidCredentialsError(detail="Invalid refresh token")
        user = user_repo.find_by_username_or_email(
            session=session, identifier=username_or_email
        )
    except ExpiredSignatureError:
        raise UserAccessForbiddenError(message="Refresh token has expired")

    if not user:
        raise ResourceNotFoundError(resource="user", message="User not found")
    new_access_token = create_access_token(
        sub=username_or_email,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return new_access_token
