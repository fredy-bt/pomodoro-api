from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.db_models import User
from schemas.users import UserResponse
from utils.auth import get_current_user

r = APIRouter(prefix='/users', tags=['users'])

@r.get('/me', response_model=UserResponse)
def profile(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user['sub']).first()
    return {"email": user.email}