from raspberry.mqtt.schemas import MQTTMessage
from raspberry.mqtt.handlers.command_handler import CommandHandler
import logging
logger = logging.getLogger(__name__)
class MQTTDispatcher:
    def __init__(
        self,
        command_handler: CommandHandler,
    ):
        self.command_handler = command_handler

    def dispatch(
        self,
        topic: str,
        payload: bytes,
    ) -> None:
        
        
        parts = topic.split("/")
        if len(parts) != 4:
            logger.warning(f"Invalid topic: {topic}")
            return

        try:
            alarm_id = int(parts[1])
        except ValueError:
            logger.warning(f"Invalid alarm id in topic {topic}")
            return
        
        resource = parts[3]

        message = MQTTMessage(
            alarm_id=alarm_id,
            resource=resource,
            payload=payload,
        )
        self.command_handler(message)

dispatcher = MQTTDispatcher()