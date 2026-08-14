from pydantic import BaseModel, Field
from datetime import datetime
from app.common.enums import (
    PushLocale,
    PushPlatform,
)
class PushTokenRequest(BaseModel):
    token: str = Field(
        min_length=1,
        max_length=255,
    )
    platform: PushPlatform
    locale: PushLocale
    device_id: str

class PushTokenResponse(BaseModel):
    id: int
    token: str
    platform: PushPlatform
    is_active: bool
    created_at: datetime
    updated_at: datetime
    locale: PushLocale
    device_id: str
    
    model_config = {
        "from_attributes": True
    }