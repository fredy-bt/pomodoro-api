from fastapi import APIRouter, HTTPException, Depends
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from schemas.responses import StandardResponse
from utils.responses import success_response
from utils.auth import get_current_user
from uuid import UUID
from sqlalchemy.orm import Session
from db.database import get_db
from db.db_models import Task

router = APIRouter(prefix='/tasks', tags=["tasks"])

@router.get('/', response_model=StandardResponse[list[TaskResponse]])
def get_tasks(db: Session = Depends(get_db), user = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.user_id == user['sub']).all()
    return success_response(data=[TaskResponse.model_validate(t).model_dump() for t in tasks])

@router.get('/{task_id}', response_model=StandardResponse[TaskResponse])
def get_task(task_id: UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.user_id == user['sub'], Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return success_response(data=TaskResponse.model_validate(db_task).model_dump())

@router.post('/', status_code=201, response_model=StandardResponse[TaskResponse])
def post_task(task: TaskCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    db_task = Task(user_id=user['sub'],name=task.name, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return success_response(data=TaskResponse.model_validate(db_task).model_dump())

@router.put('/{task_id}', response_model=StandardResponse[TaskResponse])
def update_task(task_id: UUID, task_data: TaskCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.user_id == user['sub'], Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.name = task_data.name
    db_task.description = task_data.description
    db.commit()
    db.refresh(db_task)
    return success_response(data=TaskResponse.model_validate(db_task).model_dump())

@router.patch('/{task_id}', response_model=StandardResponse[TaskResponse])
def patch_task(task_id: UUID, task_data: TaskUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.user_id == user['sub'], Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    patch = task_data.model_dump(exclude_unset=True)
    if patch == {}:
        raise HTTPException(status_code=400, detail="No fields provided to patch")
    
    for k, v in patch.items():
        setattr(db_task, k, v)

    db.commit()
    db.refresh(db_task)

    return success_response(data=TaskResponse.model_validate(db_task).model_dump())

@router.delete('/{task_id}', status_code=204)
def remove_task(task_id: UUID, db: Session = Depends(get_db), user = Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.user_id == user['sub'], Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()