from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.readings.model import SensorReading

class SensorReadingRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(self) -> list[SensorReading]:
        stmt = (
            select(SensorReading)
            .order_by(SensorReading.timestamp.desc())
        )
        return list(self.session.scalars(stmt).all())

    def get_by_id(self, reading_id: int) -> SensorReading | None:
        stmt = (
            select(SensorReading)
            .where(SensorReading.id == reading_id)
        )
        return self.session.scalar(stmt)

    def get_by_sensor(self, sensor_id:int) -> list[SensorReading]:
        stmt = (
            select(SensorReading)
            .where(SensorReading.sensor_id == sensor_id)
            .order_by(SensorReading.timestamp.desc())
        )
        return list(self.session.scalars(stmt).all())

    def create(self, reading: SensorReading) -> SensorReading:
        self.session.add(reading)
        self.session.commit()
        self.session.refresh(reading)
        return reading
    
    def delete(self, reading: SensorReading) -> None:
        self.session.delete(reading)
        self.session.commit()

    def get_latest_by_sensor(self, sensor_id: int) -> SensorReading | None:
        stmt = (
            select(SensorReading)
            .where(SensorReading.sensor_id == sensor_id)
            .order_by(SensorReading.timestamp.desc())
            .limit(1)
        )
        return self.session.scalar(stmt)