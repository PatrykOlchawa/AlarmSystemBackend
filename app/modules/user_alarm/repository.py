from app.common.enums import AlarmRole
from sqlalchemy.orm import Session
from app.modules.user_alarm.model import UserAlarm
from sqlalchemy import select

class UserAlarmRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(
        self,
        user_id: int,
        alarm_id: int,
    ) -> UserAlarm | None:
        stmt = (
            select(UserAlarm)
            .where(UserAlarm.user_id == user_id)
            .where(UserAlarm.alarm_id == alarm_id)
        )
        return self.session.scalar(stmt)
    
    def get_alarm_members(
        self,
        alarm_id: int
    ) -> list[UserAlarm]:
        stmt = (
            select(UserAlarm)
            .where(UserAlarm.alarm_id == alarm_id)
        )
        return list(self.session.scalars(stmt))
    
    def get_user_alarms(
        self,
        user_id: int,
    ) -> list[UserAlarm]:
        stmt = (
            select(UserAlarm)
            .where(UserAlarm.user_id == user_id)
        )
        return list(self.session.scalars(stmt))

    def create(
        self,
        membership: UserAlarm,
    ) -> UserAlarm:
        self.session.add(membership)
        self.session.commit()
        self.session.refresh(membership)
        return membership

    def delete(
        self,
        membership: UserAlarm,
    ) -> None:
        self.session.delete(membership)
        self.session.commit()