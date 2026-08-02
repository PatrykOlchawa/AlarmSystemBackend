from app.modules.devices.service import DeviceService
from app.services.websocket_service import WebSocketMessageService
from app.mqtt.schemas import MQTTMessage, StatePayload
from pydantic import ValidationError
from app.common.enums import DeviceType, MessageEventType
from app.modules.alarms.service import AlarmService
import logging
logger = logging.getLogger(__name__)
class StateHandler:
    def __init__(
        self,
        device_service: DeviceService,
        websocket_service: WebSocketMessageService,
        alarm_service: AlarmService,

    ):
        self.device_service = device_service
        self.websocket_service = websocket_service
        self.device_repository = self.device_service.repository
        self.alarm_service = alarm_service

    def handle(
        self,
        message: MQTTMessage
    ):
        logger.info("StateHandler started")
        logger.info("Topic resource: %s", message.resource)
        logger.info("Payload: %s", message.payload)
        try:

            payload = payload = StatePayload.model_validate_json(
                message.payload
            ).root
            alarm = self.alarm_service.get_by_id(message.alarm_id)
            device = self.device_service.get_by_name(
                alarm=alarm,
                name=message.resource
            )
            device.status = payload
            self.device_repository.update(device)
            try:

                self.websocket_service.send_message_sync(
                    alarm_id=device.alarm_id,
                        event_type=MessageEventType.DEVICE_STATE_CHANGED,
                        data={
                            "device_id": device.id,
                            "device_name": device.name,
                            "status": payload,
                        },
                )
            except Exception:
                logger.exception("Failed to send websocket notification")
            
        except ValidationError as exc:
            logger.warning(f"Invalid sensor payload {exc}")

        except Exception:
            logger.exception(f"Unexpected error while processing MQTT sensor message")

    