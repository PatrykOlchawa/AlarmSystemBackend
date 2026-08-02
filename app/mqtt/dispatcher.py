import logging
from app.mqtt.schemas import (
    MQTTMessage,
)
from app.common.enums import MQTTMessageType
from app.core.service_factory import ServicesFactory
logger = logging.getLogger(__name__)
class MQTTDispatcher:
    def __init__(self):
        self.factory = ServicesFactory()

    def dispatch(
        self,
        topic: str,
        payload: bytes,
    ) -> None:
        
        db = self.factory.create_session()
        try: 
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
            match message.message_type:

                case MQTTMessageType.SENSOR:
                    handler = self.factory.create_sensor_handler(db)
                case MQTTMessageType.STATE:
                    handler = self.factory.create_state_handler(db)
                case _:
                    logger.warning(
                        "No handler for %s",
                        message.message_type,
                    )
                    return
            logger.info("Sending sensor websocket notification")
            handler.handle(message)
            logger.info("Sensor websocket notification scheduled")
        finally:
            db.close()
dispatcher = MQTTDispatcher()