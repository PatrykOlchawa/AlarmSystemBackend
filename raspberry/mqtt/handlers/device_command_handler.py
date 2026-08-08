from raspberry.mqtt.schemas import MQTTMessage, CommandPayload
from raspberry.gpio.device_manager import DeviceManager
from raspberry.mqtt.publishers.alarm_state_publisher import StatePublisher
from pydantic import ValidationError
import logging
logger = logging.getLogger(__name__)
class DeviceCommandHandler:
    def __init__(
        self,
        device_manager: DeviceManager,
        state_publisher: StatePublisher,
    ):
        self.device_manager = device_manager
        self.state_publisher = state_publisher
        
    def handle(
        self,
        message: MQTTMessage,
    ):
        try:
            payload = CommandPayload.model_validate_json(
                message.payload 
            )

            logger.info(
                "Command received fro device $s",
                message.resource
            )

            self.device_manager.set_state(
                device_id=int(message.resource),
                status=payload.root,
            )

            self.state_publisher(
                device_id = message.resource_id,
                status = payload.root,
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