from app.modules.users.model import User
from app.security.auth_dependencies import get_current_user
from sqlalchemy.sql.functions import current_user
from fastapi import status
from fastapi import Depends
from app.modules.devices.service import DeviceService
from app.modules.devices.dependencies import get_device_service
from app.modules.devices.schemas import (
    DeviceResponse,
    CameraStreamTokenResponse,
    DeviceUpdate,
    DeviceCreate,
) 
from app.core.exceptions import (
   DeviceNotFoundException, 
   InvalidDeviceTypeException
)
from fastapi import APIRouter
from app.modules.alarms.model import Alarm
from app.security.authorization_dependencies import require_alarm_admin
from app.security.authorization_dependencies import require_alarm_member
from app.modules.media_auth.service import MediaAuthService
from app.modules.media_auth.dependencies import get_media_auth_service
from app.common.enums import DeviceType
from app.core.config import settings
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
    alarm : Alarm = Depends(require_alarm_member),
):
    return service.get_all(alarm)

@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
)
def get_device(
    device_id: int,
    service: DeviceService = Depends(get_device_service),
    alarm : Alarm = Depends(require_alarm_member),
):
    return service.get_by_id(alarm,device_id)

@router.get(
    "/cameras/{device_id}/stream-token",
    response_model=CameraStreamTokenResponse,
)
def get_camera_stream_token(
    device_id: int,
    alarm : Alarm = Depends(require_alarm_member),
    devices_service: DeviceService = Depends(get_device_service),
    media_auth_service: MediaAuthService = Depends(get_media_auth_service),
):
    camera = devices_service.get_by_id(
        alarm=alarm,
        device_id=device_id,
    )
    if camera is None:
        raise DeviceNotFoundException
    if camera.device_type != DeviceType.CAMERA:
        raise InvalidDeviceTypeException
    
    permissions = media_auth_service.create_stream_permissions(
        alarm = alarm,
    )

    token = media_auth_service.create_camera_stream_token(
        permissions=permissions
    )

    return CameraStreamTokenResponse(
        token=token,
        expires_in=settings.mediamtx_token_expire_minutes * 60,
        path=media_auth_service.get_stream_path(
            alarm=alarm,
        ),        
    )

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

@router.patch(
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
