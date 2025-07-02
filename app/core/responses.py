from pydantic import BaseModel
from typing import Generic, TypeVar, Optional


T = TypeVar("T")


class ErrorResponse(BaseModel):
    code: int
    message: str


class BaseApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    error: Optional[ErrorResponse] = None

    @classmethod
    def ok(cls, data: Optional[T], message: str = "OK") -> "BaseApiResponse[T]":
        return cls(success=True, message=message, data=data)

    @classmethod
    def fail(cls, code: int, message: str) -> "BaseApiResponse[None]":
        return cls(
            success=False,
            message=message,
            data=None,
            error=ErrorResponse(code=code, message=message),
        )
