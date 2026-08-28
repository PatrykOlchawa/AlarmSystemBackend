from app.common.enums import (
    ConnectionType,
    DeviceType,
    MessageEventType
) 

from app.modules.devices.schemas import (
    DeviceUpdate,
    DeviceCreate,
)
from app.core.exceptions import (
    DeviceAlreadyExistsException,
    DeviceNotFoundException,
    WebsocketException,
    InvalidConnectionTypeException
)
from app.modules.devices.model import Device
from app.modules.devices.repository import DeviceRepository
from app.modules.alarms.model import Alarm
from app.services.websocket_service import WebSocketMessageService
from app.mqtt.service import MQTTService
class DeviceService:
    def __init__(
        self,
        repository: DeviceRepository,
        websocket_service: WebSocketMessageService,
        mqtt_service: MQTTService,
    ):
        self.repository = repository
        self.websocket_service = websocket_service
        self.mqtt_service = mqtt_service
    def get_all(
        self,
        alarm:Alarm
    ) -> list[Device]:
        return self.repository.get_all(alarm)        
        
    def get_by_id(
        self,
        alarm:Alarm,
        device_id: int,
    ) -> Device | None:
        device = self.repository.get_by_id(alarm,device_id)
        if device is None:
            raise DeviceNotFoundException()
        return device
    
    def get_by_name(
        self,
        alarm:Alarm,
        name: str,
    ) -> Device | None:
        device = self.repository.get_by_name(alarm,name)
        if device is None:
            raise DeviceNotFoundException()
        return device
    
    def get_by_type(
        self,
        alarm:Alarm,
        device_type: DeviceType,
    ) -> list[Device]:
        return self.repository.get_by_type(alarm,device_type)
    
    def get_by_connection_type(
        self,
        alarm:Alarm,
        connection_type: ConnectionType,
    ) -> list[Device]:
        return self.repository.get_by_connection_type(alarm,connection_type)
    
    def get_enabled_devices(
        self,
        alarm:Alarm,
    ) -> list[Device]:
        return self.repository.get_enabled_devices(alarm)
    
    def create(
        self,
        alarm:Alarm,
        request: DeviceCreate,
    ) -> Device:
        exist = self.repository.get_by_name(alarm,request.name)
        if exist:
            raise DeviceAlreadyExistsException()
        
        data = request.model_dump(exclude={"alarm_id"})

        if request.type == DeviceType.CAMERA:
            if request.connection_type not in {
                ConnectionType.CSI,
                ConnectionType.USB,
            }:
                raise InvalidConnectionTypeException()
            data["connection_identifier"] = (
                self._generate_camera_connection_identifier(
                    alarm=alarm,
                    connection_type=request.connection_type,
                )
            )
        device = Device(
            **data,
            alarm_id = alarm.id
        )
        alarm.config_revision += 1
        device = self.repository.create(
            alarm,
            device
        )
        self._notify_devices_changed(alarm=alarm)
        return device
    
    def update(
        self,
        alarm:Alarm,
        device_id: int,
        request: DeviceUpdate,
    ) -> Device:
        device = self.get_by_id(alarm,device_id)
        if (
            request.name is not None
            and request.name != device.name
        ):
            exist = self.repository.get_by_name(alarm,request.name)
            if exist:
                raise DeviceAlreadyExistsException()
        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(device, field, value)
            
        alarm.config_revision += 1
        device = self.repository.update(device)
        self._notify_devices_changed(alarm=alarm)
        return device
    
    def delete(
        self,
        alarm:Alarm,
        device_id: int,
    ) -> None:
        device = self.get_by_id(alarm,device_id)
        alarm.config_revision += 1
        self.repository.delete(alarm,device)
        self._notify_devices_changed(alarm=alarm)

    def _notify_devices_changed(
        self,
        alarm: Alarm,
    ) -> None:
        self.mqtt_service.publish_config(
            alarm_id=alarm.id,
            revision=alarm.config_revision,
        )
        try:
            self.websocket_service.send_message_sync(
                alarm_id=alarm.id,
                event_type=MessageEventType.DEVICES_CHANGED,
                data={},
            )
        except Exception:
            raise WebsocketException

    def _generate_camera_connection_identifier(
        self,
        alarm:Alarm,
        connection_type: ConnectionType,
    ) -> str:
        prefix = connection_type.value.lower()
        identifiers = self.repository.get_cameras_by_connection_type(
            alarm=alarm,
            connection_type=connection_type,
        )
        used_numbers: set[int] = set()

        for identifier in identifiers:
            expected_prefix = f"{prefix}"

            if not identifier.startswith(expected_prefix):
                continue
            number_part = identifier.removeprefix(expected_prefix)

            try:
                number = int(number_part)
            except ValueError:
                continue
            used_numbers.add(number)
        number = 0
        while number in used_numbers:
            number += 1

        return f"{prefix}-{number}"