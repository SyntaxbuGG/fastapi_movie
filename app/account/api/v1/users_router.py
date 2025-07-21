from fastapi import APIRouter, Depends, UploadFile, File, Query
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta


from app.account.repositories import user_repo

from ...schemas import user as schms
from ...services import auth_service, user_service, upload_service
from app.core.responses import BaseApiResponse
from ...security.jwt_tokens import (
    create_access_token,
    create_refresh_token,
    refresh_access_token_logic,
)
from app.deps.settings import SettingsDep
from app.deps.db import SessionDep
from app.deps.auth import CurrentUserDep


users_router = APIRouter()


@users_router.post("/register", response_model=BaseApiResponse[schms.UserRead])
async def register(
    session: SessionDep,
    user_data: schms.UserCreate,
):
    data_user = await auth_service.register_user_logic(
        session=session, user_data=user_data
    )
    return BaseApiResponse.ok(data=data_user, message="User created successfully")


@users_router.post("/login", response_model=BaseApiResponse[schms.CreateToken])
async def login(
    session: SessionDep,
    settings: SettingsDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await auth_service.authenticate_user(
        session=session,
        username_or_email=form_data.username,
        password=form_data.password,
    )
    access_token = create_access_token(
        sub=str(user.id),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(
        sub=str(user.id),
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    access_token_data = schms.CreateToken(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )
    return BaseApiResponse.ok(data=access_token_data, message="Login successful")


@users_router.post(
    "/token",
    summary="OAuth2 Password Grant Login for Swagger UI",
    include_in_schema=False,
)
async def login_for_access_token(
    session: SessionDep,
    settings: SettingsDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await auth_service.authenticate_user(
        session=session,
        username_or_email=form_data.username,
        password=form_data.password,
    )
    access_token = create_access_token(
        sub=str(user.id),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}


@users_router.post("/refresh", response_model=BaseApiResponse[schms.GetRefreshToken])
async def refresh_access_token(session: SessionDep, data: schms.TokenRefreshRequest):
    new_access_token = await refresh_access_token_logic(session=session, data=data)
    data_new_access_token = schms.GetRefreshToken(
        access_token=new_access_token, token_type="bearer"
    )
    return BaseApiResponse.ok(
        data=data_new_access_token, message="Access token refreshed successfully"
    )


@users_router.patch("/me", response_model=BaseApiResponse[schms.UserUpdate])
async def update_user(
    current_user: CurrentUserDep,
    userupdate: schms.UserUpdate,
    session: SessionDep,
):
    updated_user = await user_service.update_user_logic(
        session=session,
        user_id=current_user.id,
        update_data=userupdate,
    )
    return BaseApiResponse.ok(data=updated_user, message="Success")


@users_router.delete("/me")
async def delete_user(current_user: CurrentUserDep, session: SessionDep):
    result = await user_service.delete_user_logic(
        session=session, user_id=current_user.id
    )
    return BaseApiResponse.ok(data=result, message="User deleted successfully")


@users_router.get("/me", response_model=BaseApiResponse[schms.UserDetails])
async def get_user_details(current_user: CurrentUserDep, session: SessionDep):
    schemadetails = await user_service.get_user_details_logic(
        session=session, user_id=current_user.id
    )
    return BaseApiResponse.ok(data=schemadetails, message="Succesfully")


@users_router.post("/profile-image", response_model=dict)
async def upload_avatar(
    session: SessionDep,
    current_user: CurrentUserDep,
    file: UploadFile = File(...),
):
    avatar_url = await upload_service.upload_user_image(session, current_user, file)
    return BaseApiResponse.ok(data=avatar_url, message="Avatar uploaded")


@users_router.get("/", response_model=BaseApiResponse[list[schms.UserRead]])
async def list_user(session: SessionDep):
    get_list = await user_repo.get_all_users(session=session)

    return BaseApiResponse.ok(
        data=[schms.UserRead.model_validate(user) for user in get_list],
        message="Users retrieved successfully",
    )


@users_router.post("/rate-favorite", response_model=BaseApiResponse[str])
async def rate_or_favorite_movie(
    session: SessionDep,
    current_user: CurrentUserDep,
    movie_id: int,
    rating: int | None = Query(default=None, ge=1, le=5),
    is_favorite: bool | None = Query(default=None),
):
    result = await user_service.add_user_favorites_logic(
        session, current_user.id, movie_id, rating, is_favorite
    )
    return BaseApiResponse.ok(data=result)


@users_router.get(
    "/favorites", response_model=BaseApiResponse[list[schms.UserFavorites]]
)
async def get_favorites(session: SessionDep, current_user: CurrentUserDep):
    data_response = await user_service.get_favorites_logic(session, current_user.id)
    return BaseApiResponse.ok(data=data_response)
