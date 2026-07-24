from datetime import datetime

from pydantic import BaseModel, Field

from app.common.enums import UserRole, AlarmRole

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
    username: str | None = None
    password: str | None = None
    pin: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None

class AlarmMemberResponse(UserBase):
    user_id: int
    alarm_role: AlarmRole
    is_active: bool

