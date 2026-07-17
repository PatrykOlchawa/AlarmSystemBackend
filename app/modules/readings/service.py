from app.modules.readings.model import SensorReading
from app.core.exceptions import SensorReadingNotFoundException
from app.modules.readings.repository import (
    SensorReadingRepository,
)

from app.modules.sensors.service import SensorService
from app.modules.readings.schemas import SensorReadingCreate
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.services.alarm_service import AlarmService

class SensorReadingService:
    def __init__(
        self,
        repository: SensorReadingRepository,
        sensor_service: SensorService,
        alarm_service: "AlarmService",
    ):
        self.repository = repository
        self.sensor_service = sensor_service
        self.alarm_service = alarm_service

    def get_all(self):
        return self.repository.get_all()
    
    def get_by_id(
        self,
        reading_id: int
    ):
        reading = self.repository.get_by_id(reading_id)
        if reading is None:
            raise SensorReadingNotFoundException()
        return reading
    def get_by_sensor(
        self,
        sensor_id: int,
    ):
        self.sensor_service.get_sensor_by_id(sensor_id)
        
        return self.repository.get_by_sensor(sensor_id)
    
    def get_latest_by_sensor(
        self,
        sensor_id: int,
    ):
        self.sensor_service.get_sensor_by_id(sensor_id)
        
        return self.repository.get_latest_by_sensor(sensor_id)
    
    def create(
        self,
        request: SensorReadingCreate,
    ):
        sensor = self.sensor_service.get_sensor_by_id(request.sensor_id)

        reading = SensorReading(
            sensor_id=sensor.id,
            value=request.value,
        )
        reading = self.repository.create(reading)
        
        self.alarm_service.process_reading(reading)

        return reading
    
    def delete(
        self,
        reading_id: int
    ):
        reading = self.get_by_id(reading_id)
        self.repository.delete(reading)
        