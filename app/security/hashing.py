from app.modules.users.schema import password
from passlib.context import CryptContext

class PasswordHasher:
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["bcrypt"], deprecated="auto"
        )
    
    def hash_password(self, password: str) -> str:
        if not password:
            raise ValueError("Password cannot be empty")
        return self.pwd_context.hash(password)
    
    def verify_password(
        self,
        password: str,
        hashed_password: str
    ) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def hash_pin(self, pin: str) -> str:
        if not pin:
            raise ValueError("PIN cannot be empty")
        return self.pwd_context.hash(pin)

    def verify_pin(
        self,
        pin: str,
        hashed_pin: str
    ) -> bool:
        return self.pwd_context.verify(pin, hashed_pin)


password_hasher = PasswordHasher()

