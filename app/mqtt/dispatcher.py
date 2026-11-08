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
            case MQTTMessageType.READING:
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
            case MQTTMessageType.CONFIG:
                match message.resource_type:
                    case "cameras":
                        logger.info(
                            "Cameras config revieced"
                        )
                        return self.factory.create_cameras_config_handler()
        logger.warning(
            "No handler for topic"
        )
        return None

    def dispatch(
        self,
        topic: str,
        payload: bytes,
    ) -> None:
        

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
            
            # resource_type = parts[3]
            # resource_id = None
            # if len(parts) > 4:
            #         try:
            #             resource_id = int(parts[4])
            #         except ValueError:
            #             logger.warning(
            #                 "Invalid resource id in topic %s",
            #                 topic,
            #             )
            #             return       
            # logger.info(
            #     "parts=%s resource_type=%s resource_id=%s",
            #     parts,
            #     resource_type,
            #     resource_id,
            # )       

            resource_type = None
            resource_id = None
            match message_type:

                case MQTTMessageType.READING:
                    if len(parts) != 5 or parts[3] != "sensor":
                        logger.warning("Invalid reading topic: %s", topic)
                        return None

                    resource_type = "sensor"

                    try:
                        resource_id = int(parts[4])
                    except ValueError:
                        logger.warning("Invalid sensor ID: %s", topic)
                        return None

                case MQTTMessageType.STATE:
                    if len(parts) == 4:
                        resource_type = parts[3]

                        if resource_type != "alarm":
                            logger.warning("Invalid state topic: %s", topic)
                            return None

                    elif len(parts) == 5 and parts[3] == "device":
                        resource_type = "device"

                        try:
                            resource_id = int(parts[4])
                        except ValueError:
                            logger.warning("Invalid device ID: %s", topic)
                            return None

                    else:
                        logger.warning("Invalid state topic: %s", topic)
                        return None

                case MQTTMessageType.CONFIG:
                    if len(parts) != 4:
                        logger.warning("Invalid config topic: %s", topic)
                        return None

                    resource_type = parts[3]

                case MQTTMessageType.COMMAND:
                    logger.warning("Backend should not receive command messages")
                    return None  
                case _:
                    logger.warning("Unsupported MQTT message type: %s", message_type)
                    return
            message = MQTTMessage(
                alarm_id=alarm_id,
                message_type=message_type,
                resource_type=resource_type,
                resource_id=resource_id,
                payload=payload,
            )
            db = self.factory.create_session()
            
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

