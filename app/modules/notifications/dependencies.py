from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.modules.notifications.repository import (
    NotificationRepository,
)
from app.modules.notifications.service import (
    NotificationService,
)

def get_notification_repository(
    db: Session = Depends(get_db),
) -> NotificationRepository:

    return NotificationRepository(db)

def get_notification_service(
    repository: NotificationRepository = Depends(
        get_notification_repository
    ),
) -> NotificationService:

    return NotificationService(repository)