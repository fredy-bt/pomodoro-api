from pydantic import BaseModel, ConfigDict

class UserResponse(BaseModel):
    email: str

    model_config = ConfigDict(from_attributes=True)