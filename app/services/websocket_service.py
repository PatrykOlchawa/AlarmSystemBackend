from app.common.enums import MessageEventType
from app.core.websocket.manager import connection_manager
from app.modules.user_alarm.repository import UserAlarmRepository
from app.core.websocket.schemas import WebSocketMessage
from typing import Any
import asyncio
import logging
logger = logging.getLogger(__name__)
from app.core.event_loop import get_event_loop

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
        logger.info("send_message() started")
        users_ids = self.user_alarm_repository.get_alarm_user_ids(alarm_id)
        logger.info(f"Users: {users_ids}")
        payload = WebSocketMessage(
            event=event_type,
            alarm_id=alarm_id,
            data=data,
        )
        await connection_manager.broadcast(
            users_ids,
            payload.model_dump(mode="json"),
        )

    def send_message_sync(
        self,
        alarm_id: int,
        data: dict[str, Any],
        event_type: MessageEventType,
    ) -> None:
        loop = get_event_loop()
        if loop is None:
            return
        asyncio.run_coroutine_threadsafe(
            self.send_message(
                alarm_id=alarm_id,
                data=data,
                event_type=event_type,
            ),
            loop,
        )
