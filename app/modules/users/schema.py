from datetime import datetime

from pydantic import BaseModel, Field

from app.common.enums import UserRole

class UserBase(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30
    )

    role: UserRole
class UserCreate(UserBase):
    password: str
    pin: str

class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
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
