from app.modules.alarms.model import Alarm
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.modules.events.model import AlarmEvent
from app.common.enums import AlarmEventType

class AlarmEventRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(
        self,
        alarm:Alarm
    ) -> list[AlarmEvent]:
        stmt = (
            select(AlarmEvent)
            .where(AlarmEvent.alarm_id == alarm.id)
            .order_by(AlarmEvent.timestamp.desc())
        )
        return list(self.session.scalars(stmt).all())
         
    def get_by_id(
        self,
        alarm:Alarm,
        event_id:int,
    ) -> AlarmEvent | None:
        stmt = (
            select(AlarmEvent)
            .where(AlarmEvent.alarm_id == alarm.id)
            .where(AlarmEvent.id == event_id)
        )
        return self.session.scalar(stmt)
    
    def get_latest(
        self,
        alarm:Alarm
    ) -> AlarmEvent | None:
        stmt = (
            select(AlarmEvent)
            .where(AlarmEvent.alarm_id == alarm.id)
            .order_by(AlarmEvent.timestamp.desc()).limit(1)
        )
        return self.session.scalar(stmt)
    
    def get_by_type(
        self,
        alarm:Alarm,
        event_type: AlarmEventType,
    ) -> list[AlarmEvent]:
        stmt = (
            select(AlarmEvent)
            .where(AlarmEvent.alarm_id == alarm.id)
            .where(AlarmEvent.event_type == event_type)
            .order_by(AlarmEvent.timestamp.desc())
        )
        return list(self.session.scalars(stmt).all())

    def create(
        self,
        event: AlarmEvent,
    ) -> AlarmEvent:
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event
    
    def delete(
        self,
        event: AlarmEvent,
    ) -> None:
        self.session.delete(event)
        self.session.commit()