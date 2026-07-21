from app.modules.alarms.model import Alarm
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
        #self.alarm_service.process_reading(alarm, sensor_id, reading)
        return reading
    
    def delete(
        self,
        alarm: Alarm,
        sensor_id: int,
        reading_id: int,
    ):
        reading = self.get_by_id(alarm, sensor_id, reading_id)
        self.repository.delete(reading)
        