from jose import jwt

from app.core.config import settings
from app.security.jwt_handler import jwt_handler


permissions = [
    {
        "action": "read",
        "path": "alarm-4-camera-1",
    }
]


token = jwt_handler.create_mediamtx_token(
    permissions=permissions,
)

print("\nTOKEN:")
print(token)

print("\nPAYLOAD:")

payload = jwt.get_unverified_claims(token)

print(payload)