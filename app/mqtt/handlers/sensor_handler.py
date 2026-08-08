from app.mqtt.schemas import (
    MQTTMessage,
    SensorPayload,
)
from app.mqtt.handlers.base_handler import BaseHandler
from app.modules.sensors.service import SensorService
from app.modules.readings.service import SensorReadingService
from pydantic import ValidationError
from app.services.websocket_service import WebSocketMessageService
from app.common.enums import MessageEventType
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.alarm_service import AlarmControlService
logger = logging.getLogger(__name__)
class SensorHandler(BaseHandler):
    def __init__(
        self,
        sensor_service: SensorService,
        reading_service: SensorReadingService,
        websocket_service: WebSocketMessageService,
        alarm_control_service: "AlarmControlService",
    ):
        self.sensor_service = sensor_service
        self.reading_service = reading_service
        self.websocket_service = websocket_service
        self.alarm_control_service = alarm_control_service

    def handle(
        self,
        message: MQTTMessage,        
        
    ) -> None:
        logger.info(
            "SensorHandler resource_type=%s resource_id=%s",
            message.resource_type,
            message.resource_id,
        )
        try:
            payload = SensorPayload.model_validate_json(message.payload)
            logger.info(f"resource {message.resource_id}")
            sensor = self.sensor_service.get_alarm_and_id(
                alarm_id=message.alarm_id,
                sensor_id=message.resource_id,
            )
            reading = self.reading_service.create_for_sensor(
                sensor=sensor,
                request=payload,
            )
            try: 
                self.websocket_service.send_message_sync(
                    alarm_id=sensor.alarm_id,
                    event_type=MessageEventType.SENSOR_UPDATED,
                    data={
                        "sensor_id": sensor.id,
                        "sensor_name": sensor.name,
                        "value": reading.value,
                        "timestamp": reading.timestamp.isoformat(),
                    },
                )
            except Exception:
                logger.exception("Failed to send websocket notification")

            self.alarm_control_service.process_sensor_reading(message.alarm_id, reading)
        except ValidationError as exc:
            logger.warning(f"Invalid sensor payload {exc}")

        except Exception:
            logger.exception(f"Unexpected error while processing MQTT sensor message")

        
