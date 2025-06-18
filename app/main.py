from contextlib import asynccontextmanager
from fastapi import FastAPI
from app import routers
from sqlmodel import SQLModel
from app.db import engine
from fastapi.middleware.cors import CORSMiddleware


# import logging
# logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 👇 Выполняется при запуске
    # SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Movies API",
    description="API for managing movies",
    lifespan=lifespan,
    version="1.0.0",
    debug=True,
)



app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )


@app.get("/healthz", include_in_schema=False)
def health_check():
    return {"status": "ok"}


app.include_router(router=routers.api_router)
