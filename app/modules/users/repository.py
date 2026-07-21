from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.users.model import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return self.db.scalar(stmt)

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.db.scalar(stmt)

    def get_all(self) -> list[User]:
        stmt = select(User)
        return list(self.db.scalars(stmt).all())
    
    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
    
    def update(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user