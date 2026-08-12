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
    WebsocketException
)
from app.modules.devices.model import Device
from app.modules.devices.repository import DeviceRepository
from app.modules.alarms.model import Alarm
from app.services.websocket_service import WebSocketMessageService
class DeviceService:
    def __init__(
        self,
        repository: DeviceRepository,
        websocket_service: WebSocketMessageService,
    ):
        self.repository = repository
        self.websocket_service = websocket_service
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
        
        device = Device(**request.model_dump(exclude={"alarm_id"}), alarm_id=alarm.id)
        device = self.repository.create(alarm,device)
        self._notify_devices_changed(alarm_id=alarm.id)
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
            
        device = self.repository.update(device)
        self._notify_devices_changed(alarm_id=alarm.id)
        return device
    
    def delete(
        self,
        alarm:Alarm,
        device_id: int,
    ) -> None:
        device = self.get_by_id(alarm,device_id)
        self.repository.delete(alarm,device)
        self._notify_devices_changed(alarm_id=alarm.id)

    def _notify_devices_changed(
        self,
        alarm_id: int,
    ) -> None:
        try:
            self.websocket_service.send_message_sync(
                alarm_id=alarm_id,
                event_type=MessageEventType.DEVICE_STATE_CHANGED,
                data={},
            )
        except Exception:
            raise WebsocketException