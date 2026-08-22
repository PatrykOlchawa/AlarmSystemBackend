from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import InvalidTokenException
from pathlib import Path
class JWTHandler:

    def create_access_token(
        self,
        data: dict,
    ) -> str:

        to_encode = data.copy()

        expire = datetime.now(UTC) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

        to_encode.update(
            {
                "exp": expire,
                "type":"access"
            }
        )

        return jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
        )

    def decode_access_token(
        self,
        token: str,
    ) -> dict:

        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
    def verify_access_token(
        self,
        token: str,
    ) -> dict:

        try:
            payload = self.decode_access_token(token)

        except JWTError:
            raise InvalidTokenException()

        if "sub" not in payload:
            raise InvalidTokenException()

        if payload.get("type") != "access":
            raise InvalidTokenException()
        return payload

    def get_user_id(
        self,
        token: str,
    ) -> int:
        payload = self.verify_access_token(token)

        return int(payload["sub"])

    def get_payload(
        self,
        token: str,
    ) -> dict:
        return self.verify_access_token(token)

#MediaMTX

    def create_mediamtx_token(
        self,
        permissions: list[dict],
    ) -> str:
        now = datetime.now(UTC)

        expire = now + timedelta(
            minutes=settings.mediamtx_token_expire_minutes
        )

        payload = {
            "iss": settings.mediamtx_token_issuer,
            "aud": settings.mediamtx_token_audience,
            "iat": now,
            "exp": expire,
            "mediamtx_permissions": permissions,
        }
        private_key = Path(
            settings.mediamtx_private_key_path
        ).read_text()
        return jwt.encode(
            payload,
            private_key,
            algorithm="ES256",
            headers={
                "kid": settings.mediamtx_key_id,
            },
        )

jwt_handler = JWTHandler()