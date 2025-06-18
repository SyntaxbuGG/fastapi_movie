from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlmodel import Session, select
from app.db import pwd_ctx, get_db
from .models import AccountUser
from typing import Annotated


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


SessionDep = Annotated[Session, Depends(get_db)]


def verify_password(plain, hashed):
    return pwd_ctx.verify(plain, hashed)


def get_password_hash(password):
    return pwd_ctx.hash(password)


def authenticate_user(session: Session, username: str, password: str):
    user = session.exec(
        select(AccountUser).where(AccountUser.username == username)
    ).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(sub: str, expires_delta: timedelta | None = None):
    to_encode = {"sub": sub}
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = session.exec(
        select(AccountUser).where(AccountUser.username == username)
    ).first()
    if user is None or user.disabled:
        raise credentials_exception
    return user

