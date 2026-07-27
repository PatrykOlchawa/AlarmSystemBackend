from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import InvalidTokenException

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

jwt_handler = JWTHandler()