from pydantic import BaseModel, RootModel
from typing import Any
from app.common.enums import MQTTMessageType
from app.common.enums import AlarmStatus 
class SensorMessage(BaseModel):
    value: Any

class PIRMessage(BaseModel):
    motion: bool

class MQTTMessage(BaseModel):
    alarm_id: int
    message_type: MQTTMessageType
    resource_type: str | None = None
    resource_id: int | None = None 
    payload: bytes

class SensorPayload(BaseModel):
    value: bool | int | float | str

class StatePayload(RootModel[dict[str, Any]]):
    pass

class AlarmStatePayload(BaseModel):
    status: AlarmStatus