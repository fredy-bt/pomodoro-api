from fastapi import APIRouter, HTTPException, Depends
from models.session import sessions_db, Session
from models.task import tasks_db
from schemas.session import SessionCreate, SessionUpdate
from utils.responses import success_response
from utils.auth import get_current_user
import uuid

router = APIRouter(prefix='/sessions', tags=["sessions"])

@router.get('/')
def get_sessions():
    sessions = [s.to_dict() for s in sessions_db.values()]
    return success_response(data=sessions)

@router.get('/{session_id}')
def get_session(session_id: str):
    session = sessions_db.get(session_id, None)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return success_response(data=session.to_dict())

@router.post('/', status_code=201)
def post_session(create_session: SessionCreate):
    task = tasks_db.get(create_session.task_id, None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    id = str(uuid.uuid4()) 

    new_session = Session(id, create_session.task_id, create_session.session_type, create_session.started_at, create_session.finished_at)
    sessions_db[id] = new_session

    return success_response(data=new_session.to_dict())

@router.put('/{session_id}')
def update_session(session_id: str, update: SessionCreate):
    session = sessions_db.get(session_id, None)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    task = tasks_db.get(update.task_id, None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    new_session = Session(
        session_id,
        update.task_id,
        update.session_type,
        update.started_at,
        update.finished_at
    )

    sessions_db[session_id] = new_session
    return success_response(data=new_session.to_dict())

@router.patch('/{session_id}')
def patch_session(session_id: str, update: SessionUpdate):
    session_obj = sessions_db.get(session_id, None)
    if session_obj is None:
        raise HTTPException(status_code=404, detail="Session not found")

    patch = update.model_dump(exclude_unset=True)
    if patch == {}:
        raise HTTPException(status_code=400, detail="No fields provided to patch")

    x = patch.get("task_id", "does_not_exist")
    if x != "does_not_exist" and x is not None:
        y = tasks_db.get(x, None)
        if y is None:
            raise HTTPException(status_code=404, detail="Task not found")

    if "task_id" in patch:
        session_obj.task_id = patch["task_id"]
    if "session_type" in patch:
        session_obj.session_type = patch["session_type"]
    if "started_at" in patch:
        session_obj.started_at = patch["started_at"]
    if "finished_at" in patch:
        session_obj.finished_at = patch["finished_at"]

    sessions_db[session_id] = session_obj
    return success_response(data=session_obj.to_dict())

@router.delete('/{session_id}', status_code=204)
def remove_session(session_id: str, user=Depends(get_current_user)):
    session = sessions_db.pop(session_id, None)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")