from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)