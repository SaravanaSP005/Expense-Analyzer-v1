from typing import Generic, TypeVar

from pydantic import BaseModel
from typing import Optional

T = TypeVar("T")

class ErrorDetail(BaseModel):
    code: str
    field: Optional[str] = None
    message: str

class APIResponse(BaseModel, Generic[T]):
    success: bool
    statusCode: int
    message: str
    data: Optional[T] = None
    errors: list[ErrorDetail] = []
