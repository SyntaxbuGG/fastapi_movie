from fastapi import APIRouter
from app.account.routers import users_router
from app.movie.routers import movies_router


api_router = APIRouter()
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(movies_router, prefix="/movies", tags=["movies"])


