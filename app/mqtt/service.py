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
            topic=Topics.command_alarm(
                alarm_id=alarm_id,
            ),
            payload={
                "armed" : armed,
            }
        )
    def publish_device_command(
        self,
        alarm_id: int,
        device_id: int,
        payload: dict,
    ) -> None:
        self.publish(
            topic=Topics.command_device(
                alarm_id=alarm_id,
                device_id=device_id,
            ),
            payload=payload
        )
mqtt_service = MQTTService()