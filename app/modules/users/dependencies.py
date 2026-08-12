from app.security.hashing import password_hasher
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService
from app.services.websocket_service import WebSocketMessageService
from app.core.websocket.dependencies import get_websocket_service


def get_user_repository(
    db: Session = Depends(get_db),
):
    return UserRepository(db)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
    websocket_service: WebSocketMessageService= Depends(get_websocket_service)
):

    return UserService(
        repository,
        password_hasher,
        websocket_service,
    )