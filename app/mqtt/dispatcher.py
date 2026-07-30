import logging
from app.mqtt.schemas import (
    MQTTMessage,
)
from app.mqtt.handlers.sensor_handler import SensorHandler
#from app.mqtt.handlers.state_handler import StateHandler 
#from app.mqtt.handlers.event_handler import EventHandler
#from app.mqtt.handlers.heartbeat_handler import HeartbeatHandler
from app.common.enums import MQTTMessageType
from app.mqtt.dependencies import get_sensor_handler
    

logger = logging.getLogger(__name__)
class MQTTDispatcher:
    def __init__(self):
        self.handlers = {
            MQTTMessageType.SENSOR: get_sensor_handler(),
#            MQTTMessageType.STATE: StateHandler(),
 #           MQTTMessageType.EVENT: EventHandler(),
  #          MQTTMessageType.HEARTBEAT: HeartbeatHandler(),
        }


    def dispatch(
        self,
        topic: str,
        payload: bytes,
    ) -> None:
        parts = topic.split("/")
        if len(parts) < 3:
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
            logger.warning(f"Unknown MQTT message type: {parts[2]}")
            return
        
        resource = parts[3] if len(parts) > 3 else None

        message = MQTTMessage(
            alarm_id=alarm_id,
            message_type=message_type,
            resource=resource,
            payload=payload,
        )
        logger.info(f"Received MQTT message {message.model_dump()}")

        handler = self.handlers.get(message_type)

        if handler is None:
            logger.warning(f"Unknown message type")
            return
        handler.handle(message)
        
