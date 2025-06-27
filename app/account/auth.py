import os
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import get_db
from .models import AccountUser
from typing import Annotated
from dotenv import load_dotenv
from fastapi.concurrency import run_in_threadpool

import bcrypt


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")


SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def hash_password(password: str) -> str:
    return await run_in_threadpool(
        lambda: bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    )


async def verify_password(plain: str, hashed: str) -> bool:
    return await run_in_threadpool(
        lambda: bcrypt.checkpw(plain.encode(), hashed.encode())
    )


async def authenticate_user(session: SessionDep, username: str, password: str):
    user = (
        await session.exec(
            select(AccountUser).where(AccountUser.username == username.strip().lower())
        )
    ).first()
    if not user or not await verify_password(password, user.hashed_password):
        return None
    return user


async def create_access_token(sub: str, expires_delta: timedelta | None = None):
    to_encode = {"sub": sub}
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def create_refresh_token(sub: str, expires_delta: timedelta | None = None):
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=7))
    to_encode = {"sub": sub, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id = payload.get("sub")
        print(user_id)
        
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except (JWTError, ValueError) as e:
        
        print(f"JWT Decode Error: {e}")

        raise credentials_exception
    user = await session.get(AccountUser, user_id)
    if user is None or user.disabled:
        raise credentials_exception
    return user
