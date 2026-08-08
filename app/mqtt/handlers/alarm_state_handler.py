from pydantic import ValidationError
import logging

from app.mqtt.schemas import (
    MQTTMessage,
    AlarmStatePayload,
)
from app.modules.alarms.service import AlarmService
from app.common.enums import (
    MessageEventType,
)
from app.services.websocket_service import WebSocketMessageService

logger = logging.getLogger(__name__)

class AlarmStateHandler:

    def __init__(
        self,
        alarm_service: AlarmService,
        websocket_service: WebSocketMessageService,
    ):
        self.alarm_service = alarm_service
        self.websocket_service = websocket_service

    def handle(
            self,
            message: MQTTMessage
        ):

            try:    
                payload = AlarmStatePayload.model_validate_json(
                    message.payload
                )

                alarm = self.alarm_service.get_by_id(message.alarm_id)
                alarm_status = payload.status
                self.alarm_service.set_alarm_status(
                    alarm=alarm,
                    alarm_status=alarm_status,
                )
                try:
    
                    self.websocket_service.send_message_sync(
                        alarm_id= alarm.id,
                            event_type=MessageEventType.ALARM_STATUS_CHANGED,
                            data={
                                "alarm_id": alarm.id,
                                "status": alarm_status,
                            },
                    )
                except Exception:
                    logger.exception("Failed to send websocket notification")
                
            except ValidationError as exc:
                logger.warning(f"Invalid sensor payload {exc}")
    
            except Exception:
                logger.exception(f"Unexpected error while processing MQTT sensor message")