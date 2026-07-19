from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class CarPlateBase(BaseModel):
    plate_number: str = Field(
        min_length=1,
        max_length=7,
    )
    owner_name: str | None = Field(
        default=None,
        max_length=50,
    )
    auto_open: bool = False

class CarPlateCreate(CarPlateBase):
    pass
    
class CarPlateUpdate(BaseModel):
    owner_name: str | None = Field(
        default=None,
        max_length=50,

    )

    auto_open: bool | None = None

class CarPlateRead(CarPlateBase):
    id: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes = True
    )