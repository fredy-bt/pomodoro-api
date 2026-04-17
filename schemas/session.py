from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime
from uuid import UUID

class SessionType(str, Enum):
    pomodoro = 'pomodoro'
    short_break = 'short break'
    long_break = 'long break'

class SessionCreate(BaseModel):
    task_id: Optional[UUID] = None
    session_type: SessionType
    started_at: datetime
    finished_at: datetime

class SessionUpdate(BaseModel):
    task_id: Optional[UUID] = None
    session_type: Optional[SessionType] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

class SessionResponse(BaseModel):
    id: UUID
    task_id: Optional[UUID] = None
    session_type: SessionType
    started_at: datetime
    finished_at: datetime

    model_config = ConfigDict(from_attributes=True)