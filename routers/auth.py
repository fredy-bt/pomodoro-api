from fastapi import APIRouter, HTTPException
from schemas.user import UserAuth
from models.user import users_db
from utils.auth import create_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/login')
def create_auth(user_auth: UserAuth):
    user = users_db.get(user_auth.email, None)
    if user is None:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    if not verify_password(user_auth.password, user['password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    token = create_token(user['id'])
    return {"access_token": token, "token_type": "bearer"}