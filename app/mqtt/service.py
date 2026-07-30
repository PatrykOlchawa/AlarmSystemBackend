from app.mqtt.client import mqtt_client
from app.mqtt.topics import Topics
import json
import logging
logger = logging.getLogger(__name__)
class MQTTService:
    def __init__(self):
        pass
    def publish(
        self,
        topic:str,
        payload: dict,
    ) -> None:
        mqtt_client.publish(
            topic=topic,
            payload=json.dumps(payload)
        )
        logger.info(
            "Published MQTT message to %s",
            topic,
        )
    def publish_alarm_command(
        self,
        alarm_id: int,
        armed: bool,
    ) -> None: 
        self.publish(
            topic=Topics.command(
                alarm_id=alarm_id,
                device="alarm",
            ),
            payload={
                "armed" : armed,
            }
        )

