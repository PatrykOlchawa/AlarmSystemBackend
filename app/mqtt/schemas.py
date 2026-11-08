from pydantic import BaseModel, RootModel, Field
from typing import Any
from app.common.enums import MQTTMessageType
from app.common.enums import AlarmStatus, DeviceCommand, ConfigResourceType

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
    value: float = Field(gt=-1)

class StatePayload(RootModel[dict[str, Any]]):
    pass

class AlarmStatePayload(BaseModel):
    status: AlarmStatus

class DeviceCommandPayload(BaseModel):
    command: DeviceCommand
    params: dict[str, Any] = Field(default_factory=dict)

class ConfigChangedPayload(BaseModel):
    revision: int
    resource: ConfigResourceType