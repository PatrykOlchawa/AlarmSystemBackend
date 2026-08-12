from app.modules.sensors.schemas import (
    SensorCreate,
    SensorUpdate
)
from app.core.exceptions import (
    SensorNotFoundException,
    WebsocketException,
)
from app.modules.sensors.model import Sensor
from app.modules.sensors.repository import SensorRepository
from app.modules.alarms.model import Alarm
from app.services.websocket_service import WebSocketMessageService
from app.common.enums import MessageEventType

class SensorService:
    def __init__(
        self,
        repository: SensorRepository,
        websocket_service: WebSocketMessageService
    ):
        self.repository = repository
        self.websocket_service = websocket_service
    
    def get_all_sensors(
        self,
        alarm: Alarm,
    ):
        return self.repository.get_all(alarm)
    
    def get_sensor_by_id(
        self,
        alarm: Alarm,
        sensor_id: int
    ):
        sensor = self.repository.get_by_id(alarm, sensor_id)
        if sensor is None:
            raise SensorNotFoundException

        return self.repository.get_by_id(alarm, sensor_id)

    def get_by_alarm_and_name(
        self,
        alarm_id: int,
        sensor_name: str,
    ) -> Sensor:
        sensor = self.repository.get_by_alarm_and_name(alarm_id, sensor_name)
        if Sensor is None:
            raise SensorNotFoundException()
        return sensor
    def get_alarm_and_id(
        self,
        alarm_id: int,
        sensor_id: int,
    ) -> Sensor:
        sensor = self.repository.get_alarm_and_id(alarm_id, sensor_id)
        if Sensor is None:
            raise SensorNotFoundException()
        return sensor
    
    def create_sensor(
        self,
        alarm: Alarm,
        request: SensorCreate,
    ):
        sensor = Sensor(**request.model_dump(exclude={"alarm_id"}), alarm_id=alarm.id)
        sensor = self.repository.create_sensor(sensor)
        self._notify_sensors_changed(alarm_id=alarm.id)
        return sensor
    
    def update_sensor(
        self,
        alarm: Alarm,
        sensor_int: int,
        request: SensorUpdate
    ):
        sensor = self.get_sensor_by_id(alarm, sensor_int)
        if sensor is None:
            raise SensorNotFoundException
        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(sensor, field, value)
        return self.repository.update_sensor(sensor)
        self._notify_sensors_changed(alarm_id=alarm.id)
    
    def delete_sensor(
        self,
        alarm: Alarm,
        sensor_id: int,
    ):
        sensor = self.get_sensor_by_id(alarm, sensor_id)
        if sensor is None:
            raise SensorNotFoundException
        self.repository.delete_sensor(sensor)
        self._notify_sensors_changed(alarm_id=alarm.id)

    def _notify_sensors_changed(
        self,
        alarm_id: int,
    ) -> None:
        try:
            self.websocket_service.send_message_sync(
                alarm_id=alarm_id,
                event_type=MessageEventType.SENSORS_CHANGED,
                data={},
            )
        except Exception:
            raise WebsocketException