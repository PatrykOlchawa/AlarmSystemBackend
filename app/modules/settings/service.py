from app.common.enums import (
    MessageEventType,
    AlarmStatus,
    ConfigResourceType
)
from app.core.exceptions import (
    SettingNotFoundException,
    SettingAlreadyExistsException,
    AlarmNotFoundException,
    WebsocketException
)
from app.modules.settings.schemas import(
    SettingUpdate,
    SettingCreate
) 
from app.modules.alarms.model import Alarm
from app.modules.settings.repository import SettingRepository
from app.modules.settings.model import Setting
from app.services.websocket_service import WebSocketMessageService
from app.mqtt.service import MQTTService

class SettingService:
    def __init__(
        self,
        repository:SettingRepository,
        websocket_service: WebSocketMessageService,
        mqtt_service: MQTTService
    ):
        self.repository = repository
        self.websocket_service = websocket_service
        self.mqtt_service = mqtt_service

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
            return SettingNotFoundException()
        return AlarmStatus(setting.value)
    
    def set_alarm_status(
        self,
        alarm: Alarm,
        status: AlarmStatus,
    ):
        setting = self.get_by_key(alarm, "alarm_status")
        setting.value = status.value
        return self.repository.update(setting)
    
    def create(
        self,
        alarm: Alarm,
        request: SettingCreate,
    ):
        exist = self.get_by_key(alarm, request.key)

        if exist is not None:
            raise SettingAlreadyExistsException()
        
        setting = Setting(**request.model_dump(), alarm_id=alarm.id)
        alarm.config_revision += 1
        setting = self.repository.create(setting)
        self._notify_settings_changed(alarm=alarm)
        return setting

    def update(
        self,
        alarm: Alarm,
        key: str,
        request: SettingUpdate,
    ):
        setting = self.get_by_key(alarm, key)
        setting.value = request.value

        alarm.config_revision += 1
        setting = self.repository.update(setting)
        self._notify_settings_changed(alarm=alarm)
        return setting
    def delete(
        self,
        alarm: Alarm,
        key: str,
    ):
        setting = self.get_by_key(alarm, key)
        alarm.config_revision += 1
        self.repository.delete(setting)
        self._notify_settings_changed(alarm=alarm)

    def _notify_settings_changed(
        self,
        alarm: Alarm,
    ) -> None:
        self.mqtt_service.publish_config(
            alarm_id=alarm.id,
            revision=alarm.config_revision,
            resource=ConfigResourceType.SETTINGS,
        )
        try:
            self.websocket_service.send_message_sync(
                alarm_id=alarm.id,
                event_type=MessageEventType.SETTINGS_UPDATED,
                data={},
            )
        except Exception:
            raise WebsocketException