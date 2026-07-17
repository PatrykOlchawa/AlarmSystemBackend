from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.common.enums import AlarmEventType

class AlarmEventBase(BaseModel):
    event_type: AlarmEventType

    user_id: int | None = Field(
        default=None,
        gt=-1
    )
    device_id: int | None = Field(
        default=None,
        gt=-1
    )

    location: str | None = Field(
        default=None,
        max_length = 100,
    )

    message: str | None = Field(
        default=None,
        max_length=100,

    )

class AlarmEventCreate(AlarmEventBase):
    pass

class AlarmEventRead(AlarmEventBase):
    id: int
    
    timestamp: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
    
