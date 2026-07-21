from app.modules.alarms.model import Alarm
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.modules.settings.model import Setting

class SettingRepository:
    def __init__(
        self,
        session: Session,
    ):
        self.session = session
    
    def get_all(
        self,
        alarm: Alarm
    ) -> list[Setting]:
        stmt = (
            select(Setting)
            .where(Setting.alarm_id == alarm.id)
            .order_by(Setting.key)
        )
        return list(self.session.scalars(stmt).all())
    
    def get_by_id(
        self,
        alarm: Alarm,
        setting_id:int,
    ) -> Setting | None:
        stmt = (
            select(Setting)
            .where(Setting.alarm_id == alarm.id)
            .where(Setting.id == setting_id)
        )
        return self.session.scalar(stmt)

    def get_by_key(
        self,
        alarm: Alarm,
        key:str,
    ) -> Setting | None:
        stmt = (
            select(Setting)
            .where(Setting.alarm_id == alarm.id)
            .where(Setting.key == key)
        )
        return self.session.scalar(stmt)
    
    def create(
        self,
        setting: Setting,
    ) -> Setting:
        self.session.add(setting)
        self.session.commit()
        self.session.refresh(setting)
        return setting
    
    def update(
        self,
        setting: Setting,
    ) -> Setting:
        self.session.add(setting)
        self.session.commit()
        self.session.refresh(setting)
        return setting
    
    def delete(
        self,
        setting: Setting,
    ) -> None:
        self.session.delete(setting)
        self.session.commit()
    