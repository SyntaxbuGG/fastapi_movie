from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.responses import BaseApiResponse
from app.core.constants import status_codes as status


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
        status_code=status.HTTP_403_FORBIDDEN,
        content=BaseApiResponse.fail(
            code="VALIDATION_ERROR", message="Invalid request"
        ).model_dump()
        | {"details": error_details},
    )


class AppBaseException(Exception):
    status_code = status
    code = "APP_ERROR"
    message = "Something went wrong"

    def __init__(self, message: str | None = None):
        if message:
            self.message = message


async def app_exception_handler(request: Request, exc: AppBaseException):
    error_details = {
        "path": request.url.path,
        "method": request.method,
        "status_code": exc.status_code,
        "detail": exc.message,
    }
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseApiResponse.fail(code=exc.code, message=exc.message).model_dump()
        | {"details": error_details},
    )


class ResourceNotFoundError(AppBaseException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, resource: str = "resource", message: str | None = None):
        self.code = f"{resource.upper()}_NOT_FOUND"
        self.message = message or f"{resource.capitalize()} not found"


class InvalidCredentialsError(AppBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "INVALID_CREDENTIALS"
    message = "Invalid username or password"


class UserAccessForbiddenError(AppBaseException):
    status_code = status.HTTP_403_FORBIDDEN
    code = "USER_ACCESS_FORBIDDEN"
    message = "User does not have permission to access this resource"


class UserAlreadyExistsError(AppBaseException):
    status_code = status.HTTP_409_CONFLICT
    code = "USER_ALREADY_EXISTS"
    message = "User with this username or email already exists"


class InvalidInputError(AppBaseException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, field: str = "error", message=None):
        self.code = f"INVALID_{field.upper()}"
        self.message = message or f"Invalid value for '{field}'"


class FileTooLargeError(AppBaseException):
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    code = "FILE_TO_LARGE"

    def __init__(self, limit_mb: int):
        self.message = f"File must be smaller than {limit_mb} MB"
