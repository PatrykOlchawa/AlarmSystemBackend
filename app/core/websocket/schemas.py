from pydantic import BaseModel
from app.common.enums import MessageEventType
from typing import Any
class WebSocketMessage(BaseModel):
    event: MessageEventType 
    alarm_id: int
    data: dict[str, Any]