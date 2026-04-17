from fastapi import APIRouter, HTTPException, Depends
from schemas.auth import UserAuth, UserCreate, UserResponse, TokenResponse
from db.db_models import User
from db.database import get_db
from sqlalchemy.orm import Session
from utils.auth import create_token, verify_password, hash_password

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/register', status_code=201, response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):

    email = db.query(User).filter(User.email == user_data.email).first()
    if email:
        raise HTTPException(status_code=409, detail="Email is already registered")
    
    db_user = User(
        email=user_data.email,
        password=hash_password(user_data.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = create_token(str(db_user.id))

    return {"email": db_user.email, "access_token": token, "token_type": "bearer"}

@router.post('/login', response_model=TokenResponse)
def login_user(auth_data: UserAuth, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == auth_data.email).first()
    if user is None:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    if not verify_password(auth_data.password, user.password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    token = create_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}