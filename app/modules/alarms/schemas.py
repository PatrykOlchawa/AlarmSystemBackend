from app.common.enums import AlarmStatus
from app.db.base import Base
from pydantic import BaseModel, ConfigDict, Field

class AlarmBase(BaseModel):
    name: str = Field(min_length=1, max_length=128)

class AlarmCreate(AlarmBase):
    pass

class AlarmUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=128)
    is_active: bool | None = None

class AlarmResponse(BaseModel):
    id: int
    name: str
    status: AlarmStatus
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
    
