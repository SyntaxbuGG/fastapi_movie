from contextlib import asynccontextmanager
from fastapi import FastAPI
from app import routers

from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.exceptions import (
    AppBaseException,
    http_exception_handler,
    validation_exception_handler,
    app_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles


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


app.include_router(router=routers.api_router, prefix="/api", tags=["API movies"])
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(AppBaseException, app_exception_handler)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
