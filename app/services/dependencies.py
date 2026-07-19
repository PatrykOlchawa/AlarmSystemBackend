from app.modules.car_plates.dependencies import get_car_plate_service
from app.services.tollgate_service import TollgateService
from app.services.ocr_service import OCRService
from app.modules.auth.dependencies import get_auth_service
from app.services.alarm_service import AlarmService
from typing import TYPE_CHECKING
from fastapi import Depends
from app.modules.settings.dependencies import get_settings_service
from app.modules.users.dependencies import get_user_service
from app.modules.sensors.dependencies import get_sensor_service
from app.modules.events.dependencies import get_alarm_event_service
from app.modules.notifications.dependencies import get_notification_service
from app.services.device_control_service import DeviceControlService
from app.modules.devices.service import DeviceService
from app.modules.devices.dependencies import get_device_service


#if TYPE_CHECKING:
 #   from app.modules.readings.dependencies import get_sensor_reading_service


def get_device_control_service(
    device_service: DeviceService = Depends(get_device_service),
) -> DeviceControlService:
    return DeviceControlService(device_service)
    
def get_ocr_service(
    
) -> OCRService:
    return OCRService()


def get_tollgate_service(
    device_control_service = Depends(get_device_control_service),
    ocr_service = Depends(get_ocr_service),
    car_plate_service = Depends(get_car_plate_service),
    settings_service = Depends(get_settings_service),
    device_service = Depends(get_device_service),
) -> TollgateService:
    return TollgateService(
        device_control_service,
        ocr_service,
        car_plate_service,
        settings_service,
        device_service)

def get_alarm_service(
    settings_service = Depends(get_settings_service),
    sensor_service = Depends(get_sensor_service),
    alarm_event_service = Depends(get_alarm_event_service),
    notification_service = Depends(get_notification_service),
    device_service = Depends(get_device_service),
    user_service = Depends(get_user_service),
    auth_service = Depends(get_auth_service),
    device_control_service = Depends(get_device_control_service),
    tollgate_service = Depends(get_tollgate_service),
) -> AlarmService:

    return AlarmService(
        settings_service=settings_service,
        sensor_service=sensor_service,
        alarm_event_service=alarm_event_service,
        notification_service=notification_service,
        device_service=device_service,
        user_service=user_service,
        auth_service=auth_service,
        device_control_service=device_control_service,
        tollgate_service=tollgate_service,
    )

