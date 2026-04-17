from fastapi import APIRouter, HTTPException, Depends
from schemas.session import SessionCreate, SessionUpdate, SessionResponse
from schemas.responses import StandardResponse
from utils.responses import success_response
from utils.auth import get_current_user
from db.db_models import SessionModel, Task
from db.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter(prefix='/sessions', tags=["sessions"])

@router.get('/', response_model=StandardResponse[list[SessionResponse]])
def get_sessions(db: Session = Depends(get_db), user = Depends(get_current_user)):
    sessions = db.query(SessionModel).filter(SessionModel.user_id == user['sub']).all()
    return success_response(data=[SessionResponse.model_validate(s).model_dump() for s in sessions])

@router.get('/{session_id}', response_model=StandardResponse[SessionResponse])
def get_session(session_id: UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    db_session = db.query(SessionModel).filter(SessionModel.user_id == user['sub'], SessionModel.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return success_response(data=SessionResponse.model_validate(db_session).model_dump())

@router.post('/', status_code=201, response_model=StandardResponse[SessionResponse])
def post_session(session: SessionCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if session.task_id:
        task = db.query(Task).filter(Task.user_id == user['sub'], Task.id == session.task_id).first()
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
    
    db_sessions = SessionModel(
        task_id=session.task_id,
        user_id=user['sub'],
        session_type=session.session_type,
        started_at=session.started_at,
        finished_at=session.finished_at
    )
    db.add(db_sessions)
    db.commit()
    db.refresh(db_sessions)

    return success_response(data=SessionResponse.model_validate(db_sessions).model_dump())

@router.put('/{session_id}', response_model=StandardResponse[SessionResponse])
def update_session(session_id: UUID, session_data: SessionCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    db_session = db.query(SessionModel).filter(SessionModel.user_id == user['sub'], SessionModel.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session_data.task_id:
        task = db.query(Task).filter(Task.user_id == user['sub'], Task.id == session_data.task_id).first()
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
    
    db_session.task_id = session_data.task_id
    db_session.session_type = session_data.session_type
    db_session.started_at = session_data.started_at
    db_session.finished_at = session_data.finished_at
    db.commit()
    db.refresh(db_session)
    
    return success_response(data=SessionResponse.model_validate(db_session).model_dump())

@router.patch('/{session_id}', response_model=StandardResponse[SessionResponse])
def patch_session(session_id: UUID, session_data: SessionUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    db_session = db.query(SessionModel).filter(SessionModel.user_id == user['sub'], SessionModel.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session_data.task_id:
        task = db.query(Task).filter(Task.user_id == user['sub'], Task.id == session_data.task_id).first()
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

    patch = session_data.model_dump(exclude_unset=True)
    if patch == {}:
        raise HTTPException(status_code=400, detail="No fields provided to patch")

    for k, v in patch.items():
        setattr(db_session, k, v)
    db.commit()
    db.refresh(db_session)

    return success_response(data=SessionResponse.model_validate(db_session).model_dump())

@router.delete('/{session_id}', status_code=204)
def remove_session(session_id: UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    db_session = db.query(SessionModel).filter(SessionModel.user_id == user['sub'], SessionModel.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(db_session)
    db.commit()