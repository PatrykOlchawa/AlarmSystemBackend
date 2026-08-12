from app.common.enums import MessageEventType
from app.core.websocket.manager import connection_manager
from app.modules.user_alarm.repository import UserAlarmRepository
from app.core.websocket.schemas import (
    WebSocketMessage,
    GlobalWebsocketMessage,
)
from app.modules.users.repository import UserRepository
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
        logger.info(
            "WS send start: event=%s alarm=%s data=%s",
            event_type,
            alarm_id,
            data,
        )
        logger.info(f"send_message() started")
        users_ids = self.user_alarm_repository.get_alarm_user_ids(alarm_id)
        logger.info(f"Users: {users_ids}")
        payload = WebSocketMessage(
            event=event_type,
            alarm_id=alarm_id,
            data=data,
        )
        logger.info(
            "WS broadcasting:",
            
        )

        await connection_manager.broadcast(
            users_ids,
            payload.model_dump(mode="json"),
        )

        logger.info("WS broadcast finished")

    def send_message_sync(
        self,
        alarm_id: int,
        data: dict[str, Any],
        event_type: MessageEventType,
    ) -> None:
        loop = get_event_loop()
        if loop is None:
            return
        #asyncio.run_coroutine_threadsafe(
        #    self.send_message(
        #        alarm_id=alarm_id,
        #        data=data,
        #        event_type=event_type,
        #    ),
        #    loop,
        #)
        future = asyncio.run_coroutine_threadsafe(
        self.send_message(
            alarm_id=alarm_id,
            data=data,
            event_type=event_type,
        ),
        loop,
    )

        def done_callback(future):
            try:
                future.result()
            except Exception:
                logger.exception(
                    "WebSocket send_message failed"
                )

        future.add_done_callback(done_callback)

    async def send_message_to_admins(
        self,
        admin_ids: list[int],
        data: dict[str, Any],
        event_type: MessageEventType,
    ):
        payload = GlobalWebsocketMessage(
            event=event_type,
            data=data,
        )

        await connection_manager.broadcast(
            admin_ids,
            payload.model_dump(mode="json"),
        )

    def send_message_to_admins_sync(
        self,
        admin_ids: list[int],
        data: dict[str, Any],
        event_type: MessageEventType,
    ):
        loop = get_event_loop()

        if loop is None:
            return

        asyncio.run_coroutine_threadsafe(
            self.send_message_to_admins(
                admin_ids=admin_ids,
                data=data,
                event_type=event_type,
            ),
            loop,
        )