from fastapi import Depends

from app.services.websocket_service import WebSocketMessageService
from app.modules.user_alarm.dependencies import get_user_alarm_repository


def get_websocket_service(
    user_alarm_repository = Depends(get_user_alarm_repository),
) -> WebSocketMessageService:
    return WebSocketMessageService(user_alarm_repository)
