from pydantic import BaseModel, Field
from datetime import datetime
class PushTokenRequest(BaseModel):
    token: str = Field(
        min_length=1,
        max_length=255,
    )
    platform: str = Field(
        min_length=1,
        max_length=128,
    )

class PushTokenResponse(BaseModel):
    id: int
    token: str
    platform: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }