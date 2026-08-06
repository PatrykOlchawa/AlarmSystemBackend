from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)
from datetime import datetime
from app.common.enums import ClientType
from app.modules.settings.schemas import SettingConfig
from app.modules.sensors.schemas import SensorConfig
from app.modules.devices.schemas import DeviceConfig
from app.modules.alarms.schemas import AlarmResponse 



class ClientBase(BaseModel):
    client_id: str = Field(
        min_length=1,
        max_length=128,
    )

    client_type: ClientType

    enabled: bool = True

    model_config = ConfigDict(
        from_attributes=True,
    )

class ClientCreate(ClientBase):
    secret: str = Field(
        min_length=1,
        max_length=255,
    )

class ClientUpdate(BaseModel):
    enabled: bool

class ClientResponse(BaseModel):
    id: int

    alarm_id: int

    client_id: str

    client_type: ClientType

    enabled: bool

    model_config = ConfigDict(
        from_attributes=True,
    )

class ClientLoginRequest(BaseModel):
    client_id: str
    secret: str

class ClientLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ClientCredentials(BaseModel):
    client_id: str
    secret: str

class ConfigResponse(BaseModel):
    alarm: AlarmResponse
    settings: list[SettingConfig]
    devices: list[DeviceConfig]
    sensors: list[SensorConfig]

class AlarmCreateResponse(BaseModel):
    alarm: AlarmResponse
    raspberry: ClientCredentials