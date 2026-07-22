from app.modules.alarms.model import Alarm
from app.common.enums import AlarmStatus
from app.modules.settings.schemas import SettingUpdate
from app.modules.settings.repository import SettingRepository
from app.core.exceptions import (
    SettingNotFoundException,
    SettingAlreadyExistsException,
    AlarmNotFoundException,
)
from app.modules.settings.model import Setting
from app.modules.settings.schemas import SettingCreate

class SettingService:
    def __init__(
        self,
        repository:SettingRepository,
        
    ):
        self.repository = repository

    def get_all(
        self,
        alarm: Alarm
    ):
        return self.repository.get_all(alarm)

    def get_by_id(
        self,
        alarm: Alarm,
        setting_id: int,
    ):
        setting = self.repository.get_by_id(alarm, setting_id)
        if setting is None:
            raise SettingNotFoundException()
        
        return setting
    
    def get_by_key(
        self,
        alarm: Alarm,
        key: str,
    ):
        setting = self.repository.get_by_key(alarm, key)        
        return setting

    def create(
        self,
        alarm: Alarm,
        request: SettingCreate,
    ):
        exist = self.get_by_key(alarm, request.key)

        if exist is not None:
            raise SettingAlreadyExistsException()
        
        setting = Setting(**request.model_dump())

        return self.repository.create(setting)

    def update(
        self,
        alarm: Alarm,
        key: str,
        request: SettingUpdate,
    ):
        setting = self.get_by_key(alarm, key)
        setting.value = request.value

        return self.repository.update(setting)
    
    def delete(
        self,
        alarm: Alarm,
        key: str,
    ):
        setting = self.get_by_key(alarm, key)
        self.repository.delete(setting)

    def get_string(
        self,
        key: str,
    ) -> str:

        setting = self.get_by_key(key)
        return setting.value
        
    def get_bool(
        self,
        alarm: Alarm,
        key: str,
    ) -> bool:
        value = self.get_string(alarm, key)
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
        alarm: Alarm,
        key: str,
    ) -> int:
        value = self.get_string(alarm, key)
        return int(value)

    def get_float(
        self,
        alarm: Alarm,
        key: str,
    ) -> float:
        value = self.get_string(alarm, key)
        return float(value)

    def get_alarm_status(
        self,
        alarm: Alarm
    ) -> AlarmStatus:
        setting = self.get_by_key(alarm, "alarm_status")
        if setting is None:
            return AlarmNotFoundException()
        return AlarmStatus(setting.value)
    
    def set_alarm_status(
        self,
        alarm: Alarm,
        status: AlarmStatus,
    ):
        setting = self.get_by_key(alarm, "alarm_status")
        setting.value = status.value
        return self.repository.update(setting)