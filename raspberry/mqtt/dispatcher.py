from raspberry.mqtt.schemas import MQTTMessage
from raspberry.mqtt.handlers.device_command_handler import DeviceCommandHandler
from raspberry.common.enums import MQTTMessageType
import logging
logger = logging.getLogger(__name__)
class MQTTDispatcher:
    def __init__(
        self,
        command_handler: DeviceCommandHandler,
    ):
        self.command_handler = command_handler

    def dispatch(
        self,
        topic: str,
        payload: bytes,
    ) -> None:
        
        
        parts = topic.split("/")
        if len(parts) < 4:
            logger.warning(f"Invalid topic: {topic}")
            return

        try:
            alarm_id = int(parts[1])
        except ValueError:
            logger.warning(f"Invalid alarm id in topic {topic}")
            return
        message_type = MQTTMessage(parts[2])
        resource_type = parts[3]
        resource_id = None

        if len(parts) > 4:
            resource_id = int(parts[4])

        message = MQTTMessage(
            alarm_id=alarm_id,
            message_type=message_type,
            resource_type=resource_type,
            resource_id=resource_id,
            payload=payload,
        )
        self.command_handler(message)

dispatcher = MQTTDispatcher()