from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.account import schemas
from app.account.models import AccountUser
from app.db import get_db
from app.core.responses import BaseApiResponse
from .auth import (
    ALGORITHM,
    SECRET_KEY,
    create_refresh_token,
    get_password_hash,
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from jose import jwt, JWTError

users_router = APIRouter()


SessionDep = Annotated[AsyncSession, Depends(get_db)]


@users_router.post("/register", response_model=BaseApiResponse[schemas.UserRead])
async def register(
    session: SessionDep,
    user_data: schemas.UserCreate,
):
    existing_user = (
        await session.exec(
            select(AccountUser).where(
                (AccountUser.username == user_data.username.strip().lower())
                | (AccountUser.email == user_data.email)
            )
        )
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this username or email already exists"
        )

    user = AccountUser(
        username=user_data.username,
        email=user_data.email,
        hashed_password=await get_password_hash(user_data.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    data_user = schemas.UserRead.model_validate(user)

    return BaseApiResponse.ok(data=data_user, message="User created successfully")


@users_router.post("/login", response_model=BaseApiResponse[schemas.CreateToken])
async def login(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    access_token = await create_access_token(
        sub=user.username, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = await create_refresh_token(
        sub=user.username, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    access_token_data = schemas.CreateToken(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )
    return BaseApiResponse.ok(data=access_token_data, message="Login successful")


@users_router.post("/refresh", response_model=BaseApiResponse[schemas.GetRefreshToken])
async def refresh_access_token(session: SessionDep, data: schemas.TokenRefreshRequest):
    refresh_token = data.refresh_token
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        user = (
            await session.exec(
                select(AccountUser).where(AccountUser.username == username)
            )
        ).first()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_access_token = await create_access_token(
        sub=username, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    data_new_access_token = schemas.GetRefreshToken(
        access_token=new_access_token, token_type="bearer"
    )
    return BaseApiResponse.ok(
        data=data_new_access_token, message="Access token refreshed successfully"
    )


@users_router.put("/{user_id}", response_model=schemas.UserUpdate)
async def update_user(
    user_id: int, userupdate: schemas.UserUpdate, session: SessionDep
):
    user = await session.get(AccountUser, user_id)
    if user:
        for key, value in userupdate.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        await session.commit()
    return user


@users_router.delete("/{user_id}")
async def delete_user(user_id: int, session: SessionDep):
    user_delete = await session.get(AccountUser, user_id)
    if not user_delete:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user_delete)
    await session.commit()
    session.refresh(user_delete)

    return BaseApiResponse.ok(data={"ok": True}, message="User deleted successfully")


# @users_router.get("/{user_id}", response_model=schemas.UserRead)
# def get_user(user_id: int, session: SessionDep):
#     userget = session.get(AccountUser, user_id)

#     if not userget:
#         raise HTTPException(status_code=404, detail="User not found")
#     return userget


@users_router.get("/", response_model=BaseApiResponse[list[schemas.UserRead]])
async def list_user(session: SessionDep):
    get_list = (await session.exec(select(AccountUser))).all()

    return BaseApiResponse.ok(
        data=[schemas.UserRead.model_validate(user) for user in get_list],
        message="Users retrieved successfully",
    )
