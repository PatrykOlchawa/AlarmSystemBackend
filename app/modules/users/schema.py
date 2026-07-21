from datetime import datetime

from pydantic import BaseModel, Field

from app.common.enums import UserRole


username: str = Field(
    min_length=3,
    max_length=30
)

password: str = Field(
    min_length=8,
    max_length=64
)
class UserCreate(BaseModel):
    username: str
    password: str
    pin: str
    role: UserRole


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole
    is_active: bool
    creation_date: datetime

    model_config = {
        "from_attributes": True
    }
    
class UserUpdate(BaseModel):
    username: str
    password: str
    pin: str
    role: UserRole
    is_active: bool
