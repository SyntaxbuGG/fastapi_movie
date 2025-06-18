from contextlib import asynccontextmanager
from fastapi import FastAPI
from app import routers
from sqlmodel import SQLModel
from app.db import engine


# import logging
# logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 👇 Выполняется при запуске
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Movies API",
    description="API for managing movies",
    lifespan=lifespan,
    version="1.0.0",
    debug=True,
)

app.include_router(router=routers.api_router)
