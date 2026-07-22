from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.modules.alarms.model import Alarm
from app.modules.user_alarm.model import UserAlarm
from app.common.enums import AlarmStatus
class AlarmRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Alarm]:
        stmt = (
            select(Alarm)
        )
        return list(self.session.scalars(stmt))
    
    def get_by_id(
        self,
        alarm_id: int
    ) -> Alarm | None:
        stmt = (
            select(Alarm)
            .where(Alarm.id == alarm_id)
        )
        return self.session.scalar(stmt)
    
    def get_by_name(
        self,
        name: str
    ) -> Alarm | None:
        stmt = (
            select(Alarm)
            .where(Alarm.name == name)
        )
        return self.session.scalar(stmt)
    
    def get_by_id_with_users(
        self,
        alarm_id: int
    ) -> Alarm | None:
        stmt = (
            select(Alarm)
            .options(
                selectinload(Alarm.users)
            )
            .where(Alarm.id == alarm_id)
        )
        return self.session.scalar(stmt)

    def get_all_by_user_id(
        self,
        user_id: int
    ) -> list[Alarm]:
        stmt = (
            select(Alarm)
            .where(UserAlarm.user_id == user_id)
            .where(Alarm.is_active == True)
        )
        return list(self.session.scalars(stmt))

    def create(
        self,
        alarm: Alarm
    ) -> Alarm:
        self.session.add(alarm)
        self.session.commit()
        self.session.refresh(alarm)
        return alarm
    
    def update(
        self,
        alarm: Alarm
    ) -> Alarm:        
        self.session.commit()
        self.session.refresh(alarm)
        return alarm

    def delete(
        self,
        alarm: Alarm
    ) -> None:
        self.session.delete(alarm)
        self.session.commit()

    def set_alarm_status(
        self,
        alarm: Alarm,
        status: AlarmStatus,
    ) -> None:
        alarm.status = status
        self.update(alarm)