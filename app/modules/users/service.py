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
) 
from app.security.hashing import PasswordHasher
from app.security.hashing import password_hasher
from app.modules.users.repository import UserRepository
from app.modules.users.model import User

class UserService:

    def __init__(self, repository: UserRepository, password_hasher: PasswordHasher):
        self.repository = repository
        self.password_hasher = password_hasher
    
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
        return self.repository.create(user)
    
    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:

        return self.repository.get_by_id(user_id)
    
    def get_all_users(
        self,
    ):
        return self.repository.get_all()
    

    def delete(
        self,
        user_id: int
    ) -> None:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException
        self.repository.delete(user)
    
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
    
        return self.repository.update(user)

    def get_users_by_alarm(
        self,
        alarm_id:int,
    ) -> list[AlarmMemberResponse] | None:
        return self.repository.get_users_by_alarm(alarm_id)

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


        