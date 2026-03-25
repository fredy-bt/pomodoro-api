from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None