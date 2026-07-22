from app.security.authorization_dependencies import require_alarm_admin
from app.modules.alarms.model import Alarm
from app.security.auth_dependencies import get_current_user
from app.modules.users.model import User
from fastapi import APIRouter, Depends, status

from app.modules.notifications.dependencies import (
    get_notification_service,
)

from app.modules.notifications.schemas import (
    NotificationCreate,
    NotificationRead,
    NotificationUpdate,
)

from app.modules.notifications.service import (
    NotificationService,
)

router = APIRouter(
    prefix="/alarms/{alarm_id}/notifications",
    tags=["Notifications"],
)

@router.get(
    "",
    response_model= list[NotificationRead]
)
def get_all_notifications(
    service: NotificationService = Depends(get_notification_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_all(alarm)

@router.get(
    "/user/{user_id}",
    response_model=list[NotificationRead],
)
def get_notification(
    user_id: int,
    service: NotificationService = Depends(get_notification_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_by_user(alarm, user_id)

@router.get(
    "/user/{user_id}/unread",
    response_model=list[NotificationRead],
)
def get_unread_notification(
    user_id: int,
    service: NotificationService = Depends(get_notification_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_unread_by_user(alarm, user_id)

@router.get(
    "/user/{user_id}/latest",
    response_model=NotificationRead | None,
)
def get_last_notification(
    user_id: int,
    service: NotificationService = Depends(get_notification_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_latest_by_user(alarm, user_id)

@router.get(
    "/user/{user_id}/unread-count",
    response_model=int,
)
def get_unread_count(
    user_id: int,
    service: NotificationService = Depends(get_notification_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_unread_count(alarm, user_id)

@router.get(
    "/{notification_id}",
    response_model=NotificationRead,
)
def get_notification_by_id(
    notification_id: int,
    service: NotificationService = Depends(get_notification_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_by_id(alarm, notification_id)

@router.post(
    "",
    response_model=NotificationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_notification(
    request: NotificationCreate,
    service: NotificationService = Depends(get_notification_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.create(alarm, request)

@router.patch(
    "/{notification_id}/read",
    response_model=NotificationRead,
)
def mark_as_read(
    notification_id: int,
    request: NotificationUpdate,
    service: NotificationService = Depends(get_notification_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.update(alarm, notification_id, request)

@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_notification(
    notification_id: int,
    service: NotificationService = Depends(get_notification_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    service.delete(alarm, notification_id)
