from jose import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

SECRET_KEY = 'lKaw2pOH7mSqi8'
TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = 'HS256'
pwd_context = CryptContext(schemes=['bcrypt'])

security = HTTPBearer()

def create_token(data: str) -> str:
    payload = {
        "sub": data,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def decode_token(token: str) -> str:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = decode_token(token)
        return payload
    except:
        raise HTTPException(status_code=403, detail="Invalid o expired token")