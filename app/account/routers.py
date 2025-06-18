from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.account import schemas
from app.account.models import AccountUser
from app.db import get_db
from .auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

users_router = APIRouter()


SessionDep = Annotated[Session, Depends(get_db)]



@users_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    session: SessionDep,
    user_data: schemas.UserCreate,
):
    existing_user = session.exec(
        select(AccountUser).where(
            (AccountUser.username == user_data.username)
            | (AccountUser.email == user_data.email)
        )
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this username or email already exists"
        )

    user = AccountUser(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User created successfully", "id": user.id}


@users_router.post("/token")
def login(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    access_token = create_access_token(
        sub=user.username, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@users_router.get("/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, session: SessionDep):
    userget = session.get(AccountUser, user_id)

    if not userget:
        raise HTTPException(status_code=404, detail="User not found")
    return userget


@users_router.get("/", response_model=list[schemas.UserRead])
def list_user(session: SessionDep):
    get_list = session.exec(select(AccountUser)).all()
    return get_list


@users_router.put("/{user_id}", response_model=schemas.UserUpdate)
def update_user(user_id: int, userupdate: schemas.UserUpdate, session: SessionDep):
    user = session.get(AccountUser, user_id)
    if user:
        for key, value in userupdate.dict(exclude_unset=True).items():
            setattr(user, key, value)
            session.commit()
    return user


@users_router.delete("{user_id}")
def delete_user(user_id: int, session: SessionDep):
    user_delete = session.get(AccountUser, user_id)
    if not user_delete:
        raise HTTPException(status_code=404, detail="User not found")
    with session:
        session.delete(user_delete)
        session.commit()
        session.refresh(user_delete)

    return user_delete
