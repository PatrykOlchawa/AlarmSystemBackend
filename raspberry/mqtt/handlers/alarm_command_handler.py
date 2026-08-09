from mqtt.schemas import MQTTMessage, AlarmCommandPayload
from gpio.device_manager import DeviceManager
from mqtt.publishers.alarm_state_publisher import AlarmStatePublisher
from gpio.alarm_manager import AlarmManager
from pydantic import ValidationError
from common.schemas import AlarmStatus
import logging
logger = logging.getLogger(__name__)
class AlarmCommandHandler:
    def __init__(
        self,
        alarm_manager: AlarmManager,
        alarm_state_publisher: AlarmStatePublisher,
    ):
        self.alarm_manager = alarm_manager
        self.alarm_state_publisher = alarm_state_publisher
        
    def handle(
        self,
        message: MQTTMessage,
    ):
        try:
            payload = AlarmCommandPayload.model_validate_json(
                message.payload 
            )

            logger.info(
                "Command received fro device $s",
                message.resource_id
            )

            
            if payload.armed:
                self.alarm_manager.set_status(
                    AlarmStatus.ARMED
                )
            else:
                self.alarm_manager.set_status(
                    AlarmStatus.DISARMED
                )

            self.alarm_state_publisher.publish(
                status=self.alarm_manager.status,
            )
        except ValidationError as exc:
            logger.warning(
                "Invalid command payload %s",
                exc,
            )

        except Exception:
            logger.exception(
                "Failed to process command"
            )