from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.common.enums import (
    SensorType,
    SensorStatus,
    ConnectionType,
)

class SensorBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    type: SensorType

    gpio_pin: int | None = Field(
        default=None,
        ge=0,
        le=40,
    )

    #polling_interval: int = Field(
    #    default=1000,
    #    ge=100,
    #    le=60000,
    #)

    enabled: bool = True

class SensorUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )

    type: SensorType | None = None

    gpio_pin: int | None = Field(
        default=None,
        ge=0,
        le=40,
    )

    #polling_interval: int | None = Field(
    #    default=None,
    #    ge=100,
    #    le=60000,
    #)

    enabled: bool | None = None

class SensorRead(SensorBase):
    id: int
    model_config = ConfigDict(
        from_attributes=True
    )

class SensorCreate(SensorBase):
    pass