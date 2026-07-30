from app.modules.alarms.model import Alarm
from app.modules.readings.model import SensorReading
from app.core.exceptions import SensorReadingNotFoundException
from app.modules.readings.repository import SensorReadingRepository
from app.modules.sensors.service import SensorService
from app.modules.readings.schemas import SensorReadingCreate
from app.modules.sensors.model import Sensor


class SensorReadingService:
    def __init__(
        self,
        repository: SensorReadingRepository,
        sensor_service: SensorService,
    ):
        self.repository = repository
        self.sensor_service = sensor_service

    def get_all(
        self,
        alarm: Alarm,
        sensor_id: int,
    ):
        return self.repository.get_all(alarm, sensor_id)
    
    def get_by_id(
        self,
        alarm: Alarm,
        sensor_id: int,
        reading_id: int,
    ):
        return self.repository.get_by_id(alarm, sensor_id, reading_id)
    
    def get_latest(
        self,
        alarm: Alarm,
        sensor_id: int,
    ):
        return self.repository.get_latest_by_sensor(alarm, sensor_id)
    
    def create(
        self,
        alarm: Alarm,
        sensor_id: int, 
        request: SensorReadingCreate,
    ):
        reading = SensorReading(**request.model_dump(),sensor_id=sensor_id)
        reading = self.repository.create(reading)
        return reading

    def create_for_sensor(
        self,
        sensor: Sensor,
        request: SensorReadingCreate,        
    ) -> SensorReading:
        reading = SensorReading(
            sensor_id=sensor.id,
            **request.model_dump(),
        )
        reading = self.repository.create(reading)
        return reading
    def delete(
        self,
        alarm: Alarm,
        sensor_id: int,
        reading_id: int,
    ):
        reading = self.get_by_id(alarm, sensor_id, reading_id)
        self.repository.delete(reading)
        