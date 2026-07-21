from app.modules.users.schema import UserUpdate
from app.core.exceptions import UserNotFoundException
from app.security.hashing import PasswordHasher
from app.core.exceptions import UserAlreadyExistsException
from app.modules.users.repository import UserRepository
from app.modules.users.model import User
from app.common.enums import UserRole
from app.security.hashing import password_hasher


class UserService:

    def __init__(self, repository: UserRepository, password_hasher: PasswordHasher):
        self.repository = repository
        self.password_hasher = password_hasher
    
    def create_user(
        self,
        username: str,
        password: str,
        pin: str,
        role: UserRole = UserRole.USER,  
    ) -> User:

        existing = self.repository.get_by_username(username)

        if existing:
            raise UserAlreadyExistsException
        hashed_password = password_hasher.hash_password(password)
        hashed_pin = password_hasher.hash_pin(pin)
        user = User(
            username=username,
            password_hash=hashed_password,
            role=role,
            pin_hash=hashed_pin,
        )
        return self.repository.create(user)
    
    def get_user_by_id(self, user_id: int) -> User | None:
        return self.repository.get_by_id(user_id)
    
    def get_all_users(self):
        return self.repository.get_all()

    def delete_user(
        self,
        user_id: int
    ) -> None:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException
        self.repository.delete(user)
    
    def update_user(
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