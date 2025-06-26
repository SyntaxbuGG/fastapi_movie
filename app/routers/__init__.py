from fastapi import APIRouter
from app.account.routers import users_router
from app.movie.api.v1.movies import movies_router
from app.movie.api.v1.categories import category_router
from app.movie.api.v1.genres import genre_router
from app.movie.services.movie_service import router # noqa: F401

api_router = APIRouter()
api_router.include_router(users_router, prefix="/v1/users", tags=["users"])
api_router.include_router(movies_router, prefix="/v1/movies", tags=["movies"])
api_router.include_router(category_router, prefix="/v1/categories", tags=["categories"])
api_router.include_router(genre_router, prefix="/v1/genres", tags=["genres"])
# api_router.include_router(router=router, prefix='/add_database',tags=['database'])