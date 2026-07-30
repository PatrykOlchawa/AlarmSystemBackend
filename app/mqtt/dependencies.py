from app.modules.sensors.dependencies import get_sensor_service
from app.modules.readings.dependencies import get_sensor_reading_service
from app.mqtt.handlers.sensor_handler import SensorHandler
from app.mqtt.service import MQTTService
def get_sensor_handler() -> SensorHandler:
    return SensorHandler(
        sensor_service=get_sensor_service(),
        reading_service=get_sensor_reading_service(),
    )

def get_mqtt_service() -> MQTTService:
    return MQTTService()