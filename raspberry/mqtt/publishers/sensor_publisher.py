import json
from mqtt.client import MQTTClient
from mqtt.topics import Topics

class SensorPublisher:
    def __init__(
        self,
        mqtt_client: MQTTClient,
    ):
        self.mqtt_client = mqtt_client

    def publish(
        self,
        sensor_id: int,
        value,
    ) -> None:
        self.mqtt_client.publish(
            topic=Topics.sensor(
                alarm_id=self.mqtt_client.alarm_id,
                sensor=sensor_id,
            ),
            payload= json.dumps({
                "value": value,
            })
        )