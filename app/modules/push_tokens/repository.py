from sqlalchemy import select
from sqlalchemy.orm import Session
from app.modules.push_tokens.model import PushToken

class PushTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
            self,
            push_token_id: int
        ) -> PushToken | None:
            stmt = (
                select(PushToken)
                .where(PushToken.id == push_token_id)
            )
            return self.db.scalar(stmt)
    
    def get_by_user_id(
        self,
        user_id: int,
    ) -> list[PushToken]:
        stmt = (
            select(PushToken)
            .where(
                PushToken.user_id == user_id,
                PushToken.is_active == True,
            )
        )
        return list(self.db.scalars(stmt).all())

    def get_by_token(
        self,
        token: str,
    ) -> PushToken | None:
        stmt = (
            select(PushToken)
            .where(PushToken.token == token)
        )

        return self.db.scalar(stmt)
    
    def create(
        self,
        push_token: PushToken
    ) -> PushToken:
        self.db.add(push_token)
        self.db.commit()
        self.db.refresh(push_token)
        return push_token

    def delete(
        self,
        push_token: PushToken
    ) -> None:
        self.db.delete(push_token)
        self.db.commit()
    
    def update(
        self,
        push_token: PushToken
    ) -> PushToken:
        self.db.commit()
        self.db.refresh(push_token)
        return push_token    