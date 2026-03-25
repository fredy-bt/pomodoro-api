from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from utils.responses import error_response
from routers.tasks import router as tasks_router
from routers.sessions import router as sessions_router
from routers.stats import router as stats_router
from routers.auth import router as auth_router

from models.task import tasks_db, Task
from models.session import sessions_db, Session
from datetime import datetime

app = FastAPI(
    title="Pomodoro Tracker",
    description="API to track study sessions",
    version="1.0.0"
)

app.include_router(tasks_router)
app.include_router(sessions_router)
app.include_router(stats_router)
app.include_router(auth_router)

@app.get('/health')
def health_check():
    return {"status": "ok"}

@app.exception_handler(HTTPException)
async def exception_handler_http(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(message=exc.detail)
    )

@app.exception_handler(RequestValidationError)
async def exception_handler_request(request: Request, exc:RequestValidationError):
    errors = [
        {"field": e['loc'][-1], "message": e['msg']}
        for e in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content=error_response(message="UNPROCESSABLE_ENTITY", error=errors)    
    )

tasks_db['Task-1'] = Task('Task-1', 'ANKI', 'Study ANKI cards')
tasks_db['Task-2'] = Task('Task-2', 'FastAPI', 'FastAPI core')

sessions_db['Session-1'] = Session(
    'Session-1', 'Task-1', 'pomodoro',
    datetime(2026, 3, 18, 16, 00, 00),
    datetime(2026, 3, 18, 16, 25, 00)
)

sessions_db['Session-2'] = Session(
    'Session-2', 'Task-2', 'pomodoro',
    datetime(2026, 3, 18, 18, 0, 0),
    datetime(2026, 3, 18, 18, 25, 0)
)

sessions_db['Session-3'] = Session(
    'Session-3', 'Task-2', 'pomodoro',
    datetime(2026, 3, 18, 20, 0, 0),
    datetime(2026, 3, 18, 20, 25, 0)
)