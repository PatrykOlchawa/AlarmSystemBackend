import json
from mqtt.client import MQTTClient
from mqtt.topics import Topics
from common.schemas import AlarmStatus 
class AlarmStatePublisher:
    def __init__(
        self,
        mqtt_client: MQTTClient,
    ):
        self.mqtt_client = mqtt_client

    def publish(
        self,
        status: AlarmStatus,
    ) -> None:
        self.mqtt_client.publish(
            topic=Topics.state_alarm(
                alarm_id=self.mqtt_client.alarm_id
            ),
            payload= json.dumps(
                {
                    "status": status.value
                }
            ),
        )