from pydantic import BaseModel, Field

from app.common.enums import AlarmStatus


class AlarmStatusResponse(BaseModel):
    status: AlarmStatus

class AlarmMessageResponse(BaseModel):
    message: str

class AlarmPinRequest(BaseModel):
    pin: str = Field(
        min_length=4,
        max_length=10,
    )
