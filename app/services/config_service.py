from app.core.exceptions import (
    AlarmNotFoundException
)
from app.modules.clients.schemas import (
    ConfigResponse
)
from app.modules.alarms.service import AlarmService
from app.modules.settings.service import SettingService
from app.modules.devices.service import DeviceService
from app.modules.sensors.service import SensorService
from app.modules.settings.schemas import SettingConfig
from app.modules.sensors.schemas import SensorConfig
from app.modules.devices.schemas import DeviceConfig 
from app.modules.alarms.schemas import AlarmResponse 
from app.modules.clients.model import Client

class ConfigService:
    def __init__(
        self,
        alarm_service: AlarmService,
        setting_service: SettingService,
        device_service: DeviceService,
        sensor_service: SensorService,
    ):
        self.alarm_service = alarm_service
        self.setting_service = setting_service
        self.device_service = device_service
        self.sensor_service = sensor_service
    def get_config(
        self,
        client: Client,
    ) -> ConfigResponse:
        alarm = self.alarm_service.get_by_id(client.alarm_id)
        if alarm is None:
            raise AlarmNotFoundException
        settings = self.setting_service.get_all(alarm=alarm)

        devices = self.device_service.get_all(alarm=alarm)

        sensors = self.sensor_service.get_all_sensors(alarm=alarm)

        return ConfigResponse(
            alarm=AlarmResponse.model_validate(alarm),
            settings=[
                SettingConfig.model_validate(setting)
                for setting in settings
            ],
            devices=[
                DeviceConfig.model_validate(device)
                for device in devices
            ],
            sensors=[
                SensorConfig.model_validate(sensor)
                for sensor in sensors
            ],
        )
        