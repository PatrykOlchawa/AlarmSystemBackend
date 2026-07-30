from app.mqtt.schemas import (
    MQTTMessage,
    SensorPayload,
)
from app.mqtt.handlers.base_handler import BaseHandler
from app.modules.sensors.service import SensorService
from app.modules.readings.service import SensorReadingService
from pydantic import ValidationError
import logging
logger = logging.getLogger(__name__)
class SensorHandler(BaseHandler):
    def __init__(
        self,
        sensor_service: SensorService,
        reading_service: SensorReadingService,
    ):
        self.sensor_service = sensor_service
        self.reading_service = reading_service

    def handle(
        self,
        message: MQTTMessage,        
        
    ) -> None:
        try:
            payload = SensorPayload.model_validate_json(message.payload)

            sensor = self.sensor_service.get_by_alarm_and_name(
                alarm_id=message.alarm_id,
                sensor_name=message.resource,
            )
            self.reading_service.create_for_sensor(
                sensor=sensor,
                request=payload,
            )
        except ValidationError as exc:
            logger.warning(f"Invalid sensor payload {exc}")

        except Exception:
            logger.exception(f"Unexpected error while processing MQTT sensor message")