from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from app.core.config import settings


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
                "exp": expire
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


jwt_handler = JWTHandler()