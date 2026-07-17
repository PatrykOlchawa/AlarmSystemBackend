from app.common.enums import AlarmStatus
from app.modules.settings.schemas import SettingUpdate
from app.modules.settings.repository import SettingRepository
from app.core.exceptions import (
    SettingNotFoundException,
    SettingAlreadyExistsException,
)
from app.modules.settings.model import Setting
from app.modules.settings.schemas import SettingCreate

class SettingService:
    def __init__(
        self,
        repository:SettingRepository,
    ):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(
        self,
        setting_id: int,
    ):
        setting = self.repository.get_by_id(setting_id)
        if setting is None:
            raise SettingNotFoundException()
        
        return setting
    
    def get_by_key(
        self,
        key: str,
    ):
        setting = self.repository.get_by_key(key)
        if setting is None:
            raise SettingNotFoundException()
        
        return setting

    def create(
        self,
        request: SettingCreate,
    ):
        exist = self.repository.get_by_key(request.key)

        if exist is not None:
            raise SettingAlreadyExistsException()
        
        setting = Setting(
            key = request.key,
            value = request.value
        )

        return self.repository.create(setting)

    def update(
        self,
        key: str,
        request: SettingUpdate,
    ):
        setting = self.get_by_key(key)
        setting.value = request.value

        return self.repository.update(setting)
    
    def delete(
        self,
        key: str,
    ):
        setting = self.get_by_key(key)
        self.repository.delete(setting)

    def get_string(
        self,
        key: str,
    ) -> str:

        setting = self.get_by_key(key)
        return setting.value
        
    def get_bool(
        self,
        key: str,
    ) -> bool:
        value = self.get_string(key)
        return value.lower() in (
            "1",
            "true",
            "yes",
            "y",
            "on",
            "enabled"
        )
    def get_int(
        self,
        key: str,
    ) -> int:
        value = self.get_string(key)
        return int(value)

    def get_float(
        self,
        key: str,
    ) -> float:
        value = self.get_string(key)
        return float(value)

    def get_alarm_status(self) -> AlarmStatus:
        setting = self.get_by_key("alarm_status")
        return AlarmStatus(setting.value)
    
    def set_alarm_status(
        self,
        status: AlarmStatus,
    ):
        setting = self.get_by_key("alarm_status")
        setting.value = status.value
        return self.repository.update(setting)