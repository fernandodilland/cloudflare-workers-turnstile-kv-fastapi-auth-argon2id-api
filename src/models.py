from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str

class UserData(BaseModel):
    id: str
    username: str
    password_hash: str
    created_at: Optional[str] = None
    last_login: Optional[str] = None
