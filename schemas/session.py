from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class SessionType(str, Enum):
    pomodoro = 'pomodoro'
    short_break = 'short break'
    long_break = 'long break'

class SessionCreate(BaseModel):
    task_id: str
    session_type: SessionType
    started_at: datetime
    finished_at: datetime

class SessionUpdate(BaseModel):
    task_id: Optional[str] = None
    session_type: Optional[SessionType] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None