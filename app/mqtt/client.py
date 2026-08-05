import paho.mqtt.client as mqtt
from app.core.config import settings
from app.mqtt.topics import Topics

import logging
logger = logging.getLogger(__name__)
class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id= settings.mqtt_client_id
        )
        self.client.username_pw_set(
            settings.mqtt_username,
            settings.mqtt_password,
        )
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.dispatcher = None
        
    def start(self):
        self.client.connect(
            settings.mqtt_host,
            settings.mqtt_port,
        )
        self.client.loop_start()

    def stop(self):
        logger.info("Stopping MQTT client")

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

        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            logger.error(
                "Failed to publish message (rc=%s)",
                result.rc,
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
        self.__subscribe()

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

    def __subscribe(self):
        self.client.subscribe(Topics.SENSOR)
        self.client.subscribe(Topics.STATE)
        self.client.subscribe(Topics.EVENT)
        self.client.subscribe(Topics.HEARTBEAT)

    def set_dispatcher(self, dispatcher):
        self.dispatcher = dispatcher

mqtt_client = MQTTClient()