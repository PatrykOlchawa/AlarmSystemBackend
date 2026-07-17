from app.core.exceptions import (
    InvalidCredentialsException,
)
from app.modules.users.repository import UserRepository
from app.security.hashing import PasswordHasher
from app.security.jwt_handler import JWTHandler


class AuthService:

    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
        jwt_handler: JWTHandler,
    ):
        self.repository = repository
        self.password_hasher = password_hasher
        self.jwt_handler = jwt_handler

    def login(
        self,
        username: str,
        password: str,
    ) -> str:

        user = self.repository.get_by_username(username)

        if user is None:
            raise InvalidCredentialsException()

        if not self.password_hasher.verify_password(
            password,
            user.password_hash,
        ):
            raise InvalidCredentialsException()

        return self.jwt_handler.create_access_token(
            {
                "sub": user.username,
                "user_id": user.id,
                "role": user.role.value,
            }
        )
    