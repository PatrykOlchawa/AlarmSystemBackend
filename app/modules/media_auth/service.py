import base64

from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
)
from app.core.config import settings
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


media_auth_service = MediaAuthService(
    private_key_path=settings.mediamtx_private_key_path,
    key_id=settings.mediamtx_key_id,
)