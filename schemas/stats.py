from pydantic import BaseModel

class StatsResponse(BaseModel):
    total_minutes_studied: float
    total_pomodoros_completed: int