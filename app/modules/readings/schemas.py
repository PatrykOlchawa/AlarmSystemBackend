from pydantic import ConfigDict
from app.modules.events import model
from datetime import datetime

from pydantic import BaseModel, Field

class SensorReadingBase(BaseModel):
    value: float = Field(
        gt=-1
    )

class SensorReadingCreate(SensorReadingBase):
    pass

class SensorReadingRead(SensorReadingBase):
    id: int
    timestamp: datetime
    model_config = ConfigDict(
        from_attributes=True
    )