from pydantic import BaseModel, Field
from app.common.enums import UserRole, ClientType

class LoginRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
    )

    password: str = Field(
        min_length=8,
        max_length=64,
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    username: str
    role: UserRole

class ClientTokenPayload(BaseModel):
    sub: str
    alarm_id: int
    client_id: str
    client_type: ClientType