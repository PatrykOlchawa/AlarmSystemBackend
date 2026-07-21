
from app.modules.users.model import User
from app.security.auth_dependencies import get_current_user
from sqlalchemy.sql.functions import current_user
from fastapi import status
from app.modules.devices.schemas import DeviceUpdate
from app.modules.devices.schemas import DeviceCreate
from fastapi import Depends
from app.modules.devices.service import DeviceService
from app.modules.devices.dependencies import get_device_service
from app.modules.devices.schemas import DeviceResponse
from fastapi import APIRouter
from app.modules.alarms.model import Alarm
from app.security.authorization_dependencies import require_alarm_admin

router = APIRouter(
    prefix="/alarms/{alarm_id}/devices",
    tags=["Devices"],
)

@router.get(
    "",
    response_model=list[DeviceResponse],
)
def get_devices(
    service: DeviceService = Depends(get_device_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_all(alarm)

@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
)
def get_device(
    device_id: int,
    service: DeviceService = Depends(get_device_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.get_by_id(alarm,device_id)

@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_device(
    request: DeviceCreate,
    service: DeviceService = Depends(get_device_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.create(alarm,request)

@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
)
def update_device(
    device_id: int,
    request: DeviceUpdate,
    service: DeviceService = Depends(get_device_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    return service.update(alarm,device_id, request)

@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_device(
    device_id: int,
    service: DeviceService = Depends(get_device_service),
    alarm : Alarm = Depends(require_alarm_admin),
):
    service.delete(alarm,device_id)
