import paho.mqtt.client as mqtt

from mqtt.mqtt_settings import mqtt_settings as settings
from mqtt.topics import Topics

import logging
logger = logging.getLogger(__name__)

class MQTTClient:
    def __init__(
        self,
        alarm_id: int,
    ):

        self.alarm_id = alarm_id

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=settings.client_id,
        )

        self.client.username_pw_set(
            settings.username,
            settings.password,
        )

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        self.dispatcher = None

    def start(self):
        self.client.connect(
            settings.host,
            settings.port,
        )
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish(
        self,
        topic: str,
        payload: str,
    ):
        result = self.client.publish(
            topic,
            payload,
        )
        logger.info(
            "MQTT publish rc=%s mid=%s",
            result.rc,
            result.mid,
        )

    def on_connect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties,
    ):
        if reason_code != 0:
            logger.error(f"MQTT connection failed {reason_code}")
            return
        logger.info("MQTT connected")
        self.subscribe(topic=Topics.COMMAND)

    def on_disconnect(
        self,
        client,
        userdata,
        disconnect_flags,
        reason_code,
        properties,
    ):
        logger.warning(f"MQTT disconnected {reason_code}")

    def on_message(
        self,   
        client,
        userdata,
        msg,
    ):
        logger.info(
            "MQTT RX topic=%s payload=%s",
            msg.topic,
            msg.payload.decode(),
        )

        if self.dispatcher is None:
            return
        
        self.dispatcher.dispatch(
            topic=msg.topic,
            payload=msg.payload,
        )
    def subscribe(
        self,
        topic: str,
    ):
        result, mid = self.client.subscribe(topic)
        logger.info(
            "Subscribed to topic=%s rc=%s mid=%s",
            topic,
            result,
            mid,
        )

    def set_dispatcher(self, dispatcher):
        self.dispatcher = dispatcher

