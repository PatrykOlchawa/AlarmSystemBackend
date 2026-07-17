from sqlalchemy.orm import Session
from sqlalchemy import select
from app.modules.settings.model import Setting

class SettingRepository:
    def __init__(
        self,
        session: Session,
    ):
        self.session = session
    
    def get_all(self) -> list[Setting]:
        stmt = select(Setting).order_by(Setting.key)
        return list(self.session.scalars(stmt).all())
    
    def get_by_id(
        self,
        setting_id:int,
    ) -> Setting | None:
        stmt = select(Setting).where(Setting.id == setting_id)
        return self.session.scalar(stmt)

    def get_by_key(
        self,
        key:str,
    ) -> Setting | None:
        stmt = select(Setting).where(Setting.key == key)
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
    