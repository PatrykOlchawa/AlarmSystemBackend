from app.db.base import Base
from pydantic import BaseModel, ConfigDict, Field

# pyrefly: ignore [missing-import]
from app.common.enums import ConnectionType
from app.common.enums import DeviceType

class DeviceBase(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    connection_type: ConnectionType
    connection_identifier: str = Field(min_length=1, max_length=50)
    type: DeviceType
    location: str | None = Field(default=None, max_length=256)
    enabled: bool = True

    model_config = ConfigDict(from_attributes=True)


class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=128)
    connection_type: ConnectionType | None = None
    connection_identifier: str | None = Field(default=None, min_length=1, max_length=50)
    type: DeviceType | None = None
    location: str | None = Field(default=None, max_length=256)
    enabled: bool | None = None

class DeviceResponse(BaseModel):
    id: int
    name: str
    connection_type: ConnectionType
    connection_identifier: str
    type: DeviceType
    location: str | None = None
    enabled: bool

    model_config = ConfigDict(from_attributes=True)


