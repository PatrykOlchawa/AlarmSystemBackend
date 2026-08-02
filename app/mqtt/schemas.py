from pydantic import BaseModel, RootModel
from typing import Any
from app.common.enums import MQTTMessageType
from datetime import datetime
from typing import Any

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

class StatePayload(RootModel[dict[str, Any]]):
    pass