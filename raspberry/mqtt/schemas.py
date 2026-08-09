from pydantic import BaseModel, RootModel
from typing import Any
from common.enums import AlarmStatus
from common.enums import MQTTMessageType
class MQTTMessage(BaseModel):
    alarm_id: int
    message_type: MQTTMessageType
    resource_type: str | None = None
    resource_id: int | None = None 
    payload: bytes

class AlarmCommandPayload(BaseModel):
    armed: bool

class DeviceCommandPayload(RootModel[dict[str, Any]]):
    pass

class AlarmStatePayload(BaseModel):
    status: AlarmStatus

class DeviceStatePayload(RootModel[dict[str, Any]]):
    pass