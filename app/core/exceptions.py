from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.responses import BaseApiResponse


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    error_details = {
        "path": request.url.path,
        "method": request.method,
        "status_code": exc.status_code,
        "detail": str(exc.detail),
    }
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseApiResponse.fail(
            code="HTTP_ERROR", message=str(exc.detail)
        ).model_dump()
        | {"details": error_details},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = exc.errors()

    return JSONResponse(
        status_code=422,
        content=BaseApiResponse.fail(
            code="VALIDATION_ERROR", message="Invalid request"
        ).model_dump()
        | {"details": error_details},
    )
