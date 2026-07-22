from app.modules.sensors.schemas import SensorUpdate
from app.core.exceptions import SensorNotFoundException
from app.modules.sensors.model import Sensor
from app.modules.sensors.repository import SensorRepository
from app.modules.sensors.schemas import SensorCreate
from app.modules.alarms.model import Alarm
class SensorService:
    def __init__(
        self,
        repository: SensorRepository
    ):
        self.repository = repository
    
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
    
    def create_sensor(
        self,
        alarm: Alarm,
        request: SensorCreate,
    ):
        sensor = Sensor(**request.model_dump(exclude={"alarm_id"}), alarm_id=alarm.id)
        return self.repository.create_sensor(sensor)
    
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
    
    def delete_sensor(
        self,
        alarm: Alarm,
        sensor_id: int,
    ):
        sensor = self.get_sensor_by_id(alarm, sensor_id)
        if sensor is None:
            raise SensorNotFoundException
        self.repository.delete_sensor(sensor)