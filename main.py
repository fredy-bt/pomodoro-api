from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from utils.responses import error_response
from routers.tasks import router as tasks_router
from routers.sessions import router as sessions_router
from routers.stats import router as stats_router
from routers.auth import router as auth_router
from routers.users import r as users_router
from db.database import Base, engine

app = FastAPI(
    title="Pomodoro Tracker",
    description="API to track study sessions",
    version="1.0.0"
)

app.include_router(tasks_router)
app.include_router(sessions_router)
app.include_router(stats_router)
app.include_router(auth_router)
app.include_router(users_router)

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

Base.metadata.create_all(bind=engine)