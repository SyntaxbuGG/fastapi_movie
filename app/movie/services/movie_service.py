from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import get_db
from app.management.get_movieslist import save_movies_to_movies_category
from app.management.manage_add_db_data import add_categories_to_db, add_genres_to_db



router = APIRouter()


@router.post("/internal/import-movies")
async def import_movies_endpoint(session: AsyncSession = Depends(get_db)):
    # Здесь вызови функцию импорта, например
    # чтобы передать сессию, можно изменить save_movies_to_movies_category на async и принимать сессию
    # Но для простоты вызовем её напрямую (если нужно — перепиши под async)

    # ВАЖНО! Защити этот эндпоинт токеном или IP, чтобы никто чужой не запустил!

    try:
        await add_categories_to_db()
        await add_genres_to_db()
        await save_movies_to_movies_category()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Movies import started"}
