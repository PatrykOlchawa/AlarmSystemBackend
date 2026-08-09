from mqtt.schemas import MQTTMessage
from mqtt.handlers.device_command_handler import DeviceCommandHandler
from mqtt.handlers.alarm_command_handler import AlarmCommandHandler
from common.enums import MQTTMessageType
import logging
logger = logging.getLogger(__name__)
class MQTTDispatcher:
    def __init__(
        self,
        device_command_handler: DeviceCommandHandler,
        alarm_command_handler: AlarmCommandHandler,
    ):
        self.device_command_handler = device_command_handler
        self.alarm_command_handler = alarm_command_handler

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
        try:
            message_type = MQTTMessageType(parts[2])
        except ValueError:
            logger.warning(
                "Unknown MQTT message type: %s",
                parts[2],
            )
            return
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
        handler = self._get_handler(message)
        handler.handle(message)

    def _get_handler(
        self,
        message: MQTTMessage,
    ):
        match message.message_type:

            case MQTTMessageType.COMMAND:
                match message.resource_type:
                    case "device":
                        return self.device_command_handler
                    case "alarm":
                        return self.alarm_command_handler
        return None