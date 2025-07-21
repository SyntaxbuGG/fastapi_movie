from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from datetime import datetime
from sqlalchemy.orm import selectinload

from ..schemas import user as schms
from ..models.user import AccountUser


async def check_username_or_email_exists(
    session: AsyncSession, user_data: schms.CheckUsernameEmail
) -> AccountUser | None:
    stmt = select(AccountUser).where(
        (AccountUser.username == user_data.username)
        | (AccountUser.email == user_data.email)
    )
    result = (await session.exec(stmt)).first()
    return result


async def get_user(session: AsyncSession, user_id: int) -> AccountUser | None:
    user = await session.get(AccountUser, user_id)
    return user


async def save_user_db(
    session: AsyncSession, user_data: schms.UserCreate, hashed_password: str
):
    user = AccountUser(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def find_by_username_or_email(
    session: AsyncSession, identifier: str
) -> AccountUser | None:
    identifier = identifier.strip().lower()
    stmt = select(AccountUser).where(
        (AccountUser.username == identifier) | (AccountUser.email == identifier),
        AccountUser.is_active.is_(True),
    )
    result = await session.exec(stmt)
    return result.first()


async def soft_delete_user(session: AsyncSession, user: AccountUser):
    user.is_active = False
    user.deleted_at = datetime.now()
    await session.commit()


async def get_active_user(session: AsyncSession, user_id: int) -> AccountUser | None:
    stmt = select(AccountUser).where(
        AccountUser.id == user_id, AccountUser.is_active.is_(True)
    )
    result = await session.exec(stmt)
    return result.first()


async def get_user_with_votes(
    session: AsyncSession, user_id: int
) -> AccountUser | None:
    stmt = (
        select(AccountUser)
        .options(selectinload(AccountUser.votes))
        .where(AccountUser.id == user_id, AccountUser.is_active.is_(True))
    )
    result = await session.exec(stmt)
    return result.first()


async def get_all_users(session: AsyncSession) -> list[AccountUser]:
    result = (
        await session.exec(select(AccountUser).where(AccountUser.is_active.is_(True)))
    ).all()
    return result
