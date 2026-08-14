from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.push_tokens.service import PushTokenService
from app.modules.push_tokens.repository import PushTokenRepository


def get_push_token_repository(
    db: Session = Depends(get_db),
):
    return PushTokenRepository(db)


def get_push_token_service(
    repository: PushTokenRepository = Depends(get_push_token_repository),
):
    return PushTokenService(repository)