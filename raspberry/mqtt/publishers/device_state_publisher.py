import json
from mqtt.client import MQTTClient 
from mqtt.topics import Topics

class DeviceStatePublisher:
    def __init__(
        self,
        mqtt_client: MQTTClient,
    ):
        self.mqtt_client = mqtt_client

    def publish(
        self,
        device_id: int,
        payload: dict,
    ) -> None:
        print(f"Publish device status: {payload}")
        self.mqtt_client.publish(
            topic=Topics.state_device(
                alarm_id=self.mqtt_client.alarm_id,
                device_id=device_id,
            ),
            payload= json.dumps(payload)
        )