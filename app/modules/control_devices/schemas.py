from pydantic import BaseModel, Field
from app.common.enums import MotorDirection
class ServoMoveRequest(BaseModel):
    angle: int = Field(gt=0, lt=180)

class MotorMoveRequest(BaseModel):
    direction: MotorDirection
    steps: int = Field(gt=0)
