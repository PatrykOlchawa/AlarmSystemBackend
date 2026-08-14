from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.modules.notifications.repository import (
    NotificationRepository,
)
from app.modules.notifications.service import (
    NotificationService,
)
from app.core.websocket.dependencies import get_websocket_service
from app.services.websocket_service import WebSocketMessageService

def get_notification_repository(
    db: Session = Depends(get_db),
) -> NotificationRepository:

    return NotificationRepository(db)

def get_notification_service(
    repository: NotificationRepository = Depends(get_notification_repository),
    websocket_service: WebSocketMessageService= Depends(get_websocket_service),
) -> NotificationService:

    return NotificationService(repository, websocket_service)