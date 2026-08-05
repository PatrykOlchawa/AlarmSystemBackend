from pydantic import BaseModel, RootModel
from typing import Any
class MQTTMessage(BaseModel):
    alarm_id: int
    resource: str
    payload: bytes

class CommandPayload(RootModel[dict[str, Any]]):
    pass

class StatePayload(RootModel[dict[str, Any]]):
    pass