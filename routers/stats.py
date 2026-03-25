from fastapi import APIRouter, HTTPException
from utils.responses import success_response
from datetime import date
from typing import Optional
from models.session import sessions_db
from models.task import tasks_db

router = APIRouter(prefix='/stats', tags=['stats'])

@router.get('/')
def get_stats(from_date: date, to_date: date, task_id: Optional[str] = None):
    pomodoro = 0
    minutes = 0

    if task_id is not None:
        task = tasks_db.get(task_id, None)
        if task is None:
            raise HTTPException(status_code=404, detail='Task not found')

    for session in sessions_db.values():
        if session.started_at.date() >= from_date and session.finished_at.date() <= to_date and session.session_type == 'pomodoro':
            if task_id is not None and session.task_id != task_id:
                continue

            pomodoro += 1
            lapso = session.finished_at - session.started_at
            minutes += (lapso.total_seconds()) / 60

    stats = {"total_minutes_studied": minutes, "total_pomodoros_completed": pomodoro}
    return success_response(data=stats)