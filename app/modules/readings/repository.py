from app.modules.alarms.model import Alarm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.readings.model import SensorReading
from app.modules.sensors.model import Sensor
class SensorReadingRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(
        self,
        alarm: Alarm,
        sensor_id: int,
    ) -> list[SensorReading]:
        stmt = (
           select(SensorReading)
            .join(Sensor)
            .where(Sensor.id == sensor_id)
            .where(Sensor.alarm_id == alarm.id)
            .order_by(SensorReading.timestamp.desc())
        )
        return list(self.session.scalars(stmt).all())

    def get_by_id(
        self,
        alarm: Alarm,
        sensor_id: int,
        reading_id: int
    ) -> SensorReading | None:
        stmt = (
           select(SensorReading)
            .join(Sensor)
            .where(Sensor.id == sensor_id)
            .where(Sensor.alarm_id == alarm.id)
            .where(SensorReading.id == reading_id)
            .order_by(SensorReading.timestamp.desc())
        )
        return self.session.scalar(stmt)


    def create(
        self,
        reading: SensorReading
    ) -> SensorReading:
        self.session.add(reading)
        self.session.commit()
        self.session.refresh(reading)
        return reading
    
    def delete(
        self,
        reading: SensorReading
    ) -> None:
        self.session.delete(reading)
        self.session.commit()

    def get_latest_by_sensor(
        self,
        alarm: Alarm,
        sensor_id: int
    ) -> SensorReading | None:
        stmt = (
           select(SensorReading)
            .join(Sensor)
            .where(Sensor.id == sensor_id)
            .where(Sensor.alarm_id == alarm.id)
            .order_by(SensorReading.timestamp.desc())
            .limit(1)
        )
        return self.session.scalar(stmt)