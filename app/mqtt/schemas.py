from pydantic import BaseModel
from typing import Any
from app.common.enums import MQTTMessageType
from datetime import datetime
class SensorMessage(BaseModel):
    value: Any

class PIRMessage(BaseModel):
    motion: bool

class MQTTMessage(BaseModel):
    alarm_id: int
    message_type: MQTTMessageType
    resource: str | None = None
    payload: bytes

class SensorPayload(BaseModel):
    value: bool | int | float | str
    timestamp: datetime

