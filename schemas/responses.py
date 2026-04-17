from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

T = TypeVar('T')

class StandardResponse(BaseModel, Generic[T]):
    success: bool
    data: T
    message: str
    error: Optional[str] = None