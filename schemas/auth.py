from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserAuth(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    email: str
    token: TokenResponse

    model_config = ConfigDict(from_attributes=True)