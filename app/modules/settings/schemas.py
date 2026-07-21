from pydantic import ConfigDict
from pydantic import BaseModel, Field


class SettingBase(BaseModel):

    key: str = Field(
        min_length=1,
        max_length=100,
    )

    value: str = Field(
        min_length=1,
        max_length=255,
    )
class SettingCreate(SettingBase):
    pass

class SettingRead(SettingBase):
    id: int
    model_config = ConfigDict(
        from_attributes=True,
    )

class SettingUpdate(BaseModel):
    value:str = Field(
        min_length=1,
        max_length=255,
    )