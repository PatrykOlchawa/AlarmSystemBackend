from app.modules.sensors.schemas import SensorUpdate
from app.core.exceptions import SensorNotFoundException
from app.modules.sensors.model import Sensor
from app.modules.sensors.repository import SensorRepository
from app.modules.sensors.schemas import SensorCreate

class SensorService:
    def __init__(
        self,
        repository: SensorRepository
    ):
        self.repository = repository
    
    def get_all_sensors(self):
        return self.repository.get_all()
    
    def get_sensor_by_id(
        self,
        sensor_id: int
    ):
        sensor = self.repository.get_by_id(sensor_id)
        if sensor is None:
            raise SensorNotFoundException

        return self.repository.get_by_id(sensor_id)
    
    def create_sensor(
        self,
        request: SensorCreate,
    ):
        sensor = Sensor(
            name = request.name,
            type = request.type,
            gpio_pin = request.gpio_pin,
            enabled = request.enabled
        )
        return self.repository.create_sensor(sensor)
    
    def update_sensor(
        self,
        sensor_int: int,
        request: SensorUpdate
    ):
        sensor = self.get_sensor_by_id(sensor_int)
        if sensor is None:
            raise SensorNotFoundException
        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(sensor, field, value)
        return self.repository.update_sensor(sensor)
    
    def delete_sensor(
        self,
        sensor_id: int,
    ):
        sensor = self.get_sensor_by_id(sensor_id)
        if sensor is None:
            raise SensorNotFoundException
        self.repository.delete_sensor(sensor)