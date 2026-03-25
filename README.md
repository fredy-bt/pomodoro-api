# Pomodoro Tracker

REST API to track study sessions using the Pomodoro technique.  
Built with FastAPI and Python.

## Setup

1. Clone the repository  
git clone `<tu-url>`  
dc pomodoro-api

2. Create and active virtual environment  
python -m venv venv  
venv\Scripts\activate #Windows  
source venv/bin/activate #Mac/Linux  

3. Install dependencies  
pip install -r requirements.txt

4. Run the server  
uvicorn main:app --reload

5. Open the interactive docs  
http://127.0.0.1:8000/docs

## Authentication   
Some endpoints require a JWT token. Use POST /auth/login  
with your credentials to get a token, then click "Authorize"  
in /docs and paste it.

## Endpoints

### Tasks
`GET /tasks/` - list all tasks  
`GET /tasks/{id}` - get a task  
`POST /tasks/` - create a task  
`PUT /tasks/{id}` - replace a task  
`PATCH /tasks/{id}` - update fields  
`DELETE /tasks/{id}` - delete a task 🔒  

### Sessions
`GET /sessions/` - list all sessions   
`GET /sessions/{id}` - get a session  
`POST /sessions/` - create a session  
`PUT /sessions/{id}` - replace a session  
`PATCH /sessions/{id}` - update fields  
`DELETE /sessions/{id}` - delete a session 🔒  

### Stats
`GET /stats/` - get study statistics  
Query params: from_date, to_date, task_id (optional)

### Auth
`POST /auth/login/` - get JWT token