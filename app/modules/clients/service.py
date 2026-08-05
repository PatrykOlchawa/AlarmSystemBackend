from app.modules.clients.repository import ClientRepository
from app.modules.alarms.model import Alarm
from app.modules.clients.model import Client
from app.core.exceptions import(
    ClientNotFoundException,
    ClientAlreadyExistsException,
    InvalidCredentialsException
)
from app.modules.clients.schemas import (
    ClientUpdate,
    ClientCreate,
    ClientCredentials,
)
from app.security.hashing import password_hasher
import secrets
from app.common.enums import ClientType
from datetime import datetime
import uuid
class ClientService:
    def __init__(
        self,
        repository: ClientRepository,
    ):
        self.repository = repository
        self.password_hasher = password_hasher

    def get_all(
        self,
        alarm: Alarm,
    ) ->list[Client]:
        return self.repository.get_all(alarm)

    def get_by_client_id(
        self,
        client_id: str,
    ) -> Client:
        client = self.repository.get_by_client_id(client_id)
        if client is None:
            raise ClientNotFoundException
        return client

    def create(
        self,
        alarm: Alarm,
        request: ClientCreate,
    ) -> Client:
        exist = self.repository.get_by_client_id(request.client_id)
        if exist:
            raise ClientAlreadyExistsException
        client = Client(
            client_id = request.client_id,
            alarm_id = alarm.id,
            secret_hash = self.password_hasher.hash_password(request.secret),
            client_type = request.client_type,
            enabled = request.enabled,
        )
        return self.repository.create(client)

    def update(
        self,
        client: Client,
        request: ClientUpdate,
    ) -> Client:
        if request.enabled is not None:
            client.enabled = request.enabled
        return self.repository.update(client)

    def delete(
        self,
        client: Client,
    ) -> None:
        self.repository.delete(client)

    def authenticate(
        self,
        client_id: str,
        secret: str,
    ) -> Client:
        client = self.repository.get_by_client_id(client_id)
        if client is None:
            raise InvalidCredentialsException
        if not client.enabled:
            raise InvalidCredentialsException
        if not self.password_hasher.verify_password(secret, client.secret_hash):
            raise InvalidCredentialsException
        return client

    def create_default_client(
        self,
        alarm: Alarm,
    ) -> ClientCredentials:
        client_id = str(uuid.uuid4())
        secret = secrets.token_urlsafe(32)

        client = Client(
            client_id = client_id,
            alarm_id = alarm.id,
            secret_hash = self.password_hasher.hash_password(secret),
            client_type = ClientType.RASPBERRY,
            enabled = True,
        )

        self.repository.create(client)

        return ClientCredentials(
            client_id=client_id,
            secret=secret,
        )