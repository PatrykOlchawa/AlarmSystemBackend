from pydantic import BaseModel, Field

from app.common.enums import NotificationType
from datetime import datetime
from pydantic import ConfigDict

class NotificationBase(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=100,
    )
    message: str = Field(
        min_length=1,
        max_length=255,
    )
    
    user_id: int | None = Field(
        gt=-1
    )

    is_read: bool = False

    notification_type: NotificationType

    alarm_id: int

class NotificationCreate(NotificationBase):
    pass

class NotificationRead(NotificationBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

#For updating notification status - read/unread
class NotificationUpdate(BaseModel):
    is_read: bool