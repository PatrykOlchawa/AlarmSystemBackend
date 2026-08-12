from app.modules.users.schema import (
    UserUpdate,
    AlarmMemberResponse,
    UserCreate,
    ChangePassword,
)
from app.core.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    InvalidCredentialsException,
    WebsocketException,
) 
from app.security.hashing import PasswordHasher
from app.security.hashing import password_hasher
from app.modules.users.repository import UserRepository
from app.modules.users.model import User
from app.common.enums import MessageEventType
from app.services.websocket_service import WebSocketMessageService
class UserService:

    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
        websocket_service: WebSocketMessageService,
        ):
        self.repository = repository
        self.password_hasher = password_hasher
        self.websocket_service = websocket_service

    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:

        return self.repository.get_by_id(user_id)
    
    def get_all_users(
        self,
    ):
        return self.repository.get_all()

    def get_users_by_alarm(
        self,
        alarm_id:int,
    ) -> list[AlarmMemberResponse] | None:
        return self.repository.get_users_by_alarm(alarm_id)

    def create(
        self,
        request: UserCreate,
    ) -> User:

        existing = self.repository.get_by_username(request.username)

        if existing:
            raise UserAlreadyExistsException
        hashed_password = password_hasher.hash_password(request.password)

        user = User(
            username = request.username,
            role = request.role,
            password_hash = hashed_password,
        )
        user = self.repository.create(user)
        self._notify_users_changed()
        return user

    def delete(
        self,
        user_id: int
    ) -> None:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException
        self.repository.delete(user)
        self._notify_users_changed()
    
    def update(
        self,
        user_id: int,
        request: UserUpdate
    ) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException
        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
    
        user = self.repository.update(user)
        self._notify_users_changed()
        return user


    def change_password(
        self,
        user: User,
        request: ChangePassword,
    ) -> User:
        if not self.password_hasher.verify_pin(request.old_password, user.password_hash):
            raise InvalidCredentialsException
        user.password_hash = self.password_hasher.hash_password(request.new_password)
        self.repository.update(user)
        return user


    def _notify_users_changed(
        self,
    ) -> None:
        try:
            admin_ids = self.repository.get_global_admins()

            self.websocket_service.send_message_to_admins_sync(
                admin_ids=admin_ids,
                event_type=MessageEventType.USERS_CHANGED,
                data={},
            )
        except Exception:
            raise WebsocketException    