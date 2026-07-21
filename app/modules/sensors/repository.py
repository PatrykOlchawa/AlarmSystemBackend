from app.modules.alarms.model import Alarm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.sensors.model import Sensor

class SensorRepository:
    def __init__(self, session:Session):
        self.session = session
    
    def get_all(
        self,
        alarm: Alarm,
    ) -> list[Sensor]:
        stmt = (
            select(Sensor)
            .where(Sensor.alarm_id == alarm.id)
        )
        return list(
            self.session.scalars(stmt).all()
        ) 
    def get_by_id(
        self,
        alarm: Alarm,   
        sensor_id: int
    ) -> Sensor | None:
        stmt = (
            select(Sensor)
            .where(Sensor.alarm_id == alarm.id)
            .where(Sensor.id == sensor_id)
        )
        return self.session.scalar(stmt)
    def create_sensor(
        self,
        sensor: Sensor,
        ) -> Sensor:
        self.session.add(sensor)
        self.session.commit()
        self.session.refresh(sensor)
        return sensor
    def update_sensor(
        self,
        sensor: Sensor,
    ) -> Sensor:
        self.session.commit()
        self.session.refresh(sensor)
        return sensor
    def delete_sensor(
        self,
        sensor: Sensor,
    ) -> None:
        self.session.delete(sensor)
        self.session.commit()
        return None