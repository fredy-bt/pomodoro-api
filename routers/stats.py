from fastapi import APIRouter, HTTPException, Depends
from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from schemas.stats import StatsResponse
from db.database import get_db
from db.db_models import Task, SessionModel
from utils.auth import get_current_user
from uuid import UUID

router = APIRouter(prefix='/stats', tags=['stats'])

@router.get('/', response_model=StatsResponse)
def get_stats(
    from_date: date,
    to_date: date,
    task_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
    ):

    minutes: float = 0
    query = db.query(SessionModel).filter(
        SessionModel.user_id == user['sub'],
        SessionModel.started_at >= from_date,
        SessionModel.finished_at <= to_date,
        SessionModel.session_type == "pomodoro"
    )
    
    if task_id:
        db_task = db.query(Task).filter(Task.user_id == user['sub'], Task.id == task_id).first()
        if db_task is None:
            raise HTTPException(status_code=404, detail='Task not found')
        query = query.filter(SessionModel.task_id == task_id)
    
    db_session = query.all()

    for session in db_session:
        lapso = session.finished_at - session.started_at
        minutes += (lapso.total_seconds()) / 60

    return {"total_minutes_studied": minutes, "total_pomodoros_completed": len(db_session)}