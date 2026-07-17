from fastapi import Depends

from app.modules.users.dependencies import (
    get_user_repository,
)
from app.modules.users.repository import UserRepository

from app.security.hashing import (
    password_hasher,
    PasswordHasher,
)
from app.security.jwt_handler import (
    jwt_handler,
    JWTHandler,
)

from app.modules.auth.service import AuthService


def get_password_hasher() -> PasswordHasher:
    return password_hasher


def get_jwt_handler() -> JWTHandler:
    return jwt_handler


def get_auth_service(
    repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
) -> AuthService:

    return AuthService(
        repository,
        password_hasher,
        jwt_handler,
    )
