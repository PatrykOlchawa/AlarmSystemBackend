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

    def _get_handler(
        self,
        db,
        message: MQTTMessage,
    ):
        match message.message_type:
            case MQTTMessageType.SENSOR:
                return self.factory.create_sensor_handler(db)
            case MQTTMessageType.STATE:
                match message.resource_type:
                    case "device":
                        return self.factory.create_device_state_handler(db)
                    case "alarm":
                        return self.factory.create_alarm_state_handler(db)
            case MQTTMessageType.COMMAND:
                logger.warning(
                    "Backend should not receive command messages"
                )
        logger.warning(
            "No handler for topic"
        )
        return None

    def dispatch(
        self,
        topic: str,
        payload: bytes,
    ) -> None:
        
        db = self.factory.create_session()
        try: 
            parts = topic.split("/")
            if len(parts) < 4 :
                logger.warning(f"Invalid topic: {topic}")
                return

            if parts[0] != "alarm":
                logger.warning("Invalid topic: %s", topic)
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
            
            resource_type = parts[3]
            resource_id = None
            if len(parts) > 4:
                    try:
                        resource_id = int(parts[4])
                    except ValueError:
                        logger.warning(
                            "Invalid resource id in topic %s",
                            topic,
                        )
                        return       
            logger.info(
                "parts=%s resource_type=%s resource_id=%s",
                parts,
                resource_type,
                resource_id,
            )          
            message = MQTTMessage(
                alarm_id=alarm_id,
                message_type=message_type,
                resource_type=resource_type,
                resource_id=resource_id,
                payload=payload,
            )

            handler = self._get_handler(
                db=db,
                message=message,
            )
            if handler is None:
                return

            handler.handle(message)

        finally:
            db.close()


dispatcher = MQTTDispatcher()

