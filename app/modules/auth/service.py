from app.modules.alarms.model import Alarm
from app.core.exceptions import (
    InvalidCredentialsException,
)
from app.modules.users.repository import UserRepository
from app.security.hashing import PasswordHasher
from app.security.jwt_handler import JWTHandler
from app.modules.clients.repository import ClientRepository
from app.modules.clients.service import ClientService
from app.modules.clients.schemas import ClientLoginResponse

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
                "sub": str(user.id),
                "username": user.username,
                "role": user.role.value,
            }
        )

class ClientAuthService:
    def __init__(
        self,
        service: ClientService,
        jwt_handler: JWTHandler,
    ):
        self.service = service
        self.jwt_handler= jwt_handler

    def login(
        self,
        client_id: str,
        secret: str,
    ) -> ClientLoginResponse:
        client = self.service.authenticate(client_id, secret)

        token = self.jwt_handler.create_access_token(
            {
                "sub" : str(client.id),
                "alarm_id" : client.alarm_id,
                "client_id": client.client_id,
                "client_type": client.client_type.value,
            }
        )

        return ClientLoginResponse(
            access_token=token,
            token_type="bearer",
        )