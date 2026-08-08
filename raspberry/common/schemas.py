from pydantic import (
    BaseModel,
    ConfigDict,
)
from common.enums import (
    AlarmStatus,
    SensorType,
    DeviceType,
)
class AlarmConfig(BaseModel):
    id: int
    name: str
    status: AlarmStatus
    is_active: bool

    
class SettingConfig(BaseModel):
    id: int
    key: str
    value: bool | int | float | str | None
    
class DeviceConfig(BaseModel):
    id: int
    name: str
    type: DeviceType
    connection_identifier: str
    enabled: bool
    status: dict | None 
    model_config = ConfigDict(from_attributes=True)

class SensorConfig(BaseModel):
    id: int
    name: str
    type: SensorType
    gpio_pin: int
    enabled: bool
    model_config = ConfigDict(from_attributes=True)

class ConfigResponse(BaseModel):
    alarm: AlarmConfig
    settings: list[SettingConfig]
    devices: list[DeviceConfig]
    sensors: list[SensorConfig]

class AlarmCommandPayload(BaseModel):
    armed: bool    