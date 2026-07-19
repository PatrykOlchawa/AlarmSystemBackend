from app.common.enums import ConnectionType
from app.common.enums import DeviceType
from app.modules.devices.schemas import DeviceUpdate
from app.core.exceptions import DeviceAlreadyExistsException
from app.modules.devices.schemas import DeviceCreate
from app.modules.devices.model import Device
from app.modules.devices.repository import DeviceRepository
from app.core.exceptions import DeviceNotFoundException
class DeviceService:
    def __init__(
        self,
        repository: DeviceRepository,
    ):
        self.repository = repository

    def get_all(self) -> list[Device]:
        return self.repository.get_all()        
        
    def get_by_id(
        self,
        device_id: int,
    ) -> Device | None:
        device = self.repository.get_by_id(device_id)
        if device is None:
            raise DeviceNotFoundException()
        return device
    
    def get_by_name(
        self,
        name: str,
    ) -> Device | None:
        device = self.repository.get_by_name(name)
        if device is None:
            raise DeviceNotFoundException()
        return device

    def create(
        self,
        request: DeviceCreate,
    ) -> Device:
        exist = self.repository.get_by_name(request.name)
        if exist:
            raise DeviceAlreadyExistsException()
        
        device = Device(**request.model_dump())
        return self.repository.create(device)

    def update(
        self,
        device_id: int,
        request: DeviceUpdate,
    ) -> Device:
        device = self.get_by_id(device_id)
        if (
            request.name is not None
            and request.name != device.name
        ):
            exist = self.repository.get_by_name(request.name)
            if exist:
                raise DeviceAlreadyExistsException()
        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(device, field, value)
            
        return self.repository.update(device)

    def delete(
        self,
        device_id: int,
    ) -> None:
        device = self.get_by_id(device_id)
        self.repository.delete(device)
    
    def get_by_type(
        self,
        device_type: DeviceType,
    ) -> list[Device]:
        return self.repository.get_by_type(device_type)
    
    def get_by_connection_type(
        self,
        connection_type: ConnectionType,
    ) -> list[Device]:
        return self.repository.get_by_connection_type(connection_type)
    
    def get_enabled_devices(self) -> list[Device]:
        return self.repository.get_enabled_devices()