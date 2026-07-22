from app.common.enums import ConnectionType
from app.common.enums import DeviceType
from app.modules.devices.schemas import DeviceUpdate
from app.core.exceptions import DeviceAlreadyExistsException
from app.modules.devices.schemas import DeviceCreate
from app.modules.devices.model import Device
from app.modules.devices.repository import DeviceRepository
from app.core.exceptions import DeviceNotFoundException
from app.modules.alarms.model import Alarm
class DeviceService:
    def __init__(
        self,
        repository: DeviceRepository,
    ):
        self.repository = repository

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

    def create(
        self,
        alarm:Alarm,
        request: DeviceCreate,
    ) -> Device:
        exist = self.repository.get_by_name(alarm,request.name)
        if exist:
            raise DeviceAlreadyExistsException()
        
        device = Device(**request.model_dump(exclude={"alarm_id"}), alarm_id=alarm.id)
        return self.repository.create(alarm,device)

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
            
        return self.repository.update(alarm,device)

    def delete(
        self,
        alarm:Alarm,
        device_id: int,
    ) -> None:
        device = self.get_by_id(alarm,device_id)
        self.repository.delete(alarm,device)
    
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