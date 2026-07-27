from app.common.enums import MessageEventType
from app.core.websocket.manager import connection_manager
from app.modules.user_alarm.repository import UserAlarmRepository
from app.core.websocket.schemas import WebSocketMessage
from typing import Any
class WebSocketMessageService:
    def __init__(
        self,
        user_alarm_repository: UserAlarmRepository,
    ) -> None:
        self.user_alarm_repository = user_alarm_repository

    async def send_message(
        self,
        alarm_id, 
        data: dict[str, Any],
        event_type: MessageEventType,
    ) -> None:
        users_ids = self.user_alarm_repository.get_alarm_user_ids(alarm_id)

        payload = WebSocketMessage(
            event=event_type,
            alarm_id=alarm_id,
            data=data,
        )
        await connection_manager.broadcast(
            users_ids,
            payload.model_dump(mode="json"),
        )