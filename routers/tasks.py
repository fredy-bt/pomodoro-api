from fastapi import APIRouter, HTTPException, Depends
from models.task import Task, tasks_db
from schemas.task import  TaskCreate, TaskUpdate
from utils.responses import success_response
from utils.auth import get_current_user
import uuid

router = APIRouter(prefix='/tasks', tags=["tasks"])

@router.get('/')
def get_tasks():
    tasks = [task.to_dict() for task in tasks_db.values()]
    return success_response(data=tasks)

@router.get('/{task_id}')
def get_task(task_id: str):
    task = tasks_db.get(task_id, None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return success_response(data=task.to_dict())

@router.post('/', status_code=201)
def post_task(task_create: TaskCreate):
    id = str(uuid.uuid4())
    new_task = Task(id, task_create.name, task_create.description)
    tasks_db[id] = new_task
    return success_response(data=new_task.to_dict())

@router.put('/{task_id}')
def update_task(task_id: str, update_task: TaskCreate):
    task = tasks_db.get(task_id, None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_updated = Task(task_id, update_task.name, update_task.description)
    tasks_db[task_id] = task_updated
    return success_response(data=task_updated.to_dict())

@router.patch('/{task_id}')
def patch_task(task_id: str, patch_task: TaskUpdate):
    task = tasks_db.get(task_id, None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    patch = patch_task.model_dump(exclude_unset=True)
    if patch == {}:
        raise HTTPException(status_code=400, detail="No fields provided to patch")
    task_dict = task.to_dict()

    for k, v in patch.items(): 
        task_dict[k] = v
    task_patched = Task(task_id, task_dict["name"], task_dict["description"])
    tasks_db[task_id] = task_patched
    return success_response(data=task_patched.to_dict())

@router.delete('/{task_id}', status_code=204)
def remove_task(task_id: str, user=Depends(get_current_user)):
    task = tasks_db.pop(task_id, None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")