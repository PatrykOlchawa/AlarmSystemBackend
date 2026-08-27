from app.mqtt.service import MQTTService

def get_mqtt_service() -> MQTTService:
    return MQTTService()