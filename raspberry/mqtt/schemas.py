from pydantic import BaseModel, RootModel
from typing import Any
from app.common.enums import MQTTMessageType
class MQTTMessage(BaseModel):
    alarm_id: int
    message_type: MQTTMessageType
    resource_type: str | None = None
    resource_id: int | None = None 
    payload: bytes

class CommandPayload(RootModel[dict[str, Any]]):
    pass

class StatePayload(RootModel[dict[str, Any]]):
    pass