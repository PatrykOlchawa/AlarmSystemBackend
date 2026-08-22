import base64

from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
)
from app.core.config import settings
from app.modules.devices.model import Device
from app.modules.alarms.model import Alarm
from app.security.jwt_handler import jwt_handler
class MediaAuthService:
    def __init__(
        self,
        private_key_path: str,
        key_id: str,
    ):
        self.key_id = key_id

        with open(private_key_path, "rb") as file:
            self._private_key = load_pem_private_key(
                file.read(),
                password=None,
            )

        if not isinstance(
            self._private_key.public_key(),
            EllipticCurvePublicKey,
        ):
            raise ValueError(
                "MediaMTX private key must be EC key"
            )

    @staticmethod
    def _base64url(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

    def get_camera_path(
        self,
        alarm: Alarm,
        camera: Device,
    ) -> str:
        return (
            f"alarm-{alarm.id}-"
            f"{camera.connection_identifier}"
        )
    
    def get_jwks(self) -> dict:
        public_key = self._private_key.public_key()

        if not isinstance(
            public_key,
            EllipticCurvePublicKey,
        ):
            raise ValueError(
                "MediaMTX public key must be an EC key"
            )
        numbers = public_key.public_numbers()
        x = numbers.x.to_bytes(32, byteorder="big")
        y = numbers.y.to_bytes(32, byteorder="big")

        return {
            "keys": [
                {
                    "kty": "EC",
                    "use": "sig",
                    "alg": "ES256",
                    "kid": self.key_id,
                    "crv": "P-256",
                    "x": self._base64url(x),
                    "y": self._base64url(y),
                }
            ]
        }

    def create_camera_permissions(
        self,
        alarm: Alarm,
        cameras: list[Device],
    ) -> list[dict]:

        return [
            {
                "action": "read",
                "path": self.get_camera_path(
                    alarm=alarm,
                    camera=camera,
                ),
            }
            for camera in cameras
        ]
    
    def create_camera_stream_token(
        self,
        permissions: list[dict],
    ) -> str:
        return jwt_handler.create_mediamtx_token(
            permissions=permissions,
        )
    
media_auth_service = MediaAuthService(
    private_key_path=settings.mediamtx_private_key_path,
    key_id=settings.mediamtx_key_id,
)